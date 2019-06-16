

from discord.ext import commands
from discord.ext.commands import bot
import discord
import utils.cog

#TODO react to delete message (let other staff know it's settled)

class permissions(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	async def getSettings(self,serverid):
		return await self.bot.cogs['settings'].getSettings(serverid,'permissions')

	@commands.command()
	async def setRole(self,ctx,discorRole:discord.Role,botRole:str):
		if botRole not in ['host','staff','admin']:
			await ctx.send("Bot role is")



	async def bot_check(self,ctx):
		guy = ctx.author
		command = ctx.command
		perms = await self.getSettings()
		guyRolesId = [r.id for r in guy.roles]
		authorizedRolesId = perms.get(command.name,[])
		if len(set(guyRolesId) & set(authorizedRolesId)) > 0:
			return True
		else:
			raise notAuthorized


def setup(bot):
	utils.cog.setupper(bot,permissions(bot),"permissions")