import time
import hashlib
import hmac
import requests
import os

# Segredos vindos do GitHub
PARTNER_ID = os.getenv("SHOPEE_PARTNER_ID")
APP_SECRET = os.getenv("SHOPEE_APP_SECRET")
APP_KEY = os.getenv("SHOPEE_APP_KEY")

BASE_ID = "18368450207"
SUB_BASE = "Grupaomuquiranas"

API_URL = "https://open-api.affiliate.shopee.com.br/graphql"


def gerar_sign(path, timestamp):
    base = f"{PARTNER_ID}{path}{timestamp}"
    return hmac.new(
        APP_SECRET.encode(),
        base.encode(),
        hashlib.sha256
    ).hexdigest()


def converter(url, subid):

    path = "/graphql"
    ts = int(time.time())

    sign = gerar_sign(path, ts)

    headers = {
        "Content-Type": "application/json"
    }

    query = f"""
    mutation {{
      generateShortLink(
        input: {{
          originalLink: "{url}"
          subIds: ["{subid}"]
        }}
      ) {{
        shortLink
      }}
    }}
    """

    payload = {
        "query": query
    }

    params = {
        "partner_id": PARTNER_ID,
        "timestamp": ts,
        "sign": sign
    }

    r = requests.post(
        API_URL,
        params=params,
        headers=headers,
        json=payload,
        timeout=30
    )

    data = r.json()

    if "errors" in data:
        print("Erro:", data["errors"])
        return "ERRO"

    return data["data"]["generateShortLink"]["shortLink"]


# Ler até 5 links
with open("links.txt", encoding="utf-8") as f:
    linhas = f.read().splitlines()[:5]


resultado = []


for linha in linhas:

    if "|" not in linha:
        continue

    nome, link = linha.split("|", 1)

    nome = nome.strip().replace(" ", "")

    subid = f"{SUB_BASE}-{nome}"

    curto = converter(link.strip(), subid)

    resultado.append(f"{nome}: {curto}")


with open("resultado.txt", "w", encoding="utf-8") as f:
    for r in resultado:
        f.write(r + "\n")


print("FINALIZADO")
