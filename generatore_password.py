#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore di Password Avanzato
Un'applicazione moderna per generare password sicure con interfaccia grafica
Autore: ArduinoDenis.it
Versione: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import re
import json
import os
from datetime import datetime
import hashlib
import base64
from cryptography.fernet import Fernet
import argparse
import sys

class GeneratorePasswordAvanzato:
    def __init__(self, root):
        self.root = root
        self.root.title("Generatore Password Avanzato v2.0")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # tema moderno
        self.setup_theme()
        
        # Variabili
        self.lunghezza_var = tk.IntVar(value=16)
        self.maiuscole_var = tk.BooleanVar(value=True)
        self.minuscole_var = tk.BooleanVar(value=True)
        self.numeri_var = tk.BooleanVar(value=True)
        self.speciali_var = tk.BooleanVar(value=True)
        self.escludi_ambigui_var = tk.BooleanVar(value=False)
        self.password_generata = tk.StringVar()
        self.forza_password = tk.StringVar()
        
        self.caratteri_ambigui = "0O1lI|`'\""
        
        self.cronologia = []
        
        self.crea_interfaccia()
        
    def setup_theme(self):
        """Configura un tema moderno per l'applicazione"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colori moderni
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), foreground='#34495e')
        style.configure('Strong.TLabel', font=('Segoe UI', 9, 'bold'))
        
    def crea_interfaccia(self):
        """Crea l'interfaccia grafica principale"""
       
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        title_label = ttk.Label(main_frame, text="🔐 Generatore Password Avanzato", style='Title.TLabel')
        title_label.grid(row=row, column=0, columnspan=2, pady=(0, 20))
        row += 1
        
        # lunghezza password
        ttk.Label(main_frame, text="Lunghezza Password:", style='Strong.TLabel').grid(row=row, column=0, sticky=tk.W, pady=5)
        
        length_frame = ttk.Frame(main_frame)
        length_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        length_frame.columnconfigure(0, weight=1)
        
        self.length_scale = ttk.Scale(length_frame, from_=4, to=128, orient=tk.HORIZONTAL, 
                                     variable=self.lunghezza_var, command=self.aggiorna_lunghezza)
        self.length_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.length_label = ttk.Label(length_frame, text="16")
        self.length_label.grid(row=0, column=1)
        row += 1
        
        # opzioni caratteri
        options_frame = ttk.LabelFrame(main_frame, text="Opzioni Caratteri", padding="10")
        options_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(options_frame, text="Lettere Maiuscole (A-Z)", variable=self.maiuscole_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Lettere Minuscole (a-z)", variable=self.minuscole_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Numeri (0-9)", variable=self.numeri_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Caratteri Speciali (!@#$...)", variable=self.speciali_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Escludi Caratteri Ambigui (0,O,1,l,I)", variable=self.escludi_ambigui_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="🎲 Genera Password", command=self.genera_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📋 Copia", command=self.copia_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="💾 Salva", command=self.salva_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📊 Analizza", command=self.analizza_password).pack(side=tk.LEFT, padx=5)
        row += 1
        
        # password generata
        ttk.Label(main_frame, text="Password Generata:", style='Strong.TLabel').grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        row += 1
        
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        password_frame.columnconfigure(0, weight=1)
        
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_generata, 
                                       font=('Consolas', 12), state='readonly')
        self.password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(password_frame, text="👁", command=self.toggle_visibilita, width=3).grid(row=0, column=1)
        row += 1
        
        # Indicatore forza password
        ttk.Label(main_frame, text="Forza Password:", style='Strong.TLabel').grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        row += 1
        
        self.forza_label = ttk.Label(main_frame, textvariable=self.forza_password, font=('Segoe UI', 10, 'bold'))
        self.forza_label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.forza_progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.forza_progress.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # cronologia Password Generate
        history_frame = ttk.LabelFrame(main_frame, text="Cronologia Password", padding="10")
        history_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        columns = ('Timestamp', 'Password', 'Lunghezza', 'Forza')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        history_buttons = ttk.Frame(history_frame)
        history_buttons.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(history_buttons, text="🗑 Pulisci Cronologia", command=self.pulisci_cronologia).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_buttons, text="📤 Esporta", command=self.esporta_cronologia).pack(side=tk.LEFT, padx=5)
        
        self.genera_password()
        
    def aggiorna_lunghezza(self, value):
        """Aggiorna l'etichetta della lunghezza"""
        lunghezza = int(float(value))
        self.length_label.config(text=str(lunghezza))
        
    def genera_password(self):
        """Genera una nuova password sicura"""
        try:
            lunghezza = self.lunghezza_var.get()
            
            if not any([self.maiuscole_var.get(), self.minuscole_var.get(), 
                       self.numeri_var.get(), self.speciali_var.get()]):
                messagebox.showerror("Errore", "Seleziona almeno un tipo di carattere!")
                return
            
            caratteri = ""
            caratteri_obbligatori = []
            
            if self.maiuscole_var.get():
                maiuscole = string.ascii_uppercase
                if self.escludi_ambigui_var.get():
                    maiuscole = ''.join(c for c in maiuscole if c not in self.caratteri_ambigui)
                caratteri += maiuscole
                caratteri_obbligatori.append(secrets.choice(maiuscole))
            
            if self.minuscole_var.get():
                minuscole = string.ascii_lowercase
                if self.escludi_ambigui_var.get():
                    minuscole = ''.join(c for c in minuscole if c not in self.caratteri_ambigui)
                caratteri += minuscole
                caratteri_obbligatori.append(secrets.choice(minuscole))
            
            if self.numeri_var.get():
                numeri = string.digits
                if self.escludi_ambigui_var.get():
                    numeri = ''.join(c for c in numeri if c not in self.caratteri_ambigui)
                caratteri += numeri
                caratteri_obbligatori.append(secrets.choice(numeri))
            
            if self.speciali_var.get():
                speciali = string.punctuation
                if self.escludi_ambigui_var.get():
                    speciali = ''.join(c for c in speciali if c not in self.caratteri_ambigui)
                caratteri += speciali
                caratteri_obbligatori.append(secrets.choice(speciali))
            
            password = caratteri_obbligatori.copy()
            
            for _ in range(lunghezza - len(caratteri_obbligatori)):
                password.append(secrets.choice(caratteri))
            
            secrets.SystemRandom().shuffle(password)
            password_finale = ''.join(password)
            
            self.password_generata.set(password_finale)
            self.valuta_forza_password(password_finale)
            
            self.aggiungi_cronologia(password_finale)
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione: {str(e)}")
    
    def valuta_forza_password(self, password):
        """Valuta la forza della password"""
        punteggio = 0
        feedback = []
        
        # Lunghezza
        if len(password) >= 12:
            punteggio += 25
        elif len(password) >= 8:
            punteggio += 15
        else:
            feedback.append("Troppo corta")
        
        if re.search(r'[a-z]', password):
            punteggio += 15
        else:
            feedback.append("Mancano minuscole")
            
        if re.search(r'[A-Z]', password):
            punteggio += 15
        else:
            feedback.append("Mancano maiuscole")
            
        if re.search(r'\d', password):
            punteggio += 15
        else:
            feedback.append("Mancano numeri")
            
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            punteggio += 20
        else:
            feedback.append("Mancano caratteri speciali")
        
        # Complessità aggiuntiva
        if len(set(password)) / len(password) > 0.7: 
            punteggio += 10
        
        #  livello Password
        if punteggio >= 80:
            livello = "🟢 Molto Forte"
            colore = "green"
        elif punteggio >= 60:
            livello = "🟡 Forte"
            colore = "orange"
        elif punteggio >= 40:
            livello = "🟠 Media"
            colore = "darkorange"
        else:
            livello = "🔴 Debole"
            colore = "red"
        
        self.forza_password.set(f"{livello} ({punteggio}/100)")
        self.forza_label.configure(foreground=colore)
        self.forza_progress['value'] = punteggio
        
        return punteggio, livello.split()[1]
    
    def toggle_visibilita(self):
        """Alterna la visibilità della password"""
        if self.password_entry['show'] == '*':
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')
    
    def copia_password(self):
        """Copia la password negli appunti"""
        password = self.password_generata.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Successo", "Password copiata negli appunti!")
        else:
            messagebox.showwarning("Attenzione", "Nessuna password da copiare!")
    
    def salva_password(self):
        """Salva la password in un file crittografato"""
        password = self.password_generata.get()
        if not password:
            messagebox.showwarning("Attenzione", "Nessuna password da salvare!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")],
            title="Salva Password"
        )
        
        if filename:
            try:
                # password master per crittografia
                master_password = tk.simpledialog.askstring(
                    "Password Master", 
                    "Inserisci una password master per crittografare il file:",
                    show='*'
                )
                
                if master_password:
                    
                    key = base64.urlsafe_b64encode(
                        hashlib.pbkdf2_hmac('sha256', 
                                          master_password.encode(), 
                                          b'salt_', 100000)[:32]
                    )
                    
                    fernet = Fernet(key)
                    
                    data = {
                        'password': password,
                        'timestamp': datetime.now().isoformat(),
                        'lunghezza': len(password),
                        'forza': self.forza_password.get()
                    }
                    
                    encrypted_data = fernet.encrypt(json.dumps(data).encode())
                    
                    with open(filename, 'wb') as f:
                        f.write(encrypted_data)
                    
                    messagebox.showinfo("Successo", f"Password salvata in {filename}")
                    
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel salvataggio: {str(e)}")
    
    def analizza_password(self):
        """Mostra analisi dettagliata della password"""
        password = self.password_generata.get()
        if not password:
            messagebox.showwarning("Attenzione", "Nessuna password da analizzare!")
            return
        
        analisi_window = tk.Toplevel(self.root)
        analisi_window.title("Analisi Password")
        analisi_window.geometry("500x400")
        
        analisi_text = tk.Text(analisi_window, wrap=tk.WORD, padx=10, pady=10)
        analisi_text.pack(fill=tk.BOTH, expand=True)
        
        punteggio, livello = self.valuta_forza_password(password)
        
        analisi = f"""ANALISI DETTAGLIATA PASSWORD
{'='*50}

Password: {password}
Lunghezza: {len(password)} caratteri
Forza: {livello} ({punteggio}/100)

COMPOSIZIONE:
• Lettere minuscole: {len([c for c in password if c.islower()])}
• Lettere maiuscole: {len([c for c in password if c.isupper()])}
• Numeri: {len([c for c in password if c.isdigit()])}
• Caratteri speciali: {len([c for c in password if not c.isalnum()])}
• Caratteri unici: {len(set(password))}/{len(password)}

STATISTICHE:
• Entropia: {len(password) * 3.32:.1f} bit
• Tempo crack (brute force): {self.calcola_tempo_crack(password)}
• Ripetizioni: {len(password) - len(set(password))}

RACCOMANDAZIONI:
{self.genera_raccomandazioni(password)}
"""
        
        analisi_text.insert(tk.END, analisi)
        analisi_text.configure(state='disabled')
    
    def calcola_tempo_crack(self, password):
        """Calcola tempo stimato per crack brute force"""
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(not c.isalnum() for c in password):
            charset_size += 32
        
        combinations = charset_size ** len(password)
        seconds = combinations / (2 * 1_000_000_000)
        
        if seconds < 60:
            return f"{seconds:.1f} secondi"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minuti"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} ore"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} giorni"
        else:
            return f"{seconds/31536000:.1f} anni"
    
    def genera_raccomandazioni(self, password):
        """Genera raccomandazioni per migliorare la password"""
        raccomandazioni = []
        
        if len(password) < 12:
            raccomandazioni.append("• Aumenta la lunghezza ad almeno 12 caratteri")
        
        if not any(c.islower() for c in password):
            raccomandazioni.append("• Aggiungi lettere minuscole")
        
        if not any(c.isupper() for c in password):
            raccomandazioni.append("• Aggiungi lettere maiuscole")
        
        if not any(c.isdigit() for c in password):
            raccomandazioni.append("• Aggiungi numeri")
        
        if not any(not c.isalnum() for c in password):
            raccomandazioni.append("• Aggiungi caratteri speciali")
        
        if len(set(password)) / len(password) < 0.7:
            raccomandazioni.append("• Riduci caratteri ripetuti")
        
        if not raccomandazioni:
            raccomandazioni.append("• Password ottima! Nessun miglioramento necessario.")
        
        return "\n".join(raccomandazioni)
    
    def aggiungi_cronologia(self, password):
        """Aggiunge password alla cronologia"""
        punteggio, livello = self.valuta_forza_password(password)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.cronologia.append({
            'timestamp': timestamp,
            'password': password,
            'lunghezza': len(password),
            'forza': livello
        })
        
        if len(self.cronologia) > 50:
            self.cronologia.pop(0)
        
        self.aggiorna_cronologia_view()
    
    def aggiorna_cronologia_view(self):
        """Aggiorna la visualizzazione della cronologia"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for entry in reversed(self.cronologia[-10:]):  # Mostra solo ultime 10
            self.history_tree.insert('', 0, values=(
                entry['timestamp'],
                entry['password'][:20] + '...' if len(entry['password']) > 20 else entry['password'],
                entry['lunghezza'],
                entry['forza']
            ))
    
    def pulisci_cronologia(self):
        """Pulisce la cronologia"""
        if messagebox.askyesno("Conferma", "Vuoi davvero pulire la cronologia?"):
            self.cronologia.clear()
            self.aggiorna_cronologia_view()
    
    def esporta_cronologia(self):
        """Esporta cronologia in file CSV"""
        if not self.cronologia:
            messagebox.showwarning("Attenzione", "Nessuna cronologia da esportare!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")],
            title="Esporta Cronologia"
        )
        
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'Password', 'Lunghezza', 'Forza'])
                    for entry in self.cronologia:
                        writer.writerow([entry['timestamp'], entry['password'], 
                                       entry['lunghezza'], entry['forza']])
                
                messagebox.showinfo("Successo", f"Cronologia esportata in {filename}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'esportazione: {str(e)}")

def genera_password_cli(lunghezza=16, maiuscole=True, minuscole=True, numeri=True, speciali=True, escludi_ambigui=False):
    """Funzione per generare password da linea di comando"""
    caratteri = ""
    caratteri_obbligatori = []
    caratteri_ambigui = "0O1lI|`'\""
    
    if maiuscole:
        chars = string.ascii_uppercase
        if escludi_ambigui:
            chars = ''.join(c for c in chars if c not in caratteri_ambigui)
        caratteri += chars
        caratteri_obbligatori.append(secrets.choice(chars))
    
    if minuscole:
        chars = string.ascii_lowercase
        if escludi_ambigui:
            chars = ''.join(c for c in chars if c not in caratteri_ambigui)
        caratteri += chars
        caratteri_obbligatori.append(secrets.choice(chars))
    
    if numeri:
        chars = string.digits
        if escludi_ambigui:
            chars = ''.join(c for c in chars if c not in caratteri_ambigui)
        caratteri += chars
        caratteri_obbligatori.append(secrets.choice(chars))
    
    if speciali:
        chars = string.punctuation
        if escludi_ambigui:
            chars = ''.join(c for c in chars if c not in caratteri_ambigui)
        caratteri += chars
        caratteri_obbligatori.append(secrets.choice(chars))
    
    if not caratteri:
        raise ValueError("Almeno un tipo di carattere deve essere selezionato")
    
    password = caratteri_obbligatori.copy()
    for _ in range(lunghezza - len(caratteri_obbligatori)):
        password.append(secrets.choice(caratteri))
    
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def main():
    """Funzione principale"""
    parser = argparse.ArgumentParser(
        description='Generatore di Password Avanzato v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  python generatore_password.py                    # Interfaccia grafica
  python generatore_password.py --cli              # Modalità linea di comando
  python generatore_password.py --cli -l 20        # Password di 20 caratteri
  python generatore_password.py --cli --no-special # Senza caratteri speciali
        """
    )
    
    parser.add_argument('--cli', action='store_true', help='Modalità linea di comando')
    parser.add_argument('-l', '--lunghezza', type=int, default=16, help='Lunghezza password (4-128)')
    parser.add_argument('--no-upper', action='store_true', help='Escludi maiuscole')
    parser.add_argument('--no-lower', action='store_true', help='Escludi minuscole')
    parser.add_argument('--no-digits', action='store_true', help='Escludi numeri')
    parser.add_argument('--no-special', action='store_true', help='Escludi caratteri speciali')
    parser.add_argument('--exclude-ambiguous', action='store_true', help='Escludi caratteri ambigui')
    parser.add_argument('-n', '--numero', type=int, default=1, help='Numero di password da generare')
    
    args = parser.parse_args()
    
    if args.cli:
        # Modalità CLI
        try:
            if not (4 <= args.lunghezza <= 128):
                print("❌ Errore: La lunghezza deve essere tra 4 e 128 caratteri")
                sys.exit(1)
            
            print(f"🔐 Generatore Password Avanzato v2.0")
            print(f"📏 Lunghezza: {args.lunghezza} caratteri")
            print(f"🔢 Numero password: {args.numero}")
            print("-" * 50)
            
            for i in range(args.numero):
                password = genera_password_cli(
                    lunghezza=args.lunghezza,
                    maiuscole=not args.no_upper,
                    minuscole=not args.no_lower,
                    numeri=not args.no_digits,
                    speciali=not args.no_special,
                    escludi_ambigui=args.exclude_ambiguous
                )
                print(f"Password {i+1}: {password}")
                
        except Exception as e:
            print(f"❌ Errore: {e}")
            sys.exit(1)
    else:
        # Modalità GUI
        try:
            import tkinter.simpledialog
            root = tk.Tk()
            app = GeneratorePasswordAvanzato(root)
            root.mainloop()
        except ImportError as e:
            print(f"❌ Errore: Modulo mancante - {e}")
            print("💡 Installa le dipendenze con: pip install cryptography")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Errore nell'avvio dell'interfaccia grafica: {e}")
            print("💡 Prova la modalità CLI con: python generatore_password.py --cli")
            sys.exit(1)

if __name__ == "__main__":
    main()

