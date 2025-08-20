[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
# 🔐 Generatore Password Avanzato v2.0

Un'applicazione moderna e completa per generare password sicure con interfaccia grafica intuitiva e modalità linea di comando.

## ✨ Caratteristiche Principali

### 🎯 Funzionalità Avanzate
- **Interfaccia Grafica Moderna**: Design pulito e intuitivo con tema moderno
- **Generazione Sicura**: Utilizza il modulo `secrets` per la massima sicurezza crittografica
- **Personalizzazione Completa**: Controllo totale sui tipi di caratteri da includere
- **Analisi Forza Password**: Valutazione in tempo reale della robustezza della password
- **Cronologia Intelligente**: Tracciamento delle password generate con timestamp
- **Salvataggio Crittografato**: Possibilità di salvare password in file crittografati
- **Modalità CLI**: Utilizzo da linea di comando per automazione e script

### 🛡️ Sicurezza
- Generazione crittograficamente sicura con `secrets.SystemRandom()`
- Esclusione opzionale di caratteri ambigui (0, O, 1, l, I)
- Crittografia AES per il salvataggio delle password
- Nessun logging o memorizzazione non sicura

### 📊 Analisi Password
- **Indicatore Forza**: Visualizzazione grafica della robustezza
- **Analisi Dettagliata**: Composizione, entropia, tempo di crack stimato
- **Raccomandazioni**: Suggerimenti per migliorare la sicurezza
- **Statistiche Complete**: Caratteri unici, ripetizioni, varietà

## 🚀 Installazione

### Prerequisiti
- Python 3.7 o superiore
- Tkinter (incluso nella maggior parte delle installazioni Python)

### Installazione Dipendenze
```bash
pip install -r requirements.txt
```

## 💻 Utilizzo

### Interfaccia Grafica (Modalità Predefinita)
```bash
python generatore_password.py
```

### Modalità Linea di Comando
```bash
# Genera una password con impostazioni predefinite
python generatore_password.py --cli

# Password personalizzata di 20 caratteri
python generatore_password.py --cli -l 20

# Genera 5 password senza caratteri speciali
python generatore_password.py --cli -n 5 --no-special

# Password senza caratteri ambigui
python generatore_password.py --cli --exclude-ambiguous
```

### Opzioni CLI Disponibili
- `--cli`: Attiva modalità linea di comando
- `-l, --lunghezza`: Lunghezza password (4-128, default: 16)
- `-n, --numero`: Numero di password da generare (default: 1)
- `--no-upper`: Escludi lettere maiuscole
- `--no-lower`: Escludi lettere minuscole
- `--no-digits`: Escludi numeri
- `--no-special`: Escludi caratteri speciali
- `--exclude-ambiguous`: Escludi caratteri ambigui

## 🎮 Funzionalità Interfaccia Grafica

### 🎛️ Controlli Principali
- **Slider Lunghezza**: Regola la lunghezza da 4 a 128 caratteri
- **Opzioni Caratteri**: Checkbox per ogni tipo di carattere
- **Pulsanti Azione**: Genera, Copia, Salva, Analizza
- **Toggle Visibilità**: Mostra/nascondi password generata

### 📈 Indicatori Forza
- **Barra Progresso**: Visualizzazione grafica della forza
- **Etichette Colorate**: 
  - 🔴 Debole (0-39 punti)
  - 🟠 Media (40-59 punti)
  - 🟡 Forte (60-79 punti)
  - 🟢 Molto Forte (80-100 punti)

### 📋 Cronologia
- **Visualizzazione Tabellare**: Timestamp, password, lunghezza, forza
- **Esportazione CSV**: Salva cronologia in formato CSV
- **Gestione Automatica**: Mantiene ultime 50 password generate

### 💾 Salvataggio Sicuro
- **Crittografia AES**: File protetti con password master
- **Formato JSON**: Struttura dati organizzata
- **Metadati Completi**: Timestamp, forza, lunghezza

## 🔍 Analisi Dettagliata Password

L'analisi fornisce:
- **Composizione**: Conteggio per tipo di carattere
- **Entropia**: Calcolo dell'entropia in bit
- **Tempo Crack**: Stima tempo brute force
- **Raccomandazioni**: Suggerimenti personalizzati
- **Statistiche**: Caratteri unici, ripetizioni

## 🛠️ Miglioramenti dalla Versione Precedente

### ✅ Nuove Funzionalità
- ✨ Interfaccia grafica completa e moderna
- 📊 Sistema di analisi e valutazione password
- 📋 Cronologia con esportazione
- 💾 Salvataggio crittografato
- 🎯 Controlli granulari per generazione
- 👁️ Toggle visibilità password
- 🚫 Esclusione caratteri ambigui
- 📈 Indicatori visivi forza password

### 🔧 Miglioramenti Tecnici
- 🛡️ Sicurezza crittografica migliorata
- 🎨 Design responsive e moderno
- 📱 Interfaccia utente intuitiva
- ⚡ Performance ottimizzate
- 🐛 Gestione errori robusta
- 📚 Documentazione completa

## 🎯 Esempi d'Uso

### Scenario 1: Password per Account Importante
```bash
# Password molto sicura di 24 caratteri
python generatore_password.py --cli -l 24
```

### Scenario 2: Password per Sistema Legacy
```bash
# Password senza caratteri speciali e ambigui
python generatore_password.py --cli --no-special --exclude-ambiguous
```

### Scenario 3: Batch di Password
```bash
# Genera 10 password per test
python generatore_password.py --cli -n 1 -l 12
```

## 🔒 Note sulla Sicurezza

- **Non riutilizzare password**: Ogni account dovrebbe avere una password unica
- **Lunghezza minima**: Si raccomandano almeno 12 caratteri
- **Varietà caratteri**: Includere tutti i tipi per massima sicurezza
- **Aggiornamento regolare**: Cambiare password periodicamente
- **Storage sicuro**: Utilizzare un password manager per memorizzare

## 🤝 Contributi

Questo progetto è stato completamente riscritto e migliorato per offrire:
- Maggiore sicurezza
- Interfaccia moderna
- Funzionalità avanzate
- Migliore usabilità

## 📄 Licenza

Questo software è fornito "as-is" per scopi educativi e di utilità.
