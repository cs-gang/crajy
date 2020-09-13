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

    @commands.command(name="reload")
    async def reload(self, ctx, cog):
        self.bot.unload_extension(f"cogs.{cog}")
        self.bot.load_extension(f"cogs.{cog}")
        return await ctx.send(f"Reloaded cog ``{cog}``")

    @commands.group(name="fetch")
    async def fetch_group(self, ctx):
        if ctx.invoked_subcommand is None: return await ctx.send("Invalid command")

    @fetch_group.command(name="user")
    async def fetch_user(self, ctx, user: int):
        user = await self.bot.fetch_user(user)
        embed = discord.Embed(title=user.name)
        embed.add_field(name="Username", value=str(user))
        return await ctx.send(embed=embed)

    @commands.group(name="global-tag",
                    aliases=["gt"])
    async def global_tags(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send("Invalid sub-command.")

    @global_tags.command(name="add")
    async def add_global_tag(self, ctx, tag, *, value):
        await self.bot.postgres.execute("INSERT INTO global_tags VALUES($1, $2, $3)", tag, value, ctx.author.id)
        return await ctx.send("Added to global tags database. This tag can now be used in every server in which Crajy is in.")

    @global_tags.command(name="remove")
    async def remove_global_tag(self, ctx, tag):
        await self.bot.postgres.execute("DELETE FROM global_tags WHERE tag=$1", tag)
        return await ctx.send(f"Removed tag _{tag}_ from global tags database.")

def setup(bot):
    bot.add_cog(Control(bot))
