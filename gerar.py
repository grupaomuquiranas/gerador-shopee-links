import requests
import urllib.parse

# SEU ID + SUBID
AFILIADO = "18368450207.Grupaomuquiranas"


def criar_link_afiliado(url):
    # Remove parâmetros antigos
    base = url.split("?")[0]

    # Adiciona seu ID corretamente
    return base + "?smtt=" + AFILIADO


def encurtar(url):
    api = "https://is.gd/create.php"
    params = {
        "format": "simple",
        "url": url
    }

    r = requests.get(api, params=params, timeout=20)

    return r.text.strip()


# Ler até 5 links
with open("links.txt", "r", encoding="utf-8") as f:
    links = f.read().splitlines()[:5]


resultado = []


for link in links:

    link = link.strip()

    if not link:
        continue

    # Criar link afiliado CORRETO
    afiliado = criar_link_afiliado(link)

    # Encurtar depois
    curto = encurtar(afiliado)

    resultado.append(curto)


# Salvar resultado
with open("resultado.txt", "w", encoding="utf-8") as f:

    if not resultado:
        f.write("NENHUM LINK GERADO\n")

    else:
        for r in resultado:
            f.write(r + "\n")


print("Concluído com ID correto")
