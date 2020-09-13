import discord
from discord.ext import commands
import tictactoe
import random
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
        if opponent == ctx.message.author:
            return await ctx.send("you moron, trying to play with yourself.")
        out = ""
        board = tictactoe.initial_state()
        start = random.choice([tictactoe.X, tictactoe.O])
        players = {tictactoe.X: ctx.author, tictactoe.O: opponent}

        original_message = await ctx.send(
            content=f"**New Game of Tictactoe** \n {ctx.author.mention} X vs {opponent.mention} O \n {out} \n {start} starts! (make a move for the board to appear)")

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

        while not tictactoe.terminal(board):
            if tictactoe.player(board, start) == tictactoe.X:
                try:
                    reply = await self.bot.wait_for('message', check=player1_check)
                    if not tictactoe.valid_action(tuple([int(i) for i in reply.content.split()]), board):
                        raise IndexError
                    coords = [int(i) for i in reply.content.split()]
                    board[coords[0]][coords[1]] = tictactoe.X
                except IndexError:
                    await ctx.send(f"{tictactoe.player(board, start)}, you've tried an invalid move")

                out = tictactoe.board_converter(board)
                await original_message.edit(content=out)
            elif tictactoe.player(board, start) == tictactoe.O:
                try:
                    reply = await self.bot.wait_for('message', check=player2_check)
                    if not tictactoe.valid_action(tuple([int(i) for i in reply.content.split()]), board):
                        raise IndexError
                    coords = [int(i) for i in reply.content.split()]
                    board[coords[0]][coords[1]] = tictactoe.O
                except IndexError:
                    await ctx.send(f"{tictactoe.player(board, start)}, you've tried an invalid move")
                out = tictactoe.board_converter(board)
                await original_message.edit(content=out)
        else:
            win_person = players[tictactoe.winner(board)]
            await ctx.send(f"game over, winner is {tictactoe.winner(board)}")

    pass


def setup(bot):
    bot.add_cog(games(bot))