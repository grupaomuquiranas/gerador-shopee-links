import requests

AFILIADO = "18368450207.Grupaomuquiranas"

def encurtar(url):
    api = f"https://is.gd/create.php?format=simple&url={url}"
    return requests.get(api, timeout=30).text

with open("links.txt", "r", encoding="utf-8") as f:
    links = f.read().splitlines()[:5]

resultado = []

for link in links:
    link = link.strip()
    if not link:
        continue

    afiliado = link + "?smtt=" + AFILIADO

    try:
        curto = encurtar(afiliado)
        resultado.append(curto)
    except:
        resultado.append("ERRO: " + afiliado)

with open("resultado.txt", "w", encoding="utf-8") as f:
    for r in resultado:
        f.write(r + "\n")

print("OK")
