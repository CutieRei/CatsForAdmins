import discord,sqlite3,random,os
from discord.ext import commands

class Balance(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		
	@commands.command()
	async def verify(self,ctx,member:discord.Member=None):
		db = sqlite3.connect("data.db")
		cursor = db.cursor()
		if member and "Mod" in [i.name for i in ctx.author.roles]:
			cursor.execute("""
			SELECT * FROM info WHERE id = ?
			""",(member.id,))
			db.commit()
			user = cursor.fetchone()
			if user:
				await ctx.send("That member is verified!")
			else:
				cursor.execute("""
				INSERT INTO info VALUES(?,?,?)
				""",(member.id,member.name,0,))
				db.commit()
				db.close()
				await ctx.send(f"> Verified {member.name}!")
				db.close()
		else:
			cursor.execute("""
			SELECT * FROM info WHERE id = ?
			""",(ctx.author.id,))
			db.commit()
			user = cursor.fetchone()
			if user:
				await ctx.send("You already verified!")
			else:
				cursor.execute("""
				INSERT INTO info VALUES(?,?,?)
				""",(ctx.author.id,ctx.author.name,0,))
				db.commit()
				db.close()
				await ctx.send(f"> {ctx.author.name} you are verified!")
				db.close()


def setup(bot):
	bot.add_cog(Balance(bot))