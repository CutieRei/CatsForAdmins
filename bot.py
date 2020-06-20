import discord
from discord.ext import commands
import sqlite3
import os,random
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
	
@bot.check
def custom_check(ctx):
	if "Mod" in [i.name for i in ctx.author.roles] and ctx.channel.name not in ["bot-1","bot-2"]:
		return True
	elif "Mod" not in [i.name for i in ctx.author.roles] and ctx.channel.name not in ["bot-1","bot-2"]:
		return False
	else:
		return True
		

@bot.event
async def on_member_join(member):
	db = sqlite3.connect("data.db")
	cursor = db.cursor()
	welcomes = random.choice([f"Hello {member.mention}, have fun here👋",f"Welcome {member.mention}, we hope you have fun here😄",f"Hello, friend {member.mention} have fun while in here😊"])
	card = discord.Embed(
	colour=discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
	title=f"Welcome {member.name}",
	description=welcomes
	)
	card.set_thumbnail(url=member.avatar_url_as(static_format='png'))
	channel = bot.get_channel(723841454778351668)
	cursor.execute("""
		INSERT INTO info VALUES (?,?,?)
	""",(member.id,member.name,0,))
	db.commit()
	db.close()
	await channel.send(embed=card)

@bot.command()
async def verify(ctx,member:discord.Member=None):
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
	await member.ban(reason=reason,delete_message_days=0)
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
    	
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRole):
    	await ctx.send(f"You are missing **{error.missing_role}** role meow!")
    elif isinstance(error,commands.MissingAnyRole):
    	await ctx.send(f"You are missing **{','.join(error.missing_roles)}** meow!")
    elif isinstance(error, commands.CheckFailure):
    	await ctx.send(f"🚫You cannot use command on this channel!🚫")
    else:
    	raise error
    
bot.run(TOKEN)