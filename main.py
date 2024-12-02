import nextcord
import json
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from wakeonlan import send_magic_packet

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TESTING_GUILD_ID = os.getenv('TESTING_GUILD_ID')

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="Show all id with the name", guild_ids=[TESTING_GUILD_ID])
async def show(interaction: nextcord.Interaction):
    with open('list.json', 'r') as f:
        data = json.load(f)
    embed = nextcord.Embed(title="List of ID", description="List of ID with the name", color=nextcord.Color.green())
    for id, name in data.items():
        embed.add_field(name=name, value="", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(description="Wake a device on LAN", guild_ids=[TESTING_GUILD_ID])
async def wake(interaction: nextcord.Interaction, name: str):
    try:
        with open('list.json', 'r') as f:
            data = json.load(f)
        mac = data[name]
        send_magic_packet(mac)
        await interaction.response.send_message(f"Magic packet sent to {name}")
    except Exception as e:
        await interaction.response.send_message(f"Failed to send magic packet: {e}")

bot.run(DISCORD_BOT_TOKEN)