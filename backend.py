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
