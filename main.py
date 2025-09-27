"""
Password Manager - Application principale
Point d'entrée du password manager
"""

import sys
import os
from pathlib import Path

# Ajout du répertoire racine au path
sys.path.append(str(Path(__file__).parent))

from gui.main_window import PasswordManagerApp

def main():
    """Point d'entrée principal de l'application"""
    try:
        app = PasswordManagerApp()
        app.run()
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()