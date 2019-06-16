from discord.ext import commands
import discord
import utils.cog
import utils.db
import json
import pprint

class invalidParameters(discord.ext.commands.CommandError):
	pass


class settings(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.settings = {"staffPingChannel":588176999215005698,"staffPingRole":588201589156741131} #TODO
		self.db = utils.db.getDB()


	async def getSettings(self,serverid,cog=None):
		#TODO caching (maybe)
		s = await self.db['settings'].find_one({'server_id':serverid})
		if cog == None:
			return s
		elif s == None:
			return {'enabled':False}
		else:
			return s.get(cog,{'enabled':False})


	async def updateSettings(self,serverid,newSettings):

		await self.db['settings'].update_one({'server_id':serverid}, {'$set':newSettings},upsert=True)



	@commands.command()
	async def showSettings(self,ctx):
		s = await self.getSettings(ctx.guild.id)
		s.pop('_id')
		with open('settings.json','r+') as f:
			json.dump(s,f,indent=4, separators=(',', ': '))
		with open('settings.json','r') as f:
			dfile = discord.File(f)
		try:
			await ctx.send(pprint.pformat(s))
		except:
			await ctx.send("Here are the current settings for this server",file=dfile)

	@commands.command(aliases=['updateSettings'])
	async def _updateSettings(self,ctx,*,override=None):
		if override == None:
			if len(ctx.message.attachments) == 1:
				attachment = ctx.message.attachments[0]
				await attachment.save('infile.json')
				with open('infile.json','r+') as f:
					override = json.load(f)
			else:
				raise invalidParameters
		else:
			override = json.loads(override)
		await self.updateSettings(ctx.guild.id,override)
		await ctx.send("Settings updated!")

		


def setup(bot):
	utils.cog.setupper(bot,settings(bot),"settings")