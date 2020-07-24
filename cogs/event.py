import random
import sqlite3

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(event(bot))


class event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)
        exp = random.randint(0, 5)
        db = sqlite3.connect("data.db")
        c = db.cursor()
        c.execute(f"SELECT * FROM data WHERE id = {message.author.id}")
        db.commit()
        user = c.fetchone()
        if message.author.id == 723390632709718056:
            pass
        elif user:
            exps = user[1] + exp
            levels = user[2]
            level = (exp + exps) // 100
            if level > levels:
                channel = message.channel
                await channel.send(f"{message.author.mention} Leveled up to level **{level}**")
            c.execute(f"UPDATE data SET exp = {exps}, level = {level} WHERE id = {message.author.id}")
            db.commit()
        else:
            c.execute(f"INSERT INTO data VALUES ({message.author.id}, {0}, {0})")
            db.commit()
        db.close()
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        welcomes = random.choice(
            [f"Hello {member.mention}, have fun here👋", f"Welcome {member.mention}, we hope you have fun here😄",
             f"Hello, friend {member.mention} have fun while in here😊"])
        card = discord.Embed(
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            title=f"Welcome {member.name}",
            description=welcomes
        )
        card.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        channel = self.bot.get_channel(723841454778351668)
        cursor.execute(f"INSERT INTO info VALUES ({member.id}, {member.name}, {0})")
        db.commit()
        db.close()
        await channel.send(embed=card)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        words = random.choice([f"Goodbye **{member.name}**, have a safe trip👋", f"So long **{member.name}**, bye👋",
                               f"Whats this? **{member.name}** is leaving?, bye bye **{member.name}**👋"])
        cursor.execute(f"SELECT * FROM info WHERE id = {member.id}")
        db.commit()
        user = cursor.fetchone()
        card = discord.Embed(
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            title=f"Goodbye {member.name}",
            description=words
        )
        card.set_thumbnail(url=member.avatar_url_as(static_format='png'))

        if user:
            cursor.execute(f"DELETE FROM info WHERE id = {member.id}")
            db.commit()
            channel = self.bot.get_channel(723841454778351668)
            await channel.send(embed=card)
            db.close()
        else:
            db.close()
