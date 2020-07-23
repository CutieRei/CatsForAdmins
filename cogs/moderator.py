import discord
import sqlite3

from discord.ext import commands


def setup(bot):
    bot.add_cog(moderator(bot))


class moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["hammer", "poop"])
    @commands.has_role(723112492988891156)
    async def ban(self, ctx, member: discord.Member, reason="Undefined"):
        await member.ban(reason=reason, delete_message_days=0)
        card = discord.Embed(
            colour=ctx.author.color,
            title=f"Haha now go meow!",
            description=f"{ctx.author.name} has banned {member.name}, Reason: {reason}"
        )
        await ctx.send(embed=card)

    @commands.command(aliases=["bite", "stroke"])
    @commands.has_role(723112492988891156)
    async def strike(self, ctx, member: discord.Member, strike=1):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM info WHERE id = ?", (member.id,))
        db.commit()
        user = cursor.fetchone()
        print(user)
        if user[0] == ctx.author.id:
            await ctx.send("You cant strike yourself lol")
            db.close()
        else:
            userStrike = user[2] + strike
            cursor.execute(f"""
UPDATE info
SET strike = {userStrike}
WHERE name = {member.name}
""")
            db.commit()
            db.close()
            card = discord.Embed(
                colour=discord.Colour.from_rgb(255, 20, 20),
                title=f"{member.name} has been given {strike} strikes by {ctx.author.name}"
            )
            await ctx.send(embed=card)

    @commands.command()
    @commands.has_role(723112492988891156)
    async def clear(self, ctx, msg: int):
        channel = ctx.channel
        deleted = await channel.purge(limit=msg)
        card = discord.Embed(
            colour=discord.Colour.from_rgb(20, 255, 20),
            title=f"Deleted {len(deleted)} messages"
        )
        await ctx.send(embed=card, delete_after=4)

    @commands.command()
    @commands.is_owner()
    async def dc(self, ctx):
        if ctx.author.id == 716503311402008577:
            card = discord.Embed(
                colour=discord.Colour.from_rgb(20, 255, 20),
                title="Successfully disconnected meow!"
            )
            await ctx.send(embed=card)
            await self.bot.logout()
        else:
            await ctx.send("You are not the bot owner meow!")
