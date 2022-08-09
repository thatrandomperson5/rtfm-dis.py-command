async def rtfm(message, msg):
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
