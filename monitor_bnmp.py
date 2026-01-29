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
        "uf": UF,
        "pagina": 1,
        "tamanhoPagina": 50
    }

    try:
        r = requests.post(url, json=payload, timeout=30)
    except Exception as e:
        print("Erro ao conectar no BNMP:", e)
        return

    if r.status_code != 200:
        print("BNMP respondeu status:", r.status_code)
        return

    try:
        resposta = r.json()
    except Exception:
        print("Resposta do BNMP não é JSON válido. Ignorando execução.")
        return

    dados = resposta.get("content", [])
    vistos = carregar_vistos()
    novos = []

    for item in dados:
        identificador = item.get("id")
        if identificador and identificador not in vistos:
            novos.append(item)
            vistos.append(identificador)

    if novos:
        for n in novos:
            msg = (
                f"🚨 Novo mandado BNMP\n"
                f"Município: {MUNICIPIO}/{UF}\n"
                f"Classe: {n.get('classeProcessual', 'N/A')}\n"
                f"Número: {n.get('numeroProcesso', 'N/A')}\n"
                f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )
            enviar_telegram(msg)

    salvar_vistos(vistos)
