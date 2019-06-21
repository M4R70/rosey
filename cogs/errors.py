from discord.ext import commands
import discord
import utils.cog
import traceback
import sys
class errors(commands.Cog):
	def __init__(self,bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_command_error(self,ctx,e):
		
		if isinstance(e,commands.CommandNotFound):
			return
		
		if isinstance(e,generic):
			await ctx.send(e.message)

		if isinstance(e,notAuthorized):
			await ctx.send(" You are not authorized to do this :x:")
		
		elif isinstance(e,queueAlreadyExists):
			await ctx.send(" This channel already has a queue :x:")
		
		elif isinstance(e,queueDoesNotExist):
			await ctx.send(" This channel does not have a queue :x:")
		
		elif isinstance(e,queueIsEmpty):
			await ctx.send(" The queue is empty :x:")
		
		elif isinstance(e,userAlreadyInQueue):
			await ctx.send(" User already is in this queue :x:")
		
		elif isinstance(e,userNotInQueue):
			await ctx.send(" User is not not on this queue :x:")

		elif isinstance(e,queueIsClosed):
			await ctx.send(" This queue is closed :x:")

				
		elif isinstance(e,notEnabled):
			await ctx.send(" This feature is not enabled :x:")
		else:
			 traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def setup(bot):
	utils.cog.setupper(bot,errors(bot),"errors")


class generic(discord.ext.commands.CommandError):
	pass

class notAuthorized(discord.ext.commands.CommandError):
	pass
	
class userAlreadyInQueue(discord.ext.commands.CommandError):
	pass

class userNotInQueue(discord.ext.commands.CommandError):
	pass

class queueIsClosed(discord.ext.commands.CommandError):
	pass
	
class queueAlreadyExists(discord.ext.commands.CommandError):
	pass

class queueDoesNotExist(discord.ext.commands.CommandError):
	pass

class queueIsEmpty(discord.ext.commands.CommandError):
	pass


class notEnabled(discord.ext.commands.CommandError):
	pass