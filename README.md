# Generatore di Password Sicure 🔒
[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)

Uno script Python per generare password sicure fino a 128 caratteri con:
- Lettere maiuscole
- Lettere minuscole
- Caratteri speciali
- Generazione crittograficamente sicura

## Funzionalità principali ✨
- ✅ Genera password da **3 a 128 caratteri**
- ✅ Utilizza il modulo `secrets` per sicurezza crittografica
- ✅ Include **almeno un carattere** per ogni categoria:
  - Maiuscolo (A-Z)
  - Minuscolo (a-z)
  - Carattere speciale (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
- ✅ Mescolamento casuale sicuro
- ✅ Gestione degli errori per input non validi
- ✅ Interfaccia a riga di comando (CLI)

## Installazione ⚙️
1. Clona la repository:
```bash
git clone https://github.com/ArduinoDenis/py-password-vault.git
cd py-password-vault
```

## Utilizzo 🚀

**Genera una password di default (12 caratteri):**
```bash
python generatore_password.py
```
**Genera una password personalizzata (es. 24 caratteri):**
```bash
python generatore_password.py --lunghezza 24
```
**Esegui con output diretto (per script):**

```bash
python generatore_password.py -l 16 | tee password.txt
```
**Esempio di output:**
```bash
Password generata: s9T}L@8qT!6K^bV7mP?x
```

**Opzioni della CLI 📋**
| Opzione | Descrizione | Valore Default |
|---------|-------------|---------------|
| `-l, --lunghezza` | Lunghezza password (12-128 caratteri) | 12 |


## Best Practices 🔧
- 🔐 Utilizza password di almeno 16 caratteri per servizi importanti
- ⏰ Cambia password ogni 60-90 giorni
- 🚫 Non riutilizzare la stessa password su più servizi
- 💾 Usa un password manager (es. Bitwarden, KeepassXC)
- 🛡️ Abilita l'autenticazione a due fattori (2FA) dove possibile
