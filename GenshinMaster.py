from asyncio import events
from os import wait
import discord
from discord import message
from discord import player
from discord import channel
from discord.ext import commands
from discord import DMChannel
from discord_components import *
from discord_buttons_plugin import *
import asyncio
from discord_components.dpy_overrides import send_files, send_message
import genshinstats as gs
import time
from genshinstats.genshinstats import generate_cn_ds
from prettytable import *
import csv
import mysql
import mysql.connector
from mysql.connector import Error

SQLhost='localhost'
SQLuser='SA'
SQLpassword='password'
SQLdatabase='GenshinMaster'

ltuid=126239591
ltoken="y3sTjYmk68fnL7xVwOukbn1jiqzw0RKgJT1t6w84"

client = commands.Bot(command_prefix = '.')
DiscordComponents(client)
buttons = ButtonsClient(client)

#РЕГИСТРАЦИЯ___________________________________________________________________________
@client.command()
async def login(ctx):
    #await ctx.reply('https://media.discordapp.net/attachments/907163041852977194/908391673623629854/predlagau.gif')
    await ctx.reply('Укажите ltuid:')
    userid = ctx.author.id
    def check(q):
        return q.author.id == userid
    msg = await client.wait_for('message', check=check)
    ltuid = str(msg.content)

    await ctx.reply('Укажите ltoken:')
    userid = ctx.author.id
    def check(q):
        return q.author.id == userid
    msg = await client.wait_for('message', check=check)
    ltoken = str(msg.content)

    await ctx.reply('Укажите wish:')
    userid = ctx.author.id
    def check(q):
        return q.author.id == userid
    msg = await client.wait_for('message', check=check)
    wish = str(msg.content)

    #await ctx.reply('https://media.discordapp.net/attachments/907163041852977194/908392371690041385/sosage.gif')
    await ctx.reply('LOADING...')

    try:
        connection = mysql.connector.connect(
            host=SQLhost,
            user=SQLuser,
            password=SQLpassword,
            database=SQLdatabase
        )
        cursor = connection.cursor()
        try:
            sql = f'''INSERT INTO User (DiscordID, ltuid, ltoken, wish) VALUES ("{userid}", "{ltuid}", "{ltoken}", "{wish}")'''
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(f"The error '{e}' occurred")
    except Error as e:
        print(f"The error '{e}' occurred")

#СМОЛА___________________________________________________________________________
@client.command()
async def resin(ctx, *, uid):
    try:
        connection = mysql.connector.connect(
            host=SQLhost,
            user=SQLuser,
            password=SQLpassword,
            database=SQLdatabase
        )
        cursor = connection.cursor()
        userid = ctx.author.id
        cursor.execute("SELECT * FROM sud WHERE id='%s'" % (userid))
        rows = cursor.fetchall()
        for row in rows:
            ltuid = row[1]
            ltoken = row[2]
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
        notes = gs.get_notes(uid)
        await ctx.channel.send(f"Current resin: {notes['resin']}/{notes['max_resin']}")
    except Error as e:
        print(f"The error '{e}' occurred")

#ПЕРСЫ___________________________________________________________________________
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

#СТАТА___________________________________________________________________________
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

#БЕЗДНА___________________________________________________________________________
@client.command()
async def abyss(ctx, *, uid):
    gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
    spiral_abyss = gs.get_spiral_abyss(uid)
    stats = spiral_abyss['stats']
    abyss_stats = PrettyTable()
    abyss_stats.field_names=(['abyss user', str(uid)])
    for field, value in stats.items():
        abyss_stats.add_row([field, value])
    await ctx.channel.send('`' + str(abyss_stats) + '`')

#ЕЖЕДНЕВКА ФОРУМ___________________________________________________________________________
@client.command()
async def rewaind(ctx):
    try:
        connection = mysql.connector.connect(
            host=SQLhost,
            user=SQLuser,
            password=SQLpassword,
            database=SQLdatabase
        )
        cursor = connection.cursor()
        userid = ctx.author.id
        cursor.execute("SELECT * FROM User WHERE DiscordID='%s'" % (userid))
        rows = cursor.fetchall()
        for row in rows:
            ltuid = row[1]
            ltoken = row[2]
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
        reward = gs.claim_daily_reward()
        if reward is not None:
            await ctx.channel.send(f"Claimed daily reward - {reward['cnt']}x {reward['name']}")
        else:
            await ctx.channel.send("Could not claim daily reward")
    except Error as e:
        print(f"The error '{e}' occurred")

