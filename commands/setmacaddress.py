import nextcord
from nextcord.ext import commands
from controller.database import Database

class SetmacaddressCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(description='Set the MAC address of the computer to wake up')
    async def setmacaddress(self, interaction: nextcord.Interaction, mac_address: str, user: nextcord.Member = None):
        self.db.create_table('mac_address', ['mac_address TEXT PRIMARY KEY', 'user_id TEXT UNIQUE'])

        # Utiliser l'utilisateur mentionné ou l'auteur du message
        target_user = user if user else interaction.user

        # Store the MAC address in the database, replacing the previous one if it exists
        insert_mac_address_query = "INSERT OR REPLACE INTO mac_address (mac_address, user_id) VALUES (?, ?)"
        self.db.execute_query(insert_mac_address_query, (mac_address, str(target_user.id)))

        await interaction.response.send_message(f"MAC address set to {mac_address} for {target_user.mention}")

def setup(bot):
    bot.add_cog(SetmacaddressCommand(bot))