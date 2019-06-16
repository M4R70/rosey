from discord.ext import commands
from utils.checks import dev
import traceback
import importlib
import cogs
class Cog_man:
	def __init__(self,bot):
		self.bot = bot	
	
	@commands.command()
	@dev()
	async def reload(self,ctx,*,cog:str):
		print('Tried to reload ' + cog)
		cog = 'cogs.'+cog
		try:
			self.bot.unload_extension(cog)
			importlib.reload(cogs)
			self.bot.load_extension(cog)
			await ctx.send('Done')
		except Exception as e:
			await ctx.send("""**Traceback:**\n```{0}```\n""".format(' '.join(traceback.format_exception(None, e, e.__traceback__))))

	
	@commands.command()
	@dev()
	async def unload(self,ctx,*,cog:str):
		try:
			print('Tried to unload ' + cog)
			cog = 'cogs.'+cog
			self.bot.unload_extension(cog)
			await ctx.send('Done')
		except Exception as e:
			await ctx.send("""**Traceback:**\n```{0}```\n""".format(' '.join(traceback.format_exception(None, e, e.__traceback__))))
	
	@commands.command()
	@dev()
	async def load(self,ctx,*,cog:str):
		print('Tried to load ' + cog)
		cog = 'cogs.'+cog
		try:
			importlib.reload(cogs)
			self.bot.load_extension(cog)
			await ctx.send('Done')
		except Exception as e:
			await ctx.send("""**Traceback:**\n```{0}```\n""".format(' '.join(traceback.format_exception(None, e, e.__traceback__))))

def setup(bot):
	bot.add_cog(Cog_man(bot))