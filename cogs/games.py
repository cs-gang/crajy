import discord
from discord.ext import commands
import tictactoe
import random
import asyncio
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
    @commands.cooldown(1, 30, type=commands.BucketType.channel)
    async def ttt(self, ctx, opponent: discord.Member = None):
        #if opponent == ctx.message.author:
            #return await ctx.send("you moron, trying to play with yourself.")

        board = tictactoe.initial_state()
        player = random.choice([tictactoe.X, tictactoe.O])
        next_player = tictactoe.X if player == tictactoe.O else tictactoe.O
        players = {tuple(tictactoe.X): ctx.author, tuple(tictactoe.O): opponent} #check cause of error because tuple() is unnecesary

        main_message_embed = discord.Embed(title="TicTacToe Game!",
                                            description=f"{ctx.author.mention} has challenged {opponent.mention}!\n {players[tuple(player)]} makes the first move.",
                                            timestamp=datetime.datetime.utcnow())
        main_message_embed.set_thumbnail(url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
        main_message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        main_message_embed.set_footer(text=opponent.display_name, icon_url=opponent.avatar_url)
        main_message_embed.color = discord.Color.blue()
        main_message = await ctx.send(embed=main_message_embed)
        main_message_embed.set_thumbnail(url=discord.Embed.Empty)

        top_row_message = await ctx.send("*top row*")
        for i in ["↖", "⬆", "↗"]:
            await top_row_message.add_reaction(i)

        middle_row_message = await ctx.send(content="*middle row*")
        for i in ["⬅", "⏺", "➡"]:
            await middle_row_message.add_reaction(i)

        bottom_row_message = await ctx.send(content="*bottom row*")
        for i in["↙", "⬇", "↘"]:
            await bottom_row_message.add_reaction(i)

        def player_check(reaction, user):
            if str(reaction.emoji) in ["↖", "⬆", "↗", "⬅", "⏺", "➡", "↙", "⬇", "↘"] and user == players[player]:
                return True

            return False

        while not tictactoe.terminal(board):
            reaction, _ = await self.bot.wait_for("reaction_add", check=player_check, timeout=10)
            message_of_reaction = reaction.message

            if reaction:
                main_message_embed.color = discord.Color.red()
                await message_of_reaction.clear_reaction(reaction.emoji)
                main_message_embed = tictactoe.update_board(main_message_embed, reaction.emoji, player)
                player, next_player = next_player, player
                main_message_embed.description += f"\n{players[player]}'s turn"  # maybe move to better place
                await main_message.edit(embed=main_message_embed)

        main_message_embed.description = f"{players[next_player]} destroyed {players[player]}!\n Good Game!"
        main_message_embed.color = discord.Color.green()
        await main_message.edit(embed=main_message_embed)

    @ttt.error
    async def ttt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message_embed = discord.Embed(title="TicTacToe Game!",
                                          description="There's an on going game, please wait for it to get over!",
                                          timestamp=datetime.datetime.utcnow())
            message_embed.set_thumbnail(
                url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
            message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            message_embed.color = discord.Color.red()
            return await ctx.send(embed=message_embed)

        elif isinstance(getattr(error, 'original'), asyncio.TimeoutError):
            message_embed = discord.Embed(title="TicTacToe Game!",
                                          description="The player did not play a move in time, the match is ended.",
                                          timestamp=datetime.datetime.utcnow())
            message_embed.set_thumbnail(
                url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
            message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            message_embed.color = discord.Color.red()
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=message_embed)







def setup(bot):
    bot.add_cog(games(bot))