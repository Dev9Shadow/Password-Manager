"""
Dialog des paramètres de l'application
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkSwitch, CTkOptionMenu
from PIL import ImageTk, Image

from config.settings import COLORS, WINDOW_CONFIG, IMAGES_DIR, MESSAGES
from utils.geometry import GeometryUtils
from gui.widgets.custom_widgets import ModernCard, ModernButton, ModernLabel, show_success, show_error
from gui.dialogs.master_password import MasterPasswordDialog, MasterPasswordVerificationDialog
from core.database import DatabaseManager

class SettingsDialog:
    """Dialog des paramètres de l'application"""
    
    def __init__(self, parent, on_settings_changed=None):
        self.parent = parent
        self.on_settings_changed = on_settings_changed
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.theme_var = tk.StringVar(value="dark")
        self.auto_lock_var = tk.BooleanVar(value=False)
        self.clipboard_timeout_var = tk.StringVar(value="30")
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'])
        config = WINDOW_CONFIG['settings']
        GeometryUtils.apply_window_config(self.dialog, config)
        
        # Icône et titre de la fenêtre
        self.dialog.iconbitmap() if hasattr(self.dialog, 'iconbitmap') else None
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_header()
        self._create_security_section()
        self._create_appearance_section()
        self._create_clipboard_section()
        self._create_action_buttons()
    
    def _create_header(self):
        """Créer l'en-tête du dialog"""
        # Titre principal
        title_label = ModernLabel(
            self.dialog,
            text="⚙️ Paramètres",
            style="title"
        )
        title_label.place(x=30, y=20)
        
        # Ligne décorative
        line = Canvas(
            self.dialog,
            width=440,
            height=2,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        line.place(x=30, y=60)
    
    def _create_security_section(self):
        """Créer la section sécurité"""
        # Card pour la sécurité
        security_card = ModernCard(self.dialog, width=440, height=120)
        security_card.place(x=30, y=80)
        
        # Titre de section
        security_title = ModernLabel(
            security_card,
            text="🔒 Sécurité",
            style="subtitle"
        )
        security_title.place(x=20, y=15)
        
        # Bouton changer mot de passe maître
        change_master_btn = ModernButton(
            security_card,
            text="Changer le mot de passe maître",
            command=self._change_master_password,
            width=200,
            height=35
        )
        change_master_btn.place(x=20, y=50)
        
        # Switch pour verrouillage automatique
        auto_lock_label = ModernLabel(
            security_card,
            text="Verrouillage automatique :",
            style="primary"
        )
        auto_lock_label.place(x=240, y=55)
        
        auto_lock_switch = CTkSwitch(
            security_card,
            text="",
            variable=self.auto_lock_var,
            width=40,
            height=20,
            switch_width=40,
            switch_height=20,
            fg_color=COLORS['button_secondary'],
            progress_color=COLORS['button_primary']
        )
        auto_lock_switch.place(x=380, y=55)
    
    def _create_appearance_section(self):
        """Créer la section apparence"""
        # Card pour l'apparence
        appearance_card = ModernCard(self.dialog, width=440, height=80)
        appearance_card.place(x=30, y=220)
        
        # Titre de section
        appearance_title = ModernLabel(
            appearance_card,
            text="🎨 Apparence",
            style="subtitle"
        )
        appearance_title.place(x=20, y=15)
        
        # Label thème
        theme_label = ModernLabel(
            appearance_card,
            text="Thème :",
            style="primary"
        )
        theme_label.place(x=20, y=45)
        
        # Menu déroulant pour le thème
        theme_menu = CTkOptionMenu(
            appearance_card,
            values=["Sombre", "Clair", "Automatique"],
            variable=self.theme_var,
            width=120,
            height=30,
            fg_color=COLORS['button_secondary'],
            button_color=COLORS['button_primary'],
            button_hover_color=COLORS['button_hover']
        )
        theme_menu.place(x=80, y=42)
    
    def _create_clipboard_section(self):
        """Créer la section presse-papiers"""
        # Card pour le presse-papiers
        clipboard_card = ModernCard(self.dialog, width=440, height=80)
        clipboard_card.place(x=30, y=320)
        
        # Titre de section
        clipboard_title = ModernLabel(
            clipboard_card,
            text="📋 Presse-papiers",
            style="subtitle"
        )
        clipboard_title.place(x=20, y=15)
        
        # Label timeout
        timeout_label = ModernLabel(
            clipboard_card,
            text="Effacement automatique :",
            style="primary"
        )
        timeout_label.place(x=20, y=45)
        
        # Menu déroulant pour le timeout
        timeout_menu = CTkOptionMenu(
            clipboard_card,
            values=["10 sec", "30 sec", "60 sec", "5 min", "Jamais"],
            variable=self.clipboard_timeout_var,
            width=100,
            height=30,
            fg_color=COLORS['button_secondary'],
            button_color=COLORS['button_primary'],
            button_hover_color=COLORS['button_hover']
        )
        timeout_menu.place(x=180, y=42)
    
    def _create_action_buttons(self):
        """Créer les boutons d'action"""
        # Bouton Sauvegarder
        save_btn = ModernButton(
            self.dialog,
            text="💾 Sauvegarder",
            command=self._save_settings,
            style="success",
            width=120
        )
        save_btn.place(x=220, y=420)
        
        # Bouton Annuler
        cancel_btn = ModernButton(
            self.dialog,
            text="❌ Annuler",
            command=self._close,
            style="secondary",
            width=120
        )
        cancel_btn.place(x=350, y=420)
        
        # Bouton À propos
        about_btn = ModernButton(
            self.dialog,
            text="ℹ️ À propos",
            command=self._show_about,
            style="secondary",
            width=120
        )
        about_btn.place(x=30, y=420)
    
    def _change_master_password(self):
        """Changer le mot de passe maître"""
        def on_verification_success():
            """Callback appelé après vérification réussie"""
            dialog = MasterPasswordDialog(self.dialog, self._on_master_password_changed)
            dialog.show()
        
        # D'abord vérifier l'ancien mot de passe
        verification_dialog = MasterPasswordVerificationDialog(
            self.dialog, 
            on_verification_success,
            "Vérification - Ancien mot de passe"
        )
        verification_dialog.show()
    
    def _on_master_password_changed(self):
        """Callback appelé quand le mot de passe maître est changé"""
        show_success(self.dialog, "Mot de passe maître modifié avec succès !")
    
    def _save_settings(self):
        """Sauvegarder les paramètres"""
        try:
            # Ici vous pouvez sauvegarder les paramètres dans un fichier de config
            # ou dans la base de données
            
            settings = {
                'theme': self.theme_var.get(),
                'auto_lock': self.auto_lock_var.get(),
                'clipboard_timeout': self.clipboard_timeout_var.get()
            }
            
            print(f"Sauvegarde des paramètres : {settings}")
            
            # Callback pour informer la fenêtre parent
            if self.on_settings_changed:
                self.on_settings_changed(settings)
            
            show_success(self.dialog, "Paramètres sauvegardés avec succès !")
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            show_error(self.dialog, "Erreur lors de la sauvegarde des paramètres")
    
    def _show_about(self):
        """Afficher les informations à propos"""
        about_text = """🔐 Password Vault v1.0

                    Gestionnaire sécurisé de mots de passe

                    Développé avec :
                    • Python 3.x
                    • CustomTkinter
                    • SQLite3
                    • Cryptography

                    © 2024 - Tous droits réservés"""
        
        # Créer une fenêtre à propos
        about_dialog = Toplevel(self.dialog, bg=COLORS['primary_bg'])
        about_dialog.title("À propos")
        about_dialog.geometry("400x300")
        about_dialog.resizable(False, False)
        
        # Centrer sur le parent
        about_dialog.geometry(GeometryUtils.center_on_parent(self.dialog, 400, 300))
        
        # Contenu
        about_label = ModernLabel(
            about_dialog,
            text=about_text,
            style="primary"
        )
        about_label.place(x=50, y=50)
        
        # Bouton fermer
        close_btn = ModernButton(
            about_dialog,
            text="Fermer",
            command=about_dialog.destroy,
            width=100
        )
        close_btn.place(x=150, y=250)
        
        about_dialog.grab_set()  # Modal
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()