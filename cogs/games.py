import discord
from discord.ext import commands
from ..utils import tictactoe
import random
import asyncio
import datetime


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

        else:
            raise error

    @commands.command(name="guess",
                      help="Start a word guessing game! Pick a word (within 30 seconds) that the rest of the users have to guess within a minute.")
    @commands.cooldown(1, 90, commands.BucketType.channel)
    @commands.guild_only()
    async def guess(self, ctx):
        #checks
        def reply_check(m):
            return m.author == ctx.author and m.guild is None

        def answer_check(m):
            return m.author != ctx.author and m.content.lower() == answer.content.lower() and m.channel == ctx.channel

        start_embed = discord.Embed(title="Guess Game!", description=f"{ctx.author.nick} has started a guess game.\n{ctx.author.mention}, check your DMs!",
                                    color=discord.Color.blurple(),
                                    timestamp=datetime.datetime.utcnow())
        start_embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=start_embed)

        # getting answer and clue from the user
        await ctx.author.send("Send the word that everyone has to guess!\n You have 30 seconds to pick a word.")
        answer = await self.bot.wait_for('message', check=reply_check, timeout=30)
        await ctx.author.send("Send a clue for your word!")
        clue = await self.bot.wait_for('message', check=reply_check, timeout=30)

        clue_embed = discord.Embed(title=f"{ctx.author.nick}'s Guess Game",
                                   description=f"{ctx.author.nick} has picked a word!\n\n **Clue** - {clue.content}",
                                   color=discord.Color.orange())
        clue_embed.set_thumbnail(url=r"https://media.discordapp.net/attachments/612638234782072882/754767088564043936/emoji.png?width=58&height=58")
        clue_embed.set_footer(text="You have 1 minute to guess the word!")
        await ctx.send(embed=clue_embed)

        # checking answers in chat
        try:
            user_reply = await self.bot.wait_for('message', check=answer_check, timeout=60)
        except asyncio.TimeoutError:
            end_embed = discord.Embed(title=f"{ctx.author.nick}'s Guess Game - Results",
                                      description=f"No one guessed it right.\n The word was **{answer.content}**",
                                      color=discord.Color.red())
            end_embed.set_thumbnail(url=r"https://images-ext-1.discordapp.net/external/hxIgrBXtxX2LFYYH_SXtMSP1Zrc9G16hfYBUTIMxjsA/%3Fwidth%3D418%26height%3D366/https/media.discordapp.net/attachments/612638234782072882/743805186702835742/sadcowboy-removebg-preview.png?width=274&height=240")
            return await ctx.send(embed=end_embed)

        end_embed = discord.Embed(title=f"{ctx.author.nick}'s Guess Game - Results",
                                  description=f"{user_reply.author.mention} guessed it right! The word was **{answer.content}**",
                                  color=discord.Color.green(),
                                  url=user_reply.jump_url)
        end_embed.set_thumbnail(url=user_reply.author.avatar_url)
        return await ctx.send(embed=end_embed)

    @guess.error
    async def guess_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send("A guess game is already going on in this channel. Please wait for it to end first.")

        raise error


def setup(bot):
    bot.add_cog(games(bot))
