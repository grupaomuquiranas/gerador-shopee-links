import requests

AFILIADO = "18368450207"

def encurtar(url):
    api = f"https://is.gd/create.php?format=simple&url={url}"
    return requests.get(api).text

with open("links.txt") as f:
    links = f.read().splitlines()

resultado = []

for link in links:
    afiliado = f"{link}?smtt={AFILIADO}"
    curto = encurtar(afiliado)
    resultado.append(curto)

with open("resultado.txt", "w") as f:
    for r in resultado:
        f.write(r + "\n")

print("Pronto!")
