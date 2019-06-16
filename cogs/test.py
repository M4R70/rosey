from discord.ext import commands
from discord.ext.commands import bot
import discord
import utils.cog
import pprint

#TODO react to delete message (let other staff know it's settled)

class test(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def t(self,ctx):
		commands = [c for c in self.bot.commands]
		d = {}
		for c in commands:
			cogname = c.cog.__class__.__name__
			if cogname in d:
				d[cogname][c.name] = 0
			else:
				d[cogname] = {c.name:0}
				
		await ctx.send(pprint.pformat(d))
	
			

def setup(bot):
	utils.cog.setupper(bot,test(bot),"test")