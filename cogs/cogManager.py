from discord.ext import commands
import utils.cog
from utils.checks import dev
import traceback
import importlib
import cogs

class cogManager(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.last = "cogs.cogManager"
	
	@commands.command(aliases=["r"])
	@dev()
	async def reload(self,ctx,*,cog=None):
		
		if cog == None:
			cog = self.last
		else:
			cog = 'cogs.'+cog
		self.last = cog
		try:
			self.bot.reload_extension(cog)
			await ctx.send(f'{cog} Reloaded')
		except Exception as e:
			await ctx.send("""**Traceback:**\n```{0}```\n""".format(' '.join(traceback.format_exception(None, e, e.__traceback__))))

	
	@commands.command()
	@dev()
	async def unload(self,ctx,*,cog:str):
		self.last = cog
		try:
			cog = 'cogs.'+cog
			self.bot.unload_extension(cog)
			await ctx.send(f'{cog} Unloaded')
		except Exception as e:
			await ctx.send("""**Traceback:**\n```{0}```\n""".format(' '.join(traceback.format_exception(None, e, e.__traceback__))))
	
	@commands.command(aliases=["l"])
	@dev()
	async def load(self,ctx,*,cog=None):
		
		if cog == None:
			cog = self.last
		else:
			cog = 'cogs.'+cog
		self.last = cog
		
		try:
			importlib.reload(cogs)
			self.bot.load_extension(cog)
			await ctx.send(f'{cog} Loaded')
		except Exception as e:
			await ctx.send("""**Traceback:**\n```{0}```\n""".format(' '.join(traceback.format_exception(None, e, e.__traceback__))))

def setup(bot):
	utils.cog.setupper(bot,cogManager(bot),"cogManager")