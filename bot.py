# sleepy.exe AKA birb.cc discord bot.
# Fully coded in python.
# Using discord.py recode. (Google for documentation. Will add to the read me at some point.)
# Not the most efficiant code ever, but it works.
#
# Coded by sleepy#7888 & Zankuro#9999


import discord
import random
import os
import datetime
import requests
import json
import sys
from discord.ext import commands, tasks
from itertools import cycle
from ruamel.yaml import YAML

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Start up and prefix
bot = commands.Bot(command_prefix = get_prefix)

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

status = cycle(['with my balls',
                "with sleepy's balls",  #
                "with Jordan's balls",  # Nice gay trio...
                "with Cadan's balls",   #
                'with thigh.life',
                'with birb.cc',
                'with Hentaiware.moe',
                'with Hentaihook'])

# Init
@bot.event
async def on_ready():
    change_status.start()
    print('>> Bot is initalized')
    print('>> We have logged in as {0.user}'.format(bot))

# Status Loop
@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '>'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    embed = discord.Embed(colour=0x95efcc, description=f"Prefix set to {prefix}")
    embed.set_author(name="Set Prefix")
    embed.set_footer(text="birb.cc")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@setprefix.error
async def setprefixerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=0x95efcc, description="Please specify a prefix. \n\nUsage: ,setprefix [prefix]")
        embed.set_author(name=">> Error")
        embed.set_footer(text="birb.cc")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


# Checks latency
@bot.command()
async def ping(ctx):
    embed = discord.Embed(colour=0x95efcc, description=f"Pong! {round(bot.latency * 1000)}ms.")
    embed.set_author(name="Latency")
    embed.set_footer(text="birb.cc")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

# Scans for members joining the server
# @bot.event
# async def on_member_join(member):
#    print(f'{member} has joined a server. Welcome!')

# Scans for members leaving the server
# @bot.event
# async def on_member_remove(member):
#    print(f'{member} has left a server. Goodbye!'

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


yaml = YAML()
cfg = yaml.load(open("cfg.yaml", "r"))
token = cfg["Bot"]["Token"]

if isinstance(token, str):
    bot.run(token)
else:
    print("Invalid token")
    exit()
