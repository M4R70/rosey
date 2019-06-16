from discord.ext import commands
import discord
import utils.cog
import os


class cicd(commands.Cog):
	def __init__(self,bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_message(self,message):
		if message.channel.id == 588156320796901376:
			title =  message.embeds[0].title 
			if "new commit" in title and "[oompa2:master]" in title:
				os.system("git pull")
				for ename,e in self.bot.extensions.items():
					if ename != "cogs.CiCd":
						self.bot.reload_extension(ename)


def setup(bot):
	utils.cog.setupper(bot,cicd(bot),"cicd")