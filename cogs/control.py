import discord
from discord.ext import commands

#Control Cog, for loading and unloading cogs.
#Only bot owners can use these commands.

class Control(commands.Cog, command_attrs={'hidden': True}):
    """Direct control of the bot- this cog is for the bot owner only. How did you find this? """
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

    @commands.group(name="fetch")
    async def fetch_group(self, ctx):
        if ctx.invoked_subcommand is None: return await ctx.send("Invalid command")

    @fetch_group.command(name="user")
    async def fetch_user(self, ctx, user: int):
        user = await self.bot.fetch_user(user)
        embed = discord.Embed(title=user.name)
        embed.add_field(name="Username", value=str(user))
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Control(bot))