from discord.ext import commands
from crajy.cogs.api_details import *

class Fun(commands.Cog):
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
                      help="Returns you're text, but completely turned into the corresponding emojis. Only works on alphabets.",
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

    #Love Calculator


def setup(bot):
    bot.add_cog(Fun(bot))