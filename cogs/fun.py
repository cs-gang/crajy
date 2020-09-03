import discord
from discord.ext import commands
from crajy.cogs.api_details import *
import typing

class fun(commands.Cog):
    """Commands to make your chat more fun!"""
    def __init__(self, bot):
        self.bot = bot

    #text based commands
    @commands.command(name="fancy",
                      aliases=["f"],
                      help="Returns a ƒαη¢у version of your text",
                      brief="ƒαη¢у-fies given text")
    async def fancy(self, ctx, *, message):
        querystring = {"text": message}
        async with ctx.channel.typing():
            async with self.bot.Session.get(FANCY[0], headers=FANCY[1], params=querystring) as response:
                return_text = await response.json()
                return_text = return_text["fancytext"].split(",")[0]
            await ctx.send(return_text)

    @commands.command(name="mock",
                      aliases=["m"],
                      help="dOeS tHiS tO yOuR tExT.",
                      brief="oKaY kArEn")
    async def mock(self, ctx, *, message):
        out = ""
        curr_func = "lower"
        for i in message:
            if curr_func == "lower":
                out += i.lower()
                curr_func = "upper"
            else:
                out += i.upper()
                curr_func = "lower"
        await ctx.send(out)

    @commands.command(name="uwu",
                      aliases=["owo"],
                      help="Wetuwns a owo-ified vewsion of youw text.",
                      brief="uwu")
    async def owo(self, ctx, *, message):
        out = ""
        for i in message:
            case = "upper" if i.isupper() else "lower"
            if i.lower() in ["l", "r"]:
                out += "w" if case == "lower" else "W"
            else:
                out += i
        await ctx.send(out)

    @commands.command(name="emojify",
                      aliases=["e"],
                      help="Returns your text, but completely turned into the corresponding emojis. Only works on alphabets.",
                      brief="🇹 🇭 🇮 🇸")
    async def emojify(self, ctx, *, message):
        emojis = {'a':'🇦', 'b': '🇧', 'c':'🇨', 'd':'🇩', 'e':'🇪', 'f': '🇫', 'g': '🇬', 'h':'🇭', 'i': '🇮', 'j':'🇯', 'k':'🇰', 'l':'🇱', 'm':'🇲', 'n':'🇳', 'o':'🇴', 'p':'🇵', 'q':'🇶', 'r':'🇷', 's':'🇸', 't':'🇹', 'u':'🇺', 'v':'🇻', 'w':'🇼', 'x':'🇽', 'y':'🇾', 'z':'🇿'}
        out = ""
        for letter in message.lower():
            if letter.isalpha():
                out += f"{emojis[letter]} "
            else:
                out += letter
        await ctx.send(out)

    @commands.command(name="love-calc",
                      aliases=["lc", "love", "lovecalc"],
                      help="Calculate your compatibility with another person! The command can work for two people, or if the second person isn't specified, it will be set to you. (These answers are brought from an API)",
                      brief="Calculate your compatibility with another person!",
                      usage="<person> <person>")
    async def love_calc(self, ctx, second: typing.Union[str, discord.Member], first: typing.Union[str, discord.Member]=None):
        if first is None:
            first = ctx.author
            querystring = {"fname": first.name, "sname": second}
        else:
            querystring = {"fname": str(first), "sname": str(second)}
        async with ctx.channel.typing():
            async with self.bot.Session.get(LOVE_CALC[0], headers=LOVE_CALC[1], params=querystring) as response:
                percent = await response.json()
                percent = percent["percentage"]
                result = await response.json()
                result = result["result"]
            if int(percent) >= 50:
                embed = discord.Embed(title="Love Calculator", description=f"{first} and {second} 💕",colour=discord.Color.green())
                embed.add_field(name="That poor person", value=second, inline=False)
                embed.add_field(name="Percent", value=percent, inline=True)
                embed.add_field(name="Result", value=result, inline=False)
            else:
                embed = discord.Embed(title="Love Calculator", description=f"{first} and {second} 😔",colour=discord.Color.red())
                embed.add_field(name="Percent", value=percent, inline=True)
                embed.add_field(name="Result", value=result, inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.message.channel.send(content=None, embed=embed)



    #Tag commands
    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, tag):
        if ctx.invoked_subcommand is None:
            value = await self.bot.postgres.fetchval("SELECT value FROM guilds_tags WHERE guild_id=$1 and tag=$2", ctx.guild.id, tag)
            return await ctx.send(value)

    @tag.command(name="add",
                 aliases=["-a", "create"],
                 usage="<tag> <output>",
                 help="Used to create a tag.")
    async def add_tag(self, ctx, tag, *, output):
        print("inside add")
        await self.bot.postgres.execute(f"INSERT INTO guilds_tags (guild_id, tag, value, created_by) VALUES($1, $2, $3, $4)", ctx.guild.id, tag, output, ctx.author.id)
        await ctx.send("Added")

    @tag.command(name="remove",
                 aliases=["-r", "delete"],
                 usage="<tag>",
                 help="Used to remove a tag. You must be an administrator or must've created the tag to use this.")
    async def remove_tag(self, ctx, tag):
        if ctx.author.guild_permissions.administrator:
            print("is admin")
            await self.bot.postgres.execute("DELETE FROM guilds_tags WHERE guild_id=$1 and tag=$2", ctx.guild.id, tag)
        else:
            print("not admin")
            await self.bot.postgres.execute("DELETE FROM guilds_tags WHERE guild_id=$1 and tag=$2 and created_by=$3", ctx.guild.id, tag, ctx.author.id)
        await ctx.send(f"Removed *{tag}*")

    @tag.command(name="edit-output",
                 usage="<tag> <new output>",
                 help="Used to edit the output of a tag. You must be an administrator or must've created the tag to use this.")
    async def edit_tag_output(self, ctx, tag, *, new_output):
        if ctx.author.guild_permissions.administrator:
            print("is admin")
            await self.bot.postgres.execute("UPDATE guilds_tags SET value=$1 WHERE tag=$2 and guild_id=$3", new_output, tag, ctx.guild.id)
        else:
            print("not admin")
            await self.bot.postgres.execute("UPDATE guilds_tags SET value=$1 WHERE tag=$2 and guild_id=$3 and created_by=$4",new_output, tag, ctx.guild.id, ctx.author.id)
            
        await ctx.send(f"Tag *{tag}* edited.")

    @tag.command(name="edit-tag",
                 usage="<tag> <new tag>",
                 help="Used to edit a tag itself. Enclose the tag (the original tag) in quotes if it has spaces. You must be an administrator or must've created the tag to use this.")
    async def edit_tag(self, ctx, tag, *, new_tag):
        if ctx.author.guild_permissions.administrator:
            print("is admin")
            await self.bot.postgres.execute("UPDATE guilds_tags SET tag=$1 WHERE tag=$2 and guild_id=$3", new_tag, tag, ctx.guild.id)
        else:
            print("not admin")
            await self.bot.postgres.execute(
                "UPDATE guilds_tags SET value=$1 WHERE tag=$2 and guild_id=$3 and created_by=$4", new_tag, tag, ctx.guild.id, ctx.author.id)

        await ctx.send(f"Tag *{tag}* edited.")

    @tag.command(name="search",
                 usage="<tag>",
                 help="Returns all tags which contains the searched word.")
    @commands.guild_only()
    async def tag_search(self, ctx, *, tag):
        data = await self.bot.postgres.fetch("SELECT tag, value FROM guilds_tags WHERE tag::varchar LIKE '%$1%' AND guild_id = $2", tag, ctx.guild.id)
        print(data)











def setup(bot):
    bot.add_cog(fun(bot))