import asyncio
import os
import discord
import youtube_dl
import random

from time import time, sleep
from discord.ext import commands
from discord import ChannelType
from ficavivo import keep_alive

CRAZYFROG_URL = "https://www.youtube.com/watch?v=PzE6ti2_Oo8"
CRAZYFROG_IMAGES = [
  "https://i.ytimg.com/vi/k85mRPqvMbE/mqdefault.jpg",
  "https://i.ytimg.com/vi/EQozbKOh6nY/hqdefault.jpg",
  "https://phoneky.co.uk/thumbs/screensavers/down/abstract/crazyfrogg_e6lfuqz6.gif",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwilJbtD314ZJSMLFVkesi0kwP9pf6rnWwrg&usqp=CAU",
  "https://studiosol-a.akamaihd.net/uploadfile/letras/fotos/d/c/7/0/dc7011d1e16d3d500f8b5374cd0731cc.jpg",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQx77KpROFNDBA3jAs2tkhvVs_-bjqRbp7_JQ&usqp=CAU",
  "https://i.ytimg.com/vi/S_IAqwrvEuU/maxresdefault.jpg",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkXlXDgxZZ_91UV07HoIp5ZzfWUluRgD9p1g&usqp=CAU",
  "https://i.ytimg.com/vi/TOGusJon6qw/maxresdefault.jpg",
  "https://crazyfrog.tv/assets/img/HEADER_CRAZY-FROG.jpg",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0CSeWUKIYEMI68GZmSLT8DluPXF1hmfB-wg&usqp=CAU",
  "https://media.adultnode.com/uploads/photos/2021/01/adultnode_cb4a2ddbaf584b53290361e76f1234bf.png",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDw77kqDQo1A53SkvLfs8CbC7l6s5A2xEPtw&usqp=CAU",
  "https://ehgt.org/t/2b/80/2b804faf4f24f4f9670cfe134595344b9b575edb-298653-1133-967-png_l.jpg",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpd-4Ing6oCCmERD1I6dfQKZz9RyXrn8tzMQ&usqp=CAU",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSof6nmOfz54zv6byGnFzkjNMDnO5MQYARhEw&usqp=CAU",
  "https://cdn.discordapp.com/attachments/389094746569834509/815343803803107349/EC_UhhrXsAE_Xfo.png",
  "https://media.sketchfab.com/models/62aa800fb9214e8fa126c00304d7bdb1/thumbnails/5d4c65434d024d789f967280563d52b6/7d613ab3c24648e1b7b7518d3d99d48f.jpeg",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKloajGbhTyVn0G0jBUPT1ZUyDa25dz163-g&usqp=CAU",
  "https://media.gettyimages.com/photos/crazy-frog-during-fight-for-life-fundraiser-december-12-2005-at-hard-picture-id134740624?s=612x612",
  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXUR2lXclE6MeTDE9Hhu8sXsdFn2hfBMVF1w&usqp=CAU",
  "https://pbs.twimg.com/profile_images/423522916/monalisa_mona-crazy-frog_2_400x400.jpg",
  "https://pics.me.me/create-meme-chundra-chuchundra-chundra-chuchundra-crazy-frog-53748802.png",
  "https://i.kym-cdn.com/photos/images/original/000/302/654/bb0.jpg",
  "https://i.ebayimg.com/images/g/MVUAAOxy06hSFSq5/s-l300.jpg",
  "https://cdn.discordapp.com/attachments/389094746569834509/815346365998956564/unknown.png",
]
CRAZYFROG_FRASES = [
  "Crazy frog fugindo da policia",
  "Crazy frog fumando maconha",
  "Crazy frog vs Rodrogas who is more fuck",
  "Primo distante de crazy frog Terry Morcegão",
  "Imagem rara do Crazy Frog bombardeando Hiroshima",
  "Crazy Frog Ahegao",
  "Crazy Frog poetakkkk",
  "Crazy frog correndo em seu habitat natural",
  "Crazy frog de férias",
  "Crazy Frog racer 2",
  "Crazy frog says trans rights",
  "Crazy Frog João Paulo",
  "Rodrogas crazy frog",
  "Crazy Frog Crazy hits",
  "Crazy frog rodrogas",
  "Crazy Frog perdendo o carro porque não pagou o parquímetro",
  "Sabia que o savian sabia assobiar??",
  "Crazy Frog discoteca",
  "Crazy frog presents more crazy hits",
  "Crazy Frog pelúcia",
  "Crazy frog sapo maluco",
  "Crazy Frog pintudo",
  "Crazy Frog furioso",
  "Crazy frog presents crazy Christmas",
  "Crazy Frog secsokkkk",
  "Crazy Frog crucificado",
  "Creize frogue",
  "Crazy Frog Blender",
  "Frog Crazy",
  "Exército de Crazy Frog",
  "Crayzer Frogger",
  "Crazy Frog Afro",
  "crazy Frog de calça",
  "5 Crazy frogs contra 8 savianos, quem ganha?",
  "Sabia que o Crazy Frog sabia assobiar?",
]
CRAZYFROG_MUSICAS = [
  "https://www.youtube.com/watch?v=k85mRPqvMbE&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=0kXwW6reObk&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=P1KT_I1LmtA&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=S_IAqwrvEuU&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=TOGusJon6qw&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=S6rZtIipew8&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=10HwmvvxlEw&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=jwI1j7sslYI&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=_5SfNi71nd8&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=jLPYnw17GTY&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=ua1LGVE9lvY&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=KRbsco8M7Fc&ab_channel=CrazyFrog",
  "https://www.youtube.com/watch?v=FSNXhmBxRKE&ab_channel=CrazyFrog",
]

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents(guilds=True, voice_states=True, members=True, messages=True)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