#WISH___________________________________________________________________________
@client.command()
async def wish(ctx):
    await ctx.send(content='TEXT', components = [Select(
                                    placeholder = 'Choose Banner',
                                    options = [
                                        SelectOption(label='Default Banner', value='default'),
                                        SelectOption(label='Character Event', value='CharacterEvent'),
                                        SelectOption(label='Weapon Event', value='WeaponEvent')
                                    ],
                                    custom_id='banners'
    )])
    #print(ctx.author.id)
    interaction = await client.wait_for('select_option', check=lambda i: i.custom_id == 'banners' and i.user == ctx.author)
    res = interaction.values[0]
    try:
        connection = mysql.connector.connect(
            host=SQLhost,
            user=SQLuser,
            password=SQLpassword,
            database=SQLdatabase
        )
        cursor = connection.cursor()
        userid = ctx.author.id
        print(userid)
        cursor.execute("SELECT * FROM User WHERE DiscordID='%s'" % (userid))
        rows = cursor.fetchall()
        for row in rows:
            authkey = row[3]
        print(authkey)
        wish_list = PrettyTable()
        wish_list.field_names=(['time','name','rarity','type'])
    except Error as e:
        print(f"The error '{e}' occurred")
    gs.set_authkey(authkey)

    if res == 'default':
        await interaction.send('Generate Table')
        for i in gs.get_wish_history(200):
            time = i['time']
            name = i['name']
            rarity = i['rarity']
            type = i['type']
            wish_list.add_row([time, name, rarity, type])
        print(str(wish_list))
        with open("result.txt", "w") as file:
            file.writelines(str(wish_list))
            file.close()
        with open("result.txt", "rb") as file:
            await ctx.reply("Default banner history:", file=discord.File(file, "result.txt"))
            file.close()

    if res == 'CharacterEvent':
        await interaction.send('Generate Table')
        for i in gs.get_wish_history(301):
            time = i['time']
            name = i['name']
            rarity = i['rarity']
            type = i['type']
            wish_list.add_row([time, name, rarity, type])
        print(str(wish_list))
        with open("result.txt", "w") as file:
            file.writelines(str(wish_list))
            file.close()
        with open("result.txt", "rb") as file:
            await ctx.reply("Character Event history:", file=discord.File(file, "result.txt"))
            file.close()

    if res == 'WeaponEvent':
        await interaction.send('Generate Table')
        for i in gs.get_wish_history(302):
            time = i['time']
            name = i['name']
            rarity = i['rarity']
            type = i['type']
            wish_list.add_row([time, name, rarity, type])
        print(str(wish_list))
        with open("result.txt", "w") as file:
            file.writelines(str(wish_list))
            file.close()
        with open("result.txt", "rb") as file:
            await ctx.reply("Weapon Event history:", file=discord.File(file, "result.txt"))
            file.close()

@client.command()
async def menu(ctx):
    await buttons.send(
	    content = "This is an example message!", 
	    channel = ctx.channel.id,
	    components = [
	    	ActionRow([
		    	Button(
			    	label="Register", 
				    style=ButtonType().Primary, 
				    custom_id="reg"       
			    ),
                Button(
			    	label="Resin", 
				    style=ButtonType().Primary, 
				    custom_id="resin"       
			    ),
                Button(
			    	label="characters", 
				    style=ButtonType().Primary, 
				    custom_id="characters"       
			    ),
                Button(
			    	label="Stats", 
				    style=ButtonType().Primary, 
				    custom_id="stats"       
			    )
		    ])
	    ]
    )

@buttons.click
async def reg(ctx):
    channel = client.get_channel(ctx.member.id)
    await channel.send('test')
    """userid = ctx.member.id
    def check(q):
        return q.author.id == userid
    msg = await client.wait_for('message', check=check)
    ltuid = str(msg.content)

    await ctx.reply('Укажите ltoken:')
    userid = ctx.author.id
    def check(q):
        return q.author.id == userid
    msg = await client.wait_for('message', check=check)
    ltoken = str(msg.content)

    await ctx.reply('Укажите wish:')
    userid = ctx.author.id
    def check(q):
        return q.author.id == userid
    msg = await client.wait_for('message', check=check)
    wish = str(msg.content)

    #await ctx.reply('https://media.discordapp.net/attachments/907163041852977194/908392371690041385/sosage.gif')
    await ctx.reply('LOADING...')

    try:
        connection = mysql.connector.connect(
            host=SQLhost,
            user=SQLuser,
            password=SQLpassword,
            database=SQLdatabase
        )
        cursor = connection.cursor()
        try:
            sql = f'''INSERT INTO User (DiscordID, ltuid, ltoken, wish) VALUES ("{userid}", "{ltuid}", "{ltoken}", "{wish}")'''
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(f"The error '{e}' occurred")
    except Error as e:
        print(f"The error '{e}' occurred")
"""
client.run('ODQzMDUxOTI5MTE3NjU1MDUx.YJ-PSw.FB0XcGwkWj9VWaAkMpSIQxxOXws')

#https://youtu.be/14XYntpP9W0?t=938