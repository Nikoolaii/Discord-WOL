import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from controller.database import Database

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # Appeler la méthode on_ready de chaque cog
    for cog in bot.cogs.values():
        if hasattr(cog, 'on_ready'):
            await cog.on_ready()

# Charger les commandes depuis le dossier commands
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

bot.run(DISCORD_BOT_TOKEN)