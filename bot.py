
from discord.ext import commands
import json
import os

def hola():
    print('aloha')

with open('creds.json','r') as f:
    creds = json.load(f)
    token = creds["token"]

bot = commands.AutoShardedBot(command_prefix='!', formatter=None, description=None, pm_help=False,max_messages=50000)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"ID: {bot.user.id}")
    for cog in os.listdir('cogs/'):
        try:
            if cog.endswith('.py'):
                bot.load_extension("cogs."+cog[:-3])
            print("All cogs loaded OK")
        except Exception as e:
            print("Error loading cog")
            print(e)


bot.run(token)