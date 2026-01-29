import requests
import json
import os
from datetime import datetime

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
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


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
    vistos = carregar()
    novos = []

    for item in dados:
        identificador = item.get("id")
        if identificador and identificador not in vistos:
            novos.append(item)
            vistos.append(identificador)

    if novos:
        for n in novos:
            nome = (
                n.get("nomeParte")
                or n.get("nomePessoa")
                or n.get("nomeIndiciado")
                or "não informado pelo BNMP"
            )

            msg = (
                f"🚨 Novo mandado BNMP\n"
                f"👤 Nome: {nome}\n"
                f"📍 Município: {MUNICIPIO}/{UF}\n"
                f"📄 Classe: {n.get('classeProcessual', 'N/A')}\n"
                f"🔢 Processo: {n.get('numeroProcesso', 'N/A')}\n"
                f"🕒 Detectado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

            enviar(msg)

    salvar(vistos)


consultar()
print("🔔 TESTE: enviando última ocorrência")

if dados:
    ultimo = dados[0]
    enviar_telegram(
        f"🧪 TESTE MANUAL\n\n"
        f"👤 Nome: {ultimo.get('nome', 'N/A')}\n"
        f"📄 Número: {ultimo.get('numero', 'N/A')}"
    )

