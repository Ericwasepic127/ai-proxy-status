import os, json, asyncio
from pyscript import web
from pyscript import fetch

SERVERS = {
    "oregon-0": "https://ai-proxy-x.onrender.com/",
    "oregon-1": "https://ai-proxy-2.onrender.com/",
    "singapore-0": "https://ai-proxy-3.onrender.com/",
    "frankfurt-1": "https://ai-proxy-4.onrender.com/",
}

MEAN = [
    "Account API key - index number 0",
    "Account API key - index number 1"
]

def serverList(sel):
    ip = SERVERS[sel]
    location, index = sel.split("-")
    return ip, location.title(), MEAN[int(index)]

async def testOut(ip):
    try:
        return (await fetch(ip + "ready")).ok
    except:
        return False

contain = web.page["#divelem"]
if contain and os.environ.get("MARK_ELEM"):
    contain._dom_element.innerHTML = ""
    contain.style.clear()
    contain.classes.clear()
else:
    os.environ["MARK_ELEM"] = "True"
    web.page["#executer"].insertAdjacentElement("afterend", web.div(id="divelem")._dom_element)
    contain = web.page["#divelem"]

ipInf = "\U0001f4cd IP address: %s"
pf = """\U0001f9ed Location: %s
\U0001f9fe Info: Render server (%s)"""
sd = "\U0001f4f6 Is server down? %s"

items = []
for name in SERVERS:
    items.append(serverList(name))

async def check(ip, po):
    po._dom_element.innerHTML = sd % ("No" if await testOut(ip) else "Yes")

for item in items:
    ps = web.p(sd % "checking status")
    asyncio.create_task(check(item[0], ps))
    contain.append(
        web.h3(ipInf % (f'<a href="{item[0]}">{item[0]}</a>')),
        web.pre(pf % item[1:]),
        ps
  )
