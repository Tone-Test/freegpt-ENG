import g4f
import discord as ds
from dotenv import load_dotenv
import os
from helpers import *
from consts import *

ctxt = ds.ApplicationContext

def request(q, model=g4f.Model.gpt_35_turbo):
    response: str = g4f.ChatCompletion.create(model=model, messages=[{'role': 'user', 'content': q}])
    response = response.encode('iso-8859-1').decode('utf-8')
    return response

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
            emb = ds.Embed()
            emb.color = ds.Colour.blurple()
            emb.title = 'О FreeGPT'
            emb.description = INFO_TEXT
            await msg.channel.send(embed=emb, reference=msg)
            return
        async with msg.channel.typing():
            try:
                res = request(q)
            except:
                await msg.channel.send(embed=ErrorEmbed('Ответ не получен'), reference=msg)
                return
        emb = ds.Embed()
        emb.color = ds.Colour.green()
        emb.title = f'Вопрос: {q}'
        emb.description = res
        emb.set_footer(text=g4f.Model.falcon_7b.name)
        await msg.channel.send(embed=emb, reference=msg)

@bot.slash_command(description='Просмотреть информацию о боте')
async def info(ctx: ctxt):
    emb = ds.Embed()
    emb.color = ds.Colour.blurple()
    emb.title = 'О FreeGPT'
    emb.description = INFO_TEXT
    await ctx.respond(embed=emb)

@bot.slash_command(description='Задать вопрос')
async def ask(ctx: ctxt, prompt: str, model: ds.Option(str, description='Название модели', choices=MODELS)=g4f.Model.gpt_35_turbo.name):
    async with ctx.typing():
        emb = ds.Embed()
        emb.color = ds.Colour.orange()
        emb.title = 'GPT думает...'
        emb.description = f'Вопрос: {prompt}\nМодель: {model}'
        await ctx.respond(embed=emb)
        try:
            res = request(prompt)
        except:
            await ctx.edit(embed=ErrorEmbed('Ответ не получен'))
            return
    emb.color = ds.Colour.green()
    emb.title = f'Вопрос: {prompt}'
    emb.description = res
    emb.set_footer(text=model)
    await ctx.edit(embed=emb)

@bot.slash_command(description='Очистить чат от разговора с ботом')
async def cleanup(ctx: ctxt, n: int):
    await ctx.respond(content='Подождите...')
    await ctx.channel.purge(limit=n, check=lambda msg: msg.author.id == ctx.author.id)
    await ctx.channel.purge(limit=n, check=lambda msg: msg.author.id == bot.user.id)
    await ctx.delete()

bot.run(os.getenv('TOKEN'))