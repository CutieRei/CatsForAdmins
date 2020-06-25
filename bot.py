import discord
from discord.ext import commands
import sqlite3
import os,random,datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix=["!","?"])
bot.remove_command("help")

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
	cursor.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER,exp INTEGER,level INTEGER)")
	db.commit()
	
	db.close()

@bot.check
def custom_check(ctx):
	if "Mod" in [i.name for i in ctx.author.roles] or "Reyter" in [i.name for i in ctx.author.roles] and ctx.channel.name not in ["bot-1","bot-2"]:
		return True
	elif "Mod" not in [i.name for i in ctx.author.roles] and ctx.channel.name not in ["bot-1","bot-2"]:
		return False
	else:
		return True

@bot.command()
async def help(ctx):
	card = discord.Embed(
	title="**Help**",
	colour=discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
	)
	card.add_field(name="ℹ️-Info\n",value="--**verify** [member] -Verify yourself or verify someone else(Mod only)\n\n",inline=False)
	card.add_field(name="😎-Moderator\n",value="**--[strike|stroke|bite]** [amount=1] -Give strikes to a member\n\n**--[ban|hammer|poop]** <member> -Ban a member\n\n--**dc** -Disconnect the bot(Reyter only)\n\n--**clear** <amount> -Clear the message of the current channel",inline=False)
	times = datetime.datetime.now()
	today = str(times.hour)+":"+str(times.minute)
	card.set_footer(text=f"Prototype help commands, prefix = \"{' , '.join(bot.command_prefix)}\" |Today at {today}")
	await ctx.send(embed=card)
	
    	
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