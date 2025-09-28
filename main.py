"""
Password Manager - Application principale modernisée
Point d'entrée du password manager avec interface moderne et authentification
"""

import sys
import os
from pathlib import Path
import customtkinter as ctk
import tkinter.font as font 
import tkinter as tk

# Forcer l'encodage UTF-8 pour la console
if sys.platform.startswith('win'):
    # Windows
    try:
        # Essayer de définir l'encodage de la console sur UTF-8
        os.system('chcp 65001 >nul 2>&1')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Configuration CustomTkinter moderne
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ajout du répertoire racine au path
sys.path.append(str(Path(__file__).parent))

from gui.main_window import PasswordManagerApp
from core.database import DatabaseManager
from gui.dialogs.master_password import MasterPasswordDialog, MasterPasswordVerificationDialog

class AuthenticationManager:
    """Gestionnaire d'authentification au démarrage"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.authenticated = False
        self.setup_window = None
    
    def check_authentication_required(self):
        """Vérifier si une authentification est requise"""
        return self.db_manager.has_master_password()
    
    def show_first_time_setup(self):
        """Afficher le setup de première fois"""
        # Créer une fenêtre temporaire pour le setup
        self.setup_window = ctk.CTk()
        self.setup_window.withdraw()  # Cacher la fenêtre principale
        
        # D'abord afficher le message de bienvenue
        from gui.dialogs.startup_login import StartupWelcomeDialog
        welcome_dialog = StartupWelcomeDialog(
            self.setup_window,
            self._show_master_password_creation
        )
        welcome_dialog.show()
    
    def _show_master_password_creation(self):
        """Afficher le dialog de création de mot de passe"""
        from gui.dialogs.master_password import MasterPasswordDialog
        dialog = MasterPasswordDialog(
            self.setup_window, 
            self._on_first_setup_complete
        )
        dialog.show()
    
    def show_login_dialog(self):
        """Afficher le dialog de connexion personnalisé"""
        # Créer une fenêtre temporaire pour le login
        self.setup_window = ctk.CTk()
        self.setup_window.withdraw()  # Cacher la fenêtre principale
        
        # Dialog de connexion personnalisé
        from gui.dialogs.startup_login import StartupLoginDialog
        dialog = StartupLoginDialog(
            self.setup_window,
            self._on_login_success,
            self._on_login_cancelled
        )
        dialog.show()

    def _on_login_cancelled(self):
        """Callback appelé si l'utilisateur annule la connexion"""
        print("[i] Connexion annulée par l'utilisateur")
        self.authenticated = False
        self._close_setup_window()
    
    def _on_first_setup_complete(self):
        """Callback appelé après création du premier mot de passe"""
        print("[✓] Mot de passe maître créé avec succès")
        self.authenticated = True
        self._close_setup_window()
    
    def _on_login_success(self):
        """Callback appelé après connexion réussie"""
        print("[✓] Authentification réussie")
        self.authenticated = True
        self._close_setup_window()
    
    def _close_setup_window(self):
        """Fermer la fenêtre de setup"""
        if self.setup_window:
            self.setup_window.destroy()
            self.setup_window = None
    
    def is_authenticated(self):
        """Vérifier si l'utilisateur est authentifié"""
        return self.authenticated

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
    print("[*] Démarrage du Password Manager...")
    
    # Vérifications préalables
    if not check_dependencies():
        print("[!] Arrêt du programme à cause des dépendances manquantes.")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)
    
    try:
        print("[*] Configuration du thème moderne...")
        setup_modern_theme()
        
        print("[*] Initialisation du système d'authentification...")
        auth_manager = AuthenticationManager()
        
        # Vérifier si c'est la première utilisation
        if not auth_manager.check_authentication_required():
            print("[i] Première utilisation détectée - Configuration requise")
            print("[*] Ouverture du setup initial...")
            auth_manager.show_first_time_setup()
        else:
            print("[i] Mot de passe maître existant - Authentification requise")
            print("[*] Ouverture de l'écran de connexion...")
            auth_manager.show_login_dialog()
        
        # Vérifier si l'authentification a réussi
        if not auth_manager.is_authenticated():
            print("[i] Authentification annulée par l'utilisateur")
            print("[*] Fermeture de l'application...")
            sys.exit(0)
        
        print("[✓] Authentification réussie")
        print("[*] Lancement de l'interface principale...")
        
        # Lancer l'application principale
        app = PasswordManagerApp()
        # Configurer les polices après création de la fenêtre principale
        setup_modern_fonts()
        
        print("[✓] Application prête")
        app.run()
        
    except ImportError as e:
        print(f"[!] Erreur d'import : {e}")
        print("[i] Vérifiez que tous les modules sont bien créés.")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n[i] Interruption par l'utilisateur")
        sys.exit(0)
        
    except Exception as e:
        print(f"[!] Erreur lors du démarrage de l'application : {e}")
        print(f"[i] Type d'erreur : {type(e).__name__}")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)

if __name__ == "__main__":
    main()