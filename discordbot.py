from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.utils import get
from discord.channel import VoiceChannel
from discord import FFmpegPCMAudio
from google.cloud import texttospeech
import re
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()
voiceChannel: VoiceChannel 
messageChannel = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    
@client.event
async def on_message(message):
    global voiceChannel
    global messageChannel
    cmd = message.content.split(" ")[0]
    args = message.content.split(" ")[1:]
    
    if message.author == client.user:
        return
    if message.content == f'{PREFIX}c':
        if message.author.voice is None:
            await message.channel.send('음성체팅에 접속후 사용해주세요')
            return
        
        if messageChannel != None:
            await message.channel.send('봇이 다른 채널에서 접속해있습니다')
            return

        messageChannel = message.channel
        vc = await vc.connect(message.author.voice.channel)
        return
    if message.content == f'{PREFIX}dc':
        if message.channel == messageChannel:
            voiceChannel.stop()
            await vc.disconnect()
            await messageChannel.send('음성채팅에서 퇴장합니다')
            messageChannel = None
            return
        else:
            await message.channel.send('봇이 다른채널에 접속해있습니다')
            await message.channel.send('접속해 있는채널 : ' + messageChannel.name)
            return
        
    if message.channel == messageChannel:
        play_voice(message.content)
        
def text_limitation(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    if re.match(pattern, text):
        text = "URL은 읽을수 없습니다"
    elif len(text) > 100:
        text = text[0:100]
    return text

def text_to_ssml(text):
    text = text_limitation(text)

    escaped_lines = html.escape(text)
    ssml = "{}".format(
        escaped_lines
    )
    return ssml

def ssml_to_speech(ssml, file, language_code, gender):
    ttsClient = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = ttsClient.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(file, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + file)
    return file

def play_voice(text):
    ssml = text_to_ssml(text)
    file = ssml_to_speech(ssml, "voice.mp3", "ja-JP", texttospeech.SsmlVoiceGender.MALE)
    voiceChannel.play(FFmpegPCMAudio(executable="D:\\Work\\Dev\\ffmpeg\\bin\\ffmpeg.exe", source=file))
    
@client.event
async def on_voice_state_update(member, before, after):
    global voiceChannel
    global messageChannel
    if member.bot:
        return
    if after.channel == None:
        if len(before.channel.members) == 1:
            voiceChannel.stop()
            await voiceChannel.disconnect()
            await messageChannel.send('ワオーン！(ひとりで寂しくなったのでTtSDogはお家に帰ります)')
            messageChannel = None
   
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
