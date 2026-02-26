import time
import hashlib
import hmac
import requests
import os

PARTNER_ID = os.getenv("SHOPEE_PARTNER_ID")
APP_SECRET = os.getenv("SHOPEE_APP_SECRET")
APP_KEY = os.getenv("SHOPEE_APP_KEY")

SUB_BASE = "Grupaomuquiranas"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

def gerar_sign(path, timestamp):
    base = f"{PARTNER_ID}{path}{timestamp}"
    return hmac.new(APP_SECRET.encode(), base.encode(), hashlib.sha256).hexdigest()

def converter(url, subid):
    try:
        path = "/graphql"
        ts = int(time.time())
        sign = gerar_sign(path, ts)

        headers = {"Content-Type": "application/json"}

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
        payload = {"query": query}
        params = {"partner_id": PARTNER_ID, "timestamp": ts, "sign": sign}

        print(f"Chamando API para {url} com subid {subid}")
        r = requests.post(API_URL, params=params, headers=headers, json=payload, timeout=20)
        data = r.json()
        print("Resposta da API:", data)

        if "errors" in data:
            return "ERRO"

        return data["data"]["generateShortLink"]["shortLink"]

    except Exception as e:
        print(f"Exception no link {url}: {e}")
        return "ERRO"

# Ler até 5 links
with open("links.txt", encoding="utf-8") as f:
    linhas = f.read().splitlines()[:5]

resultado = []

for linha in linhas:
    if "|" not in linha:
        print(f"Pulado (formato inválido): {linha}")
        continue
    nome, link = linha.split("|", 1)
    nome = nome.strip().replace(" ", "")
    link = link.strip()
    subid = f"{SUB_BASE}-{nome}"

    curto = converter(link, subid)
    resultado.append(f"{nome}: {curto}")

with open("resultado.txt", "w", encoding="utf-8") as f:
    for r in resultado:
        f.write(r + "\n")

print("FINALIZADO")
