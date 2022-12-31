from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
import lxml
from gtts import gTTS
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@bot.command(name="tts")
async def tts(ctx, *args):
    text = " ".join(args)
    user = ctx.message.author
    if user.voice != None:
        try:
            global vc
            global entireText
            vc = await ctx.message.author.voice.channel.connect()
        except:
            vc = ctx.voice_client
            
        sound = gTTS(text=text, lang="ko", slow=False)
        sound.save("tts-audio.mp3")
        if vc.is_playing():
            vc.stop()
            
        vc.play(discord.FFmpegPCMAudio("tts-audio.mp3"))
    else:
        await ctx.send("없는 명령어 입니다")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
