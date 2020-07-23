import discord
import sqlite3
from discord.ext import commands


def setup(bot):
    bot.add_cog(info(bot))


class info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx, member: discord.Member):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        if member and "Mod" in [i.name for i in ctx.author.roles] or 716503311402008577 == ctx.author.id:
            cursor.execute(f"SELECT * FROM info WHERE id = {member.id}")
            db.commit()
            user = cursor.fetchone()
            if user:
                await ctx.send("That member is verified!")
            else:
                cursor.execute(f"INSERT INTO info VALUES({member.id}, {member.name}, {0})")
                db.commit()
                db.close()
                await ctx.send(f"> Verified {member.name}!")
                db.close()
        else:
            cursor.execute(f"SELECT * FROM info WHERE id = {ctx.author.id}")
            db.commit()
            user = cursor.fetchone()
            if user:
                await ctx.send("You already verified!")
            else:
                cursor.execute(f"INSERT INTO info VALUES({ctx.author.id}, {ctx.author.name}, {0})")
                db.commit()
                db.close()
                await ctx.send(f"> {ctx.author.name} you are verified!")
                db.close()

    @commands.command()
    @commands.has_role(723112492988891156)
    async def check(self, ctx, member: discord.Member):
        db = sqlite3.connect("data.db")
        c = db.cursor()
        c.execute("SELECT * FROM info WHERE id = ?", (member.id,))
        user = c.fetchone()
        if user:
            await ctx.send(f"==Info==\nID: {user[0]}\nName: {user[1]}\nStrikes: {user[2]}")
        else:
            await ctx.send("Member not found!")
        db.close()
