import requests
import json
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MUNICIPIO = "GOIANESIA"
UF = "GO"

ARQUIVO = "vistos.json"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

def consultar():
    url = "https://portalbnmp.cnj.jus.br/api/pecas/pesquisar"
    payload = {
        "municipio": MUNICIPIO,
        "uf": UF
    }

    r = requests.post(url, json=payload, timeout=30)
 try:
    dados = r.json().get("content", [])
except Exception:
    print("Resposta do BNMP não é JSON válido. Ignorando execução.")
    return


    vistos = carregar()
    novos = []

    for item in dados:
        numero = item.get("numeroMandado")
        if numero and numero not in vistos:
            novos.append(numero)
            vistos.append(numero)

    if novos:
        msg = "🚨 NOVOS MANDADOS BNMP:\n\n" + "\n".join(novos)
        enviar(msg)

    salvar(vistos)

if __name__ == "__main__":
    consultar()
