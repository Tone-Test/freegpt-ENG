import g4f
import discord as ds
from dotenv import load_dotenv
import os
from helpers import *
from consts import *
from base import *

ctxt = ds.ApplicationContext
load_dotenv()

bot = ds.Bot(intents=ds.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_message(msg: ds.Message):
    if msg.content.startswith(f'<@{bot.user.id}>'):
        q = ' '.join(msg.content.split(' ')[1:])
        if q == '':
            await msg.channel.send(embed=InfoEmbed('О FreeGPT', INFO_TEXT), reference=msg)
            return
        async with msg.channel.typing():
            try:
                udata = {}
                if os.path.exists(STORAGE + str(msg.author.id)):
                    udata = readjson(str(msg.author.id))
                model = udata.get('model', DEFAULT_MODEL.name)
                chat = udata.get('chat', [])
                res = request(chat, q, model)
                chat.append({'role': 'assistant', 'content': res})
                udata['chat'] = chat
                savejson(str(msg.author.id), udata)
            except Exception as e:
                await msg.channel.send(embed=ErrorEmbed('Ответ не получен\n'+str(e)), reference=msg)
                return
        emb = MessageEmbed(q, res)
        emb.set_footer(text=model)
        await msg.channel.send(embed=emb, reference=msg)

@bot.slash_command(descriprion='Сменить модель')
async def model(ctx: ctxt, model: ds.Option(str, choices=MODELS)):
    udata = {'chat': []}
    if os.path.exists(STORAGE + str(ctx.author.id)):
        udata = readjson(str(ctx.author.id))
    udata['model'] = model
    savejson(str(ctx.author.id), udata)
    await ctx.respond(embed=InfoEmbed('Успешно', f'Модель изменена на {model}'), ephemeral=True)

@bot.slash_command(description='Сбросить диалог')
async def reset(ctx: ctxt):
    if os.path.exists(STORAGE + str(ctx.author.id)): chatlen = len(readjson(str(ctx.author.id))['chat']); os.remove(STORAGE + str(ctx.author.id))
    else: chatlen = 0
    await ctx.respond(embed=InfoEmbed('Успешно', f'Диалог из {chatlen} сообщений сброшен'), ephemeral=True)

@bot.slash_command(description='Просмотреть информацию о боте')
async def info(ctx: ctxt):
    emb = ds.Embed()
    emb.color = ds.Colour.blurple()
    emb.title = 'О FreeGPT'
    emb.description = INFO_TEXT
    await ctx.respond(embed=emb)

@bot.slash_command(description='Очистить чат от разговора с ботом')
async def cleanup(ctx: ctxt, n: int):
    await ctx.respond(content='Подождите...')
    await ctx.channel.purge(limit=n, check=lambda msg: msg.author.id == ctx.author.id)
    await ctx.channel.purge(limit=n, check=lambda msg: msg.author.id == bot.user.id)
    await ctx.delete()

bot.run(os.getenv('TOKEN'))