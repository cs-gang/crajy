import discord
from discord.ext import commands

#Control Cog, for loading and unloading cogs.
#Only bot owners can use these commands.

class Control(commands.Cog, command_attrs={'hidden': True}):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="load")
    async def load(self, ctx, cog):
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded **{cog}**")

    @commands.command(name="unload")
    async def unload(self, ctx, cog):
        self.bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Unloaded **{cog}**")

def setup(bot):
    bot.add_cog(Control(bot))