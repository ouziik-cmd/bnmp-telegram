# 🔔 Monitor de Mandados BNMP → Telegram

Este projeto monitora automaticamente o **BNMP (Banco Nacional de Mandados de Prisão)**  
e envia uma **notificação no Telegram** sempre que surgir **um novo mandado** para um município específico.

Atualmente configurado para:
- 📍 Município: **Goianésia / GO**
- 🔁 Execução automática via **GitHub Actions**
- ⏱️ Intervalo: configurável (ex: a cada 3 ou 5 minutos)

---

## 🚀 Como funciona

1. O GitHub Actions executa o script em intervalos regulares
2. O script consulta o BNMP
3. Se houver **mandado novo**:
   - envia mensagem no Telegram
4. Mandados já verificados não são reenviados

---

## 🛠️ Tecnologias usadas

- Python 3.11
- GitHub Actions
- API do Telegram
- Requests (HTTP)

---

## 🔐 Variáveis de ambiente (Secrets)

Este projeto utiliza **GitHub Secrets**:

- `TELEGRAM_TOKEN` → Token do bot do Telegram
- `CHAT_ID` → ID do chat ou usuário que receberá as mensagens

---

## 📁 Estrutura do projeto

```text
.
├── monitor_bnmp.py
├── vistos.json
├── README.md
└── .github/
    └── workflows/
        └── monitor_bnmp.yml
