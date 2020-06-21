import discord
from discord.ext import commands
import sqlite3
import os,random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix=["!","?"])

initial_extension = ["event","info","moderator"]

for extension in initial_extension:
	bot.load_extension(extension)

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
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRole):
    	await ctx.send(f"You are missing **{error.missing_role}** role meow!😼")
    elif isinstance(error,commands.MissingAnyRole):
    	await ctx.send(f"You are missing **{' , '.join(error.missing_roles)}** roles meow!😼")
    elif isinstance(error, commands.CheckFailure):
    	await ctx.send(f"🚫You cannot use command on this channel!🚫")
    else:
    	raise error
    
bot.run(TOKEN)