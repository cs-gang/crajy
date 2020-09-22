import discord
from discord.ext import commands
import tictactoe
import random
import datetime
import asyncpg

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tictactoe", 
                      aliases=["ttt"],
                      help="Play tictactoe with another person!",
                      brief="Play tictactoe with another person!",
                      usage="<person>")

    async def ttt(self, ctx, opponent: discord.Member = None):
        #if opponent == ctx.message.author:
            #return await ctx.send("you moron, trying to play with yourself.")
        out = ""
        board = tictactoe.initial_state()
        start = random.choice([tictactoe.X, tictactoe.O])
        players = {tuple(tictactoe.X): ctx.author, tuple(tictactoe.O): opponent} #check cause of error because tuple() is unnecesary

        main_message_embed = discord.Embed(title="TicTacToe Game!",
                                            description=f"{ctx.author.mention} has challenged {opponent.mention}!\n {players[tuple(start)]} makes the first move.",
                                            timestamp=datetime.datetime.utcnow())
        main_message_embed.set_thumbnail(url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
        main_message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        main_message_embed.set_footer(text=opponent.display_name, icon_url=opponent.avatar_url)
        main_message = await ctx.send(embed=main_message_embed)
        main_message_embed.set_thumbnail(url=discord.Embed.Empty)

        top_row_message = await ctx.send(content="*top row*")
        for i in ["↖", "⬆", "↗"]:
            await top_row_message.add_reaction(i)

        middle_row_message = await ctx.send(content="*middle row*")
        for i in ["⬅", "⏺", "➡"]:
            await middle_row_message.add_reaction(i)

        bottom_row_message = await ctx.send(content="*bottom row*")
        for i in["↙", "⬇", "↘"]:
            await bottom_row_message.add_reaction(i)

        def player_check(reaction, user):
            print(str(reaction.emoji))
            if str(reaction.emoji) in ["↖", "⬆", "↗", "⬅", "⏺", "➡", "↙", "⬇", "↘"] and user == players[start]:
                return True
            return False

        while not tictactoe.terminal(board):
            reaction, _ = await self.bot.wait_for("reaction_add", check=player_check)

            if reaction:
                print(reaction)
                main_message_embed = tictactoe.update_board(main_message_embed, reaction.emoji, start)
                print(main_message_embed.description)
                await main_message.edit(embed=main_message_embed)







def setup(bot):
    bot.add_cog(games(bot))