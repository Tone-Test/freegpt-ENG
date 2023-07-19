import g4f
from json import load, dump
from consts import *

def request(ctx: list, q, model=DEFAULT_MODEL):
    ctx.append({'role': 'user', 'content': q})
    response: str = g4f.ChatCompletion.create(model=model, messages=ctx)
    response = response.encode('iso-8859-1').decode('utf-8')
    return response

def readjson(path) -> dict:
    with open(STORAGE + path) as f:
        d = load(f)
        f.close
    return d

def savejson(path, data):
    with open(STORAGE + path, 'w') as f:
        dump(data, f)
        f.close()