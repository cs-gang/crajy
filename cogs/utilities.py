import discord
from discord.ext import commands
import asyncpg
from disputils import BotEmbedPaginator

class utilities(commands.Cog):
    """Commands related to the bot itself, and other utilities."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="change-prefix",
                      aliases=["change_prefix", "changeprefix"],
                      help="Change the server-wide prefix for the bot. The bot will only respond to commands starting with the new prefix. This new prefix can be at most 3 characters long.",
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

    @commands.command(name="ping",
                      aliases=["pong"],
                      help="Returns the ping of the bot.")
    async def ping(self, ctx):
        embed = discord.Embed(title="Ping", description=f"{self.bot.latency*1000}ms")
        await ctx.send(embed=embed)

    @commands.command(name="pin",
                      help="Add the message to pinned messages. If the channel cannot add any more pins (due to the 50 pins per channel limit), the bot will save it in the database, and can be retrieved using the `pins` command.")
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, message_id: discord.Message=None):
        if message_id is None:
            channel_history = await ctx.channel.history(limit=3).flatten()
            message_id = channel_history[1]

        await self.bot.postgres.execute("INSERT INTO pins VALUES($1, $2, $3)", ctx.guild.id, message_id.id, message_id.jump_url)
        try:
            await message_id.pin()
        except discord.HTTPException:
            await ctx.send(f"{ctx.channel.mention} already has over 50 pinned messages, so you can't pin anymore. The message has been pinned in the bot database though, and you can display them using `pins` command.")

        return await ctx.message.add_reaction("✅")

    @commands.command(name="pins",
                      help="A list of pinned messages. These do NOT include the messages pinned in the discord channel itself, only the ones saved in our database. Instead, if your channel already has over 50 pins, using the `pin` command adds the message to the bot database.")
    async def pins(self, ctx):
        data = await self.bot.postgres.fetch("SELECT ")



def setup(bot):
    bot.add_cog(utilities(bot))