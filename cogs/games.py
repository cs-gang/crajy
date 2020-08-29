import discord
from discord.ext import commands
import asyncpg

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pass


def setup(bot):
    bot.add_cog(Games(bot))