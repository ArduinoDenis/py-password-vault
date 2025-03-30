# Utilizzo:
# Senza parametri password di 12 caratteri - 'python generatore_password.py'
# Specificando la lunghezza della password: 'python generatore_password.py -l 20'

import argparse
import secrets
import string

def genera_password(lunghezza=12):
    """
    Genera una password casuale sicura con maiuscole, minuscole e caratteri speciali.
    """
    if lunghezza < 3 or lunghezza > 128:
        raise ValueError("La lunghezza deve essere compresa tra 3 e 128 caratteri.")

    maiuscole = string.ascii_uppercase
    minuscole = string.ascii_lowercase
    speciali = string.punctuation
    tutti_caratteri = maiuscole + minuscole + speciali

    password = [
        secrets.choice(maiuscole),
        secrets.choice(minuscole),
        secrets.choice(speciali)
    ]

    if lunghezza > 3:
        password += [secrets.choice(tutti_caratteri) for _ in range(lunghezza - 3)]
    
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generatore di password sicure con maiuscole, minuscole e caratteri speciali'
    )
    parser.add_argument(
        '-l', '--lunghezza',
        type=int,
        default=12,
        help='Lunghezza della password (min 3, max 128)'
    )
    
    args = parser.parse_args()
    
    if not (3 <= args.lunghezza <= 128):
        print("Errore: La lunghezza deve essere compresa tra 3 e 128 caratteri")
        exit(1)

    try:
        password = genera_password(args.lunghezza)
        print("Password generata:", password)
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        exit(1)