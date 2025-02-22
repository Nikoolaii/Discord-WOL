import nextcord
from nextcord.ext import commands
from controller.database import Database

class SetlogsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(description='Set the logs channel')
    async def setlogs(self, interaction: nextcord.Interaction):
        # Send an embed message
        embed = nextcord.Embed(title='Set logs channel', description='Set the logs channel', color=nextcord.Color.green())
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()

        # Create the table in the database
        self.db.create_table('logs_channel', ['channel_id TEXT PRIMARY KEY, server_id TEXT UNIQUE'])

        # Store the channel ID in the database, replacing the previous one if it exists
        insert_message_query = "INSERT OR REPLACE INTO logs_channel (channel_id, server_id) VALUES (?, ?)"
        self.db.execute_query(insert_message_query, (str(interaction.channel_id), str(interaction.guild_id)))

        await interaction.channel.send(f"Logs channel set to {interaction.channel_id}")

def setup(bot):
    bot.add_cog(SetlogsCommand(bot))
