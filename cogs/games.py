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
        players = {tictactoe.X: ctx.author, tictactoe.O: opponent}

        original_message_embed = discord.Embed(title="TicTacToe Game!",
                                               description=f"{ctx.author.mention} has challenged {opponent.mention}!",
                                               timestamp=datetime.datetime.utcnow())
        original_message_embed.set_thumbnail(url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
        original_message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        original_message_embed.set_footer(text=opponent.display_name, icon_url=opponent.avatar_url)
        original_message = await ctx.send(embed=original_message_embed)

        top_row_message = await ctx.send(content="*top row*")
        for i in ["↖", "⬆", "↗"]:
            await top_row_message.add_reaction(i)

        middle_row_message = await ctx.send(content="*middle row*")
        for i in ["⬅", "⏺", "➡"]:
            await middle_row_message.add_reaction(i)

        bottom_row_message = await ctx.send(content="*bottom row*")
        for i in["↙", "⬇", "↘"]:
            await bottom_row_message.add_reaction(i)

        def player1_check(m):
            if m.author == ctx.message.author and len(m.content.split()) == 2:
                try:
                    [int(i) for i in m.content.split()]
                except ValueError:
                    return False
                return True

        def player2_check(m):
            if m.author == opponent and len(m.content.split()) == 2:
                try:
                    [int(i) for i in m.content.split()]
                except ValueError:
                    return False
                return True

        '''while not tictactoe.terminal(board):
            if tictactoe.player(board, start) == tictactoe.X:



                out = tictactoe.board_converter(board)
                await original_message.edit(content=out)
            elif tictactoe.player(board, start) == tictactoe.O:

                out = tictactoe.board_converter(board)
                await original_message.edit(content=out)
        else:
            win_person = players[tictactoe.winner(board)]
            await ctx.send(f"game over, winner is {tictactoe.winner(board)}")'''

    pass


def setup(bot):
    bot.add_cog(games(bot))