from discord.ext import commands
# from utils.checks import kl_only
# from utils.checks import queue_exists
# from utils.checks import host
from utils import db
import utils.cog
import discord
import random
from cogs.errors import *
from iteration_utilities import deepflatten


async def is_host(user,ctx):
	rids = [r.id for r in user.roles]
	s = await ctx.cog.getSettings(ctx.guild.id,cogOnly=False)
	hostRoleid = s['roles']['Host']
	return hostRoleid in rids

def Host():
	async def predicate(ctx):
		ish = await is_host(ctx.author,ctx) 
		if ish:
			return True
		else:
			raise notAuthorized
	return commands.check(predicate)

def Staff():
	async def predicate(ctx):
		rids = [r.id for r in ctx.author.roles]
		s = await ctx.cog.getSettings(ctx.guild.id,cogOnly=False)


		staffRoleid = s['roles']['Staff']
		if staffRoleid in rids:
			return True
		else:
			raise notAuthorized
	return commands.check(predicate)
		

def QIsNotEmpty():
	async def predicate(ctx):
		q = await ctx.cog.getQ(ctx.guild.id,ctx.channel.id)
		if len(q['queue']) > 0:
			return True
		else:
			raise queueIsEmpty
	return commands.check(predicate)


def UserNotInQueue():
	async def predicate(ctx):
		user = ctx.author.id
		q = await ctx.cog.getQ(ctx.guild.id,ctx.channel.id)
		if user in q['queue']:
			raise userAlreadyInQueue
		else:
			return True
	return commands.check(predicate)

def UserInQueue():
	async def predicate(ctx):
		user = ctx.author.id
		q = await ctx.cog.getQ(ctx.guild.id,ctx.channel.id)
		if not userid in q['queue']:
			raise userNotInQueue
		else:
			return True
	return commands.check(predicate)

def QIsNotClosed():
	async def predicate(ctx):
		q = await ctx.cog.getQ(ctx.guild.id,ctx.channel.id)
		if q['closed']:
			raise queueIsClosed
		else:
			return True
	return commands.check(predicate)


def QPerms(perm):
	async def predicate(ctx):
		cog = ctx.cog
		s = await cog.getSettings(ctx.guild.id)
		if perm == 'next':
			q = await ctx.cog.getQ(ctx.guild.id,ctx.channel.id)
			if not q['locked']:
				return True

		userPermissions = list(set(deepflatten([s['permissions'].get(str(r.id),[]) for r in ctx.author.roles ],depth=1)))
		if perm not in userPermissions:
			raise notAuthorized
		else:
			return True
	return commands.check(predicate)

def QEnabled():
	async def predicate(ctx):
		cog = ctx.cog
		s = await cog.getSettings(ctx.guild.id)
		if s['enabled'] == False:
			raise notEnabled
		else:
			return True

	return commands.check(predicate)

def QDoesNotExist():
	async def predicate(ctx):
		cog = ctx.cog
		q = await cog.getQ(ctx.guild.id,ctx.channel.id)
		if q == None:
			return True
		else:
			raise queueAlreadyExists
	return commands.check(predicate)

def QExists():
	async def predicate(ctx):
		cog = ctx.cog
		q = await cog.getQ(ctx.guild.id,ctx.channel.id)
		if q != None:
			return True
		else:
			raise queueDoesNotExist

	return commands.check(predicate)
