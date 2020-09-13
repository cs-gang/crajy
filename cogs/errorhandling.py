import discord
from discord.ext import commands
import asyncio

import asyncpg

from crajy.utils.help_class import HelpCommand


class ErrorHandler(commands.Cog, command_attrs={'hidden': True}):
    """Handling errors that occur during command execution."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            error = getattr(error, 'original', error)

            if hasattr(ctx.command, 'on_error'):
                return
            embed = discord.Embed(title="Command Error", color=discord.Color.red())

            if isinstance(error, asyncpg.exceptions.StringDataRightTruncationError):
                embed.description = "The value you inputted was too long."
                return await ctx.send(embed=embed)
            elif isinstance(error, asyncio.TimeoutError):
                embed.description = "You took too long to respond. The command has timed out."
                return await ctx.send(embed=embed)

            elif isinstance(error, asyncpg.exceptions.UniqueViolationError):
                embed.description = "The tag you're trying to create already exists."
                return await ctx.send(embed=embed)

            elif isinstance(error, commands.MissingRole):
                embed.description = f"You are missing the following necessary roles to use this command - `{error.missing_role}`"
                return await ctx.send(embed=embed)

            elif isinstance(error, commands.MissingPermissions):
                embed.description = f"You are missing the following necessary permissions to use this command - `{error.missing_perms}`"
                return await ctx.send(embed=embed)

            elif isinstance(error, commands.CheckFailure):
                embed.description = f"Restricted command!"
                return await ctx.send(embed=embed)

            elif isinstance(error, commands.MissingRequiredArgument):
                embed.description = f"`{error.param}` is a necessary argument. \n Command Usage - `{HelpCommand.get_clean_usage_signature(ctx.command)}`"
                embed.set_footer(text="Try the help command for more info")
                return await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Unexpected Error", description=str(error), color=discord.Color.red())
                embed.set_footer(text="Think this is a mistake? Report it at our help server.")
                await ctx.send(embed=embed)
                raise error


def setup(bot):
    return bot.add_cog(ErrorHandler(bot))
