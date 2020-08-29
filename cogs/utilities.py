import discord
from discord.ext import commands
import asyncpg

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="change-prefix",
                      aliases=["change_prefix", "changeprefix"],
                      help="Change the server-wide prefix for the bot. The bot will only respond to commands starting with the new prefix",
                      brief="Change the server-wide prefix for the bot.",
                      )
    @commands.has_guild_permissions(administrator=True)
    async def change_prefix(self, ctx, new_prefix):
        current_prefix = await self.bot.postgres.fetchval(f'SELECT prefix FROM prefixes WHERE guild_id={ctx.guild.id}')
        if new_prefix == current_prefix:
            return await ctx.send(f'`{new_prefix}` _is_ the prefix right now.')
        else:
            await self.bot.postgres.execute(f"UPDATE prefixes SET prefix='{new_prefix}' WHERE guild_id={ctx.guild.id}")
            embed = discord.Embed(title='Success', description=f'Server-wide prefix changed to {new_prefix}',
                                  color=discord.Color.green())
            embed.set_footer(text=f'Requested by {ctx.author.name}')
            return await ctx.send(embed=embed)

    @commands.command(name="invite",
                      aliases=["inv"],
                      help="Returns an OAuth link to invite Crajy to your servers!",
                      brief="Link to invite Crajy to your servers."
                      )
    async def invite(self, ctx):
        permissions = discord.Permissions(read_messages=True,
                                         send_messages=True,
                                         manage_messages=True,
                                         embed_links=True,
                                         read_message_history=True,
                                         external_emojis=True,
                                         manage_nicknames=True,
                                         add_reactions=True)
        url = discord.utils.oauth_url(client_id=749140007729627138, permissions=permissions)
        embed = discord.Embed(title="Invite Crajy to your server!", url=url, color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_author(name=str(ctx.author))
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))