class queues(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.db = utils.db.getDB()
		# self.perms = ['create/delete']

	async def getQ(self,serverid,channelid):
		return await self.db['queues'].find_one({'server_id':serverid,'channel_id':channelid})

	async def updateQ(self,q):
		await self.db['queues'].update_one({'server_id':q['server_id'],'channel_id':q['channel_id']},{'$set':q},upsert=True)

	async def getSettings(self,serverid,cogOnly=True):
		if cogOnly:
			return await self.bot.cogs['settings'].getSettings(serverid,'queues')
		else:
			return await self.bot.cogs['settings'].getSettings(serverid)





	# se chequean de abajo para arriba
	@Staff()
	@QDoesNotExist()
	@QEnabled()
	@commands.command()
	async def qcreate(self,ctx):
		await self.updateQ({
		'server_id':ctx.guild.id,
		'channel_id':ctx.channel.id,
		'queue': [],
		'closed':False,
		'locked':False
		})


		await ctx.send('Queue created :thumbsup:')
	@Staff()
	@QExists()
	@QEnabled()
	@commands.command()	
	async def qdelete(self,ctx):
		await self.db['queues'].delete_one({'server_id':ctx.guild.id,'channel_id':ctx.channel.id})
		await ctx.send('Queue deleted :thumbsup:')


	
	@UserNotInQueue()
	@QIsNotClosed()
	@QExists()
	@QEnabled()
	@commands.command(aliases=["qj"])
	async def qjoin(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		q['queue'].append(ctx.author.id)
		await self.updateQ(q)
		await ctx.send(ctx.author.display_name + ' joined the queue!')

	@UserInQueue()
	@QExists()
	@QEnabled()
	@commands.command(aliases=["ql"])
	async def qleave(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		q['queue'].remove(ctx.author.id)
		await self.updateQ(q)
		await ctx.send(ctx.author.display_name + ' left the queue :(')


	@QExists()
	@QEnabled()
	@commands.command(aliases=["q"])
	async def qprint(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		queue = q['queue']
		e = self.embedQ(queue,ctx)
		await ctx.send(embed=e)
	
	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def qclose(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		q['closed'] = True
		await self.updateQ(q)
		await ctx.send("Queue closed :thumbsup:")
	
	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def qopen(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		q['closed'] = False
		await self.updateQ(q)
		await ctx.send("Queue opened :thumbsup:")

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def qreset(self,ctx):
		await self.updateQ({
		'server_id':ctx.guild.id,
		'channel_id':ctx.channel.id,
		'queue': [],
		})
		await ctx.send('Queue cleared :thumbsup:')

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def qshuffle(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		random.shuffle(q['queue'])
		await self.updateQ(q)
		await ctx.send("Queue shuffled :thumbsup:")

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def shoo(self,ctx,user:discord.Member):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		if not user.id in q['queue']:
			raise userNotInQueue
		q['queue'].remove(user.id)
		await self.updateQ(q)
		await ctx.send(f"{user} was removed from the queue :thumbsup:")

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def drag(self,ctx,user:discord.Member):

		
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		if user.id in q['queue']:
			raise userAlreadyInQueue
		q['queue'].append(user.id)
		await self.updateQ(q)
		await ctx.send(f"{user} was dragged to the queue :thumbsup:")		
	
	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def qlock(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		q['locked'] = True
		await self.updateQ(q)
		await ctx.send("Queue locked :thumbsup:")

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def qunlock(self,ctx):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		q['locked'] = False
		await self.updateQ(q)
		await ctx.send("Queue opened :thumbsup:")

	
	@QIsNotEmpty()
	@QExists()
	@QEnabled()
	@commands.command(aliases=["qn"])
	async def qnext(self,ctx):
		queue = await self.getQ(ctx.guild.id,ctx.channel.id)

		if queue['locked'] == True:
			ish = await is_host(ctx.author,ctx) 
			if not ish:
				await ctx.send("Only hosts can qn when the queue is locked :x:")
				return
		q = queue['queue']
		if len(q) == 1:
			queue['queue'] = []
			await ctx.send("There's no more people in the queue :(")
			await self.updateQ(queue)
			return
		else:
			q.pop(0) #previous turn
			currentPerformer = ctx.guild.get_member(q[0])
			if currentPerformer != None:
				msg = f"It is now {currentPerformer.mention}'s turn!"
			else:
				if ctx.command.can_run():
					ctx.invoke(ctx.command)
			if len(q) > 1:
				nextPerformer = ctx.guild.get_member(q[1])
				if q[1] != None:
					msg += f"\n {nextPerformer.mention} your turn comes next, please be ready!"
			queue['queue'] = q
			await self.updateQ(queue)
			await ctx.send(msg)

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def put(self,ctx,user:discord.Member,pos:int):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)
		if user.id in q['queue']:
			q['queue'].remove(user.id)
		q['queue'].insert(pos,user.id)
		await self.updateQ(q)
		await ctx.send('Done :thumbsup:')

	@Host()
	@QExists()
	@QEnabled()
	@commands.command()
	async def swap(self,ctx,user1:discord.Member,user2:discord.Member):
		q = await self.getQ(ctx.guild.id,ctx.channel.id)

		if not user1.id in q['queue'] or user2.id not in q['queue']:
			raise userNotInQueue
		i = q['queue'].index(user1.id)
		j = q['queue'].index(user2.id)
		q['queue'][i],q['queue'][j] = q['queue'][j],q['queue'][i]
		await self.updateQ(q)
		await ctx.send('Done :thumbsup:')

	def embedQ(self,q,ctx): #legacy code, but works
		e = discord.Embed()
		e.colour = discord.Colour.blue()
		e.title = "Queue:"
		i=0
		for guyid in q:
			guy = ctx.guild.get_member(guyid)
			if guy:
				if i == 0:
					e.add_field(name=f"\u200b \u0009 Current turn: {guy.display_name}",value="\u200b",inline = False)
				else:
					e.add_field(name=f"\u200b \u0009 {i} \u200b \u0009 {guy.display_name}",value="\u200b",inline = False)

				i+=1
		return e

def setup(bot):
	utils.cog.setupper(bot,queues(bot),"queues")