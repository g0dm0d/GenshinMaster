import discord
from discord import message
from discord import player
from discord.ext import commands
import asyncio
import genshinstats as gs
import time
from prettytable import *

#async def resin():
#    gs.set_cookie(ltuid= 126239591, ltoken ="y3sTjYmk68fnL7xVwOukbn1jiqzw0RKgJT1t6w84")
#    uid=717884374
#    #706382070
#    notes = gs.get_notes(uid)
#    print(f"Current resin: {notes['resin']}/{notes['max_resin']}")
#asyncio.run(resin())

ltuid=126239591
ltoken="y3sTjYmk68fnL7xVwOukbn1jiqzw0RKgJT1t6w84"

client = commands.Bot(command_prefix = '.')
@client.command()
async def resin(ctx):
    gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
    uid=717884374
    notes = gs.get_notes(uid)
    await ctx.channel.send(f"Current resin: {notes['resin']}/{notes['max_resin']}")
@client.command()
async def characters(ctx, *, uid):
    gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
    characters = gs.get_characters(uid)
    characters_list = PrettyTable()
    characters_list.field_names=(['rarity','name','lvl','const'])
    for char in characters:
        rarity = char['rarity']
        name = char['name']
        level = char['level']
        const = char['constellation']
        #print(f"{char['rarity']}* {char['name']:10} | lvl {char['level']:2} C{char['constellation']}")
        #characters_list.append(f'["{rarity}", "{name}", "{level}", "{const}"]')
        characters_list.add_row([rarity,name,level,const])
    await ctx.channel.send('`' + str(characters_list) + '`')
@client.command()
async def stats(ctx, *, uid):
    gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
    stats = gs.get_user_stats(uid)['stats']
    player_stats = PrettyTable()
    player_stats.field_names=(['stats user:', uid])
    for field, value in stats.items():
        #print(f"{field}: {value}")
        player_stats.add_row([field,value])
    await ctx.channel.send('`' + str(player_stats) + '`')
client.run('ODQzMDUxOTI5MTE3NjU1MDUx.YJ-PSw.FB0XcGwkWj9VWaAkMpSIQxxOXws')