bot = commands.Bot(command_prefix=commands.when_mentioned_or("cf:"),
                   description='Relatively simple music bot example',
                   intents=intents)


@bot.command(pass_context=True)
async def dingding(ctx):
  """Destezo crazy frog"""

  await ctx.channel.send("Destezo crazy frog")


@bot.command(pass_context=False)
async def letra(ctx):
  """A letra de crazy frog muito foda"""

  await ctx.channel.send(open("crazyfrogletra", 'r').read())


@bot.command(pass_context=False)
async def imagem(ctx):
  """Posta uma imagem do crazy frog"""

  e = discord.Embed()
  e.set_image(url=CRAZYFROG_IMAGES[random.randrange(0, len(CRAZYFROG_IMAGES))])
  await ctx.channel.send(CRAZYFROG_FRASES[random.randrange(0, len(CRAZYFROG_FRASES))], embed = e)


async def play(ctx, channel: discord.VoiceChannel):
  """Toca uma musica aleatoria do crazy frog"""
  if ctx.guild.voice_client is None:
    await channel.connect()
  else:
    await ctx.voice_client.move_to(channel)
  
  tocar_crazyfrog(channel, CRAZYFROG_MUSICAS[random.randrange(0, len(CRAZYFROG_MUSICAS))])


@bot.event
async def on_ready():
  print('Logged in as {0} ({0.id})'.format(bot.user))
  print('------')

  for guild in bot.guilds:
    for voice_channel in guild.voice_channels:
      members = voice_channel.members
      if len(members) > 0:
        has_bot = False
        for member in members:
          if member.bot:
            has_bot = True
            break
        
        if has_bot:
          continue
        
        await voice_channel.connect()
        await tocar_crazyfrog(voice_channel, CRAZYFROG_URL)
        break


@bot.event
async def on_voice_state_update(member, before, after):
  # Canal
  channel = None
  if before.channel is not None:
    channel = before.channel
    print(member.name+" saiu de um canal")
  elif after.channel is not None:
    channel = after.channel
    print(member.name+" entrou em um canal")
  
  if channel is None:
    print("Deu pau")
    return
  
  voice_client = channel.guild.voice_client

  # Alguem entrou ou saiu de um canal
  if not before.channel and after.channel or before.channel and not after.channel:
    # Ja estamos tocando crazy frog
    if voice_client is not None:
      print("Ja estamos tocando crazy frog")
      
      bot_entrou = before.channel is None and after.channel is not None and after.channel == voice_client.channel and member != bot.user and member.bot
      estamos_sozinho = len(voice_client.channel.members) == 1
      # Se um bot entrar, ou se tivermos sozinho no canal, sai
      if bot_entrou or estamos_sozinho:
        print("Saindo: Estamos sozinho: "+str(estamos_sozinho)+ "; Bot entrou: "+str(bot_entrou))
        await voice_client.disconnect()
      return
    
    print("Nao estamos tocando crazy frog")

    # Checar se o canal ja tem bot
    for m in channel.members:
      if m.bot:
        print("O canal que esse usuario entrou ja tem bot, faz nada")
        return
      
    # Checar se o canal tem gente
    if len(channel.members) == 0:
      return
    
    await channel.connect()
    await tocar_crazyfrog(channel, CRAZYFROG_URL)


async def tocar_crazyfrog(canal, url):
    player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
    canal.guild.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    print("Tocando crazy frog")


keep_alive()
bot.run(os.getenv("TOKEN"))