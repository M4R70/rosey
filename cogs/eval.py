from discord.ext import commands
import utils.cog
from utils.checks import dev
from io import StringIO
import traceback
import discord
import contextlib

class eval(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.is_owner()
	@commands.command(aliases=['ev'])
	async def eval(self,ctx,*,code):

		code = code.lstrip("`").rstrip("`")

		for line in code.split("\n"):
			for word in line.split(" "):
				orig = word
				current = word.replace('\n','')
				# print(current + """ start({0}) end({1})""".format(current[0],current[len(current)-1]))
				if current.startswith('<') and current.endswith('>'):
					ide = current.replace('<','').replace('>','')
					new = """discord.utils.find(lambda m: m.id == {0}, ctx.guild.members)""".format(int(ide))
					if orig.endswith('\n'):
						new+='\n'
					code = code.replace(orig,new)			
		
		# code = ' '.join(replacer)
		lines = code.split("\n")
		lines = ["    " + i for i in lines]
		newline = '\n'
		f_code = """async def _():\n{0}""".format(newline.join(lines))
		stdout = StringIO()

		try:
			namespace = {'bot':self.bot,'ctx':ctx,'discord':discord}
			exec(f_code, namespace, namespace)
			func = namespace["_"]

			with contextlib.redirect_stdout(stdout):
				result = await func()

		except Exception as e:
			result = traceback.format_exception(None, e, e.__traceback__)
		finally:
			stdout.seek(0)
		fmt=''
		outp = stdout.read()
		if outp:
			fmt+= """**output:**\n```{0}```\n""".format(outp)
		if result:
			fmt += """**Traceback:**\n```{0}```\n""".format(newline.join(result))
		if fmt != '':
			await ctx.send(fmt)

def setup(bot):
	utils.cog.setupper(bot,eval(bot),"eval")