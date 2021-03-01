import os
import nacl
import discord
import random

from dotenv import load_dotenv
from ytdlsource import YTDLSource
from time import time, sleep
from discord.ext import commands
from ficavivo import keep_alive
from settings import CRAZYFROG_URL, CRAZYFROG_MUSICAS, CRAZYFROG_IMAGES, CRAZYFROG_FRASES, CRAZYFROG_PREFIX

load_dotenv()
intents = discord.Intents(
    guilds=True, voice_states=True, members=True, messages=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CRAZYFROG_PREFIX),
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
    e.set_image(url=pegar_el_aleatorio(CRAZYFROG_IMAGES))
    await ctx.channel.send(pegar_el_aleatorio(CRAZYFROG_FRASES), embed=e)


@bot.command(pass_context=True)
async def estavivo(ctx):
    """Pra ver se o crazy frog ta vivo"""

    await ctx.channel.send("nao")


# @bot.command(pass_context=True)


async def play(ctx, channel: discord.VoiceChannel):
    """Toca uma musica aleatoria do crazy frog"""
    if ctx.guild.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    reproduzir_video(channel, pegar_el_aleatorio(CRAZYFROG_MUSICAS))


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
                await reproduzir_video(voice_channel, CRAZYFROG_URL)
                print("Tocando crazy frog")
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
                print("Saindo: Estamos sozinho: "+str(estamos_sozinho) +
                      "; Bot entrou: "+str(bot_entrou))
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
        await reproduzir_video(channel, CRAZYFROG_URL)
        print("Tocando crazy frog")


async def reproduzir_video(canal, url):
    player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
    canal.guild.voice_client.play(player, after=lambda e: print(
        'Player error: %s' % e) if e else None)


def pegar_el_aleatorio(array):
    return array[random.randrange(0, len(array))]


keep_alive()
bot.run(os.getenv("TOKEN"))
