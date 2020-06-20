import discord
from discord.ext import commands
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix=["!","?"])

@bot.event
async def on_ready():
	print(f"{bot.user.name} has joined!")
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS info(
		id INTEGER,
		name TEXT,
        strike INTEGER
	)
	""")
	
	db.commit()

@bot.command()
async def verify(ctx):
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	card = discord.Embed(
	colour=discord.Colour.from_rgb(20,255,20),
	title="Success!",
	description="You are verified!"
	)
	card.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url_as(static_format='png'))
	cursor.execute("SELECT * FROM info WHERE name=?",(ctx.author.name,))
	db.commit()
	row = cursor.fetchone()
	db.commit()
	if row:
		card.colour = discord.Colour.from_rgb(255,20,20)
		card.title="Failed!"
		card.description="You already verified!"
		await ctx.send(embed=card)
		db.close()
	else:
		
		cursor.execute("""INSERT INTO info VALUES (?,?,?)
		 """,(ctx.author.id,ctx.author.name,0,))
		 
		await ctx.send(embed=card)
		 
		db.commit()
		db.close()


@bot.command()
@commands.has_role("Reyter")
async def dc(ctx):
	card = discord.Embed(
	colour=discord.Colour.from_rgb(20,255,20),
	title="Successfully disconnected meow!"
	)
	await ctx.send(embed=card)
	await bot.logout()

@bot.command()
@commands.has_any_role("Mod","Reyter")
async def clear(ctx,msg:int):
	channel = ctx.channel
	deleted = await channel.purge(limit=msg)
	card = discord.Embed(
	colour=discord.Colour.from_rgb(20,255,20),
	title=f"Deleted {len(deleted)} messages"
	)
	await ctx.send(embed=card,delete_after=4)
	
@bot.command(aliases=["Hammer","hammer","poop","Poop"])
@commands.has_any_role("Mod","Reyter")
async def ban(ctx,member:discord.Member,reason=None):
	if reason == None:
		reason = "Undefined"
	await member.ban(reason=reason)
	card = discord.Embed(
	colour=ctx.author.color,
	title=f"Haha now go meow!",
	description=f"{ctx.author.name} has banned {member.name}, Reason: {reason}"
	)
	await ctx.send(embed=card)
@bot.command(aliases=["Stroke","bite","Bite","stroke"])
@commands.has_any_role("Mod","Reyter")
async def strike(ctx,member:discord.Member,strike=1):
    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM info WHERE id = ?
    """,(member.id,))
    db.commit()
    user = cursor.fetchone()
    print(user)
    if user[0] == ctx.author.id:
    	await ctx.send("You cant strike yourself lol")
    	db.close()
    else:
    	userStrike = user[2]+strike
    	cursor.execute("""
    		UPDATE info
    			SET strike = ?
    			WHERE name = ?
    		""",(userStrike,member.name,))
    	db.commit()
    	db.close()
    	card = discord.Embed(
    	colour=discord.Colour.from_rgb(255,20,20),
    	title=f"{member.name} has been given {strike} strikes by {ctx.author.name}"
    	)
    	await ctx.send(embed=card)
    
bot.run(TOKEN)