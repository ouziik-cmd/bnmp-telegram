import requests
import json
import os
from datetime import datetime

# ===== CONFIGURAÇÕES =====
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MUNICIPIO = "GOIANESIA"
UF = "GO"

ARQUIVO = "vistos.json"


# ===== TELEGRAM =====
def enviar(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": msg},
        timeout=20
    )


# ===== CONTROLE DE MANDADOS JÁ VISTOS =====
def carregar_vistos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []


def salvar_vistos(vistos):
    with open(ARQUIVO, "w") as f:
        json.dump(vistos, f)


# ===== CONSULTA AO BNMP =====
def consultar():
    url = "https://portalbnmp.cnj.jus.br/api/pecas/pesquisar"

    payload = {
        "municipio": MUNICIPIO,
        "uf": UF,
        "pagina": 1,
        "tamanhoPagina": 50
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
    except Exception as e:
        print("Erro ao conectar no BNMP:", e)
        return

    if r.status_code != 200:
        print("BNMP respondeu status:", r.status_code)
        return

    try:
        resposta = r.json()
    except Exception:
        print("Resposta do BNMP não é JSON válido.")
        return

    dados = resposta.get("content", [])
    if not dados:
        print("Nenhum mandado retornado pelo BNMP.")
        return

    vistos = carregar_vistos()
    novos = []

    for item in dados:
        identificador = item.get("id")
        if identificador and identificador not in vistos:
            novos.append(item)
            vistos.append(identificador)

    if not novos:
        print("Nenhum mandado novo.")
        return

    for n in novos:
        nome = (
            n.get("nomeParte")
            or n.get("nomePessoa")
            or n.get("nomeIndiciado")
            or "não informado pelo BNMP"
        )

        msg = (
            f"🚨 NOVO MANDADO BNMP\n\n"
            f"👤 Nome: {nome}\n"
            f"📍 Município: {MUNICIPIO}/{UF}\n"
            f"📄 Classe: {n.get('classeProcessual', 'N/A')}\n"
            f"🔢 Processo: {n.get('numeroProcesso', 'N/A')}\n"
            f"🕒 Detectado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        enviar(msg)

    salvar_vistos(vistos)


# ===== EXECUÇÃO =====
if __name__ == "__main__":
    consultar()
