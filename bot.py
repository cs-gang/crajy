import os
import discord
from discord.ext import commands
import dotenv
import asyncpg
from aiohttp import ClientSession
import datetime      #remove later maybe?


dotenv.load_dotenv(dotenv.find_dotenv())
TOKEN = os.environ.get("TOKEN")

async def get_prefix(bot, message):
    return await bot.postgres.fetchval(f'SELECT prefix FROM prefixes WHERE guild_id={message.guild.id}')

bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive=True,
                   activity=discord.Activity(type=discord.ActivityType.playing, name="in development"),
                   owner_id=int(os.environ.get("OWNER_ID")))

bot.Session = ClientSession()

async def create_database_connection():
    bot.postgres = await asyncpg.create_pool(os.environ.get("POSTGRES"))

@bot.event
async def on_ready():
    print(f"Bot running: {datetime.datetime.now()}")

@bot.event
async def on_guild_join(guild):
    #setting default prefix in database
    await bot.postgres.execute(f'INSERT INTO prefixes VALUES ({guild.id})')
    channel = discord.utils.get(guild.channels, name="general")
    if channel is not None:
        text = "Thanks for adding me to your server.\n You can invoke my commands using the prefix `.`\nTry `.help` to learn more!"
        embed = discord.Embed(title="Hi!", description=text, color=discord.Color.green())
        await channel.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
    await bot.postgres.execute(f'DELETE FROM prefixes WHERE guild_id={guild.id}')
    #add more `remove` statements here for the other guild data that will be added
    #to be tested more.

@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, asyncpg.exceptions.StringDataRightTruncationError):
        embed = discord.Embed(title="Operation Failed", description="The value you inputted was too long", color=discord.Color.red())
        await ctx.send(embed=embed)




    else:
        embed = discord.Embed(title="Unexpected Error", description=str(error), color=discord.Color.red())
        embed.set_footer(text="Think this is a mistake? Report it at our help server.")
        await ctx.send(embed=embed)

#loading cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except commands.NoEntryPointError:
            pass

bot.loop.run_until_complete(create_database_connection())
bot.run(TOKEN)