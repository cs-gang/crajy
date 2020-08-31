import discord
from discord.ext import commands

import asyncpg
from aiohttp import ClientSession

import datetime      #remove later maybe?
import dotenv
import os

from crajy.utils.help_class import HelpCommand

dotenv.load_dotenv(dotenv.find_dotenv())
TOKEN = os.environ.get("TOKEN")

async def get_prefix(bot, message):
    return await bot.postgres.fetchval(f'SELECT prefix FROM prefixes WHERE guild_id={message.guild.id}')


bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive=True,
                   help_command=HelpCommand(),
                   activity=discord.Activity(type=discord.ActivityType.playing, name="in development"),
                   owner_id=int(os.environ.get("OWNER_ID")))


async def create_database_connection():
    bot.postgres = await asyncpg.create_pool(os.environ.get("POSTGRES_BOT"))
    bot.postgres_guilds = await asyncpg.create_pool(os.environ.get("POSTGRES_GUILDS"))

@bot.event
async def on_ready():
    bot.Session = ClientSession()
    print(f"Bot running: {datetime.datetime.now()}\n ClientSession made")

@bot.event
async def on_message(message):
    if '<@!749140007729627138>' in message.content:
        prefix = await get_prefix(bot, message)
        return await message.channel.send(f"Hi, {message.author.mention}! My commands begin with `{prefix}`\nTry the `help` command if you're confused!")
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    #setting default prefix in utils
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


#loading cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except commands.NoEntryPointError:
            pass

bot.loop.run_until_complete(create_database_connection())
bot.run(TOKEN)
