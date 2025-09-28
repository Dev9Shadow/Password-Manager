"""
Password Manager - Application principale modernisée
Point d'entrée du password manager avec interface moderne
"""

import sys
import os
from pathlib import Path
import customtkinter as ctk
import tkinter.font as font

# Configuration CustomTkinter moderne
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ajout du répertoire racine au path
sys.path.append(str(Path(__file__).parent))

from gui.main_window import PasswordManagerApp

def setup_modern_fonts():
    """Configurer les polices modernes pour toute l'application"""
    try:
        # Police par défaut moderne
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10, weight="normal")
        
        # Police pour le texte
        text_font = font.nametofont("TkTextFont") 
        text_font.configure(family="Segoe UI", size=10, weight="normal")
        
        # Police pour les menus
        menu_font = font.nametofont("TkMenuFont")
        menu_font.configure(family="Segoe UI", size=9, weight="normal")
        
        # Police pour les headers
        heading_font = font.nametofont("TkHeadingFont")
        heading_font.configure(family="Segoe UI", size=11, weight="bold")
        
    except Exception as e:
        print(f"Impossible de configurer les polices modernes : {e}")

def setup_modern_theme():
    """Configurer le thème moderne de l'application"""
    try:
        # Définir les couleurs personnalisées pour CustomTkinter
        ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = ["#1e1e2f", "#1e1e2f"]
        ctk.ThemeManager.theme["CTkButton"]["fg_color"] = ["#4facfe", "#00c9ff"]
        ctk.ThemeManager.theme["CTkButton"]["hover_color"] = ["#00c9ff", "#4facfe"]
        ctk.ThemeManager.theme["CTkEntry"]["fg_color"] = ["#1e1e2f", "#1e1e2f"]
        ctk.ThemeManager.theme["CTkEntry"]["border_color"] = ["#4facfe", "#4facfe"]
        
    except Exception as e:
        print(f"Impossible de configurer le thème : {e}")

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    missing_deps = []
    
    try:
        import customtkinter
    except ImportError:
        missing_deps.append("customtkinter")
    
    try:
        import pyperclip
    except ImportError:
        missing_deps.append("pyperclip")
    
    try:
        from PIL import Image, ImageTk
    except ImportError:
        missing_deps.append("pillow")
    
    if missing_deps:
        print("[!] Dependances manquantes :")
        for dep in missing_deps:
            print(f"   - {dep}")
        print(f"\n[i] Pour installer : pip install {' '.join(missing_deps)}")
        return False
    
    return True

def main():
    """Point d'entrée principal de l'application"""
    print("[*] Demarrage du Password Manager...")
    
    # Vérifications préalables
    if not check_dependencies():
        print("[!] Arret du programme a cause des dependances manquantes.")
        input("Appuyez sur Entree pour fermer...")
        sys.exit(1)
    
    try:
        print("[*] Configuration du theme moderne...")
        setup_modern_theme()
        
        print("[*] Lancement de l'interface...")
        app = PasswordManagerApp()
        # Configurer les polices après création de la fenêtre principale
        setup_modern_fonts()
        app.run()
        
    except ImportError as e:
        print(f"[!] Erreur d'import : {e}")
        print("[i] Verifiez que tous les modules sont bien crees.")
        input("Appuyez sur Entree pour fermer...")
        sys.exit(1)
        
    except Exception as e:
        print(f"[!] Erreur lors du demarrage de l'application : {e}")
        print(f"[i] Type d'erreur : {type(e).__name__}")
        input("Appuyez sur Entree pour fermer...")
        sys.exit(1)

if __name__ == "__main__":
    main()