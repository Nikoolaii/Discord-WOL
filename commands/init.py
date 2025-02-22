import nextcord
from nextcord.ext import commands
from controller.database import Database
from controller.wol import WakeOnLan
from datetime import datetime

class StartButton(nextcord.ui.View):
    def __init__(self, db):
        super().__init__()
        self.db = db

    @nextcord.ui.button(label="Démarrer", style=nextcord.ButtonStyle.green)
    async def start_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Récupérer l'adresse MAC depuis la base de données
        select_mac_query = "SELECT mac_address FROM mac_address WHERE user_id = ?"
        mac_address = self.db.execute_read_query(select_mac_query, (str(interaction.user.id),))
        if mac_address:
            WakeOnLan.wake(mac_address[0][0])
            await interaction.response.send_message(str(interaction.user.mention) + " ton pc démarre...", delete_after=20)

            # Get log channel ID from the database
            select_query = "SELECT channel_id FROM logs_channel WHERE server_id = ?"
            channel_id = self.db.execute_read_query(select_query, (str(interaction.guild_id),))
            if channel_id:
                channel = interaction.guild.get_channel(int(channel_id[0][0]))
                if channel:
                    # Obtenir la date et l'heure actuelles
                    now = datetime.now()
                    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    await channel.send(f"{formatted_time} : {interaction.user.name}")
        else:
            await interaction.response.send_message("Adresse MAC non trouvée pour cet utilisateur.")

class InitCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(description='Initialisation of the bot')
    async def init(self, interaction: nextcord.Interaction):
        # Send an embed message
        embed = nextcord.Embed(title='Démarrage a distance', description='Un clique et hop ton pc démarre', color=nextcord.Color.green())

        # Create a button
        view = StartButton(self.db)
        await interaction.response.send_message(embed=embed, view=view)
        message = await interaction.original_message()

        # Create the table in the database
        self.db.create_table('messages', ['message_id TEXT PRIMARY KEY', 'channel_id TEXT', 'server_id TEXT UNIQUE'])

        # Store the message ID and channel ID in the database, replacing the previous one if it exists
        insert_message_query = "INSERT OR REPLACE INTO messages (message_id, channel_id, server_id) VALUES (?, ?, ?)"
        self.db.execute_query(insert_message_query, (str(message.id), str(interaction.channel_id), str(interaction.guild_id)))

    async def on_ready(self):
        # Fetch the message ID and channel ID from the database
        select_query = "SELECT message_id, channel_id FROM messages"
        messages = self.db.execute_read_query(select_query)
        if messages:
            for message_id, channel_id in messages:
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    try:
                        message = await channel.fetch_message(int(message_id))
                        if message:
                            # Create a button
                            view = StartButton(self.db)
                            await message.edit(view=view)
                    except Exception as e:
                        print(f"Erreur lors de la récupération du message : {e}")

def setup(bot):
    bot.add_cog(InitCommand(bot))