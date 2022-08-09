from discord.ext import commands
bot = commands.Bot(command_prefix='?')

async def docget(slug, version, q):
    async with aiohttp.ClientSession() as cs:
        url = f"https://readthedocs.org/api/v2/search/?format=json&project={slug}&q={q}&version={version}"
        print(url)
        async with cs.get(url) as r:
            res = await r.json()
    out = {}
    
    for x in res["results"]:
        if x["path"].endswith("api.html"):
            out[x["domain"]+x["path"]] = x["blocks"]
        
    for x, y in out.items():
        out[x] = [z for z in y if z["type"] == "domain"]
    return out
 
async def rtfm_(message, msg):
    if msg[1].startswith("https://") or msg[1].startswith("http://"):
        sl = urlparse(msg[1])
        sl = sl.hostname
        sl = sl.split(".")
        sl = sl[0]
        dg = await docget(sl, msg[2], msg[3])
    else:
        dg = await docget(msg[1], msg[2], msg[3])
    
    ds = "\n"
    for x,y in dg.items():
        for z in y:
           ds += f"\n[`{z['name']}`]({x+'#'+z['id']})"
    ds += "\n "
    embed = discord.Embed(description=ds)
    await message.channel.send(embed=embed)

@bot.command()
async def rftm(ctx, doc: str, version: str, query: str):
    rftm_(ctx.message, [doc, version, query])
    
bot.run('token')
