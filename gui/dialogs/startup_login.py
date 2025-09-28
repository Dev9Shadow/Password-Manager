"""
Dialog de connexion au démarrage de l'application
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas
import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel, CTkFrame

from config.settings import COLORS, WINDOW_CONFIG
from utils.geometry import GeometryUtils
from gui.widgets.custom_widgets import CustomEntry, show_error
from core.database import DatabaseManager

class StartupLoginDialog:
    """Dialog de connexion personnalisé pour le démarrage"""
    
    def __init__(self, parent, on_success_callback=None, on_cancel_callback=None):
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.on_cancel_callback = on_cancel_callback
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.password_entry = None
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'])
        config = WINDOW_CONFIG['startup_login']
        GeometryUtils.apply_window_config(self.dialog, config)
        self.dialog.resizable(False, False)
        
        # Centrer la fenêtre
        self.dialog.geometry(GeometryUtils.center_window(self.dialog, 600, 350))
        
        # Empêcher la fermeture par X
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_header()
        self._create_password_field()
        self._create_buttons()
        self._create_footer()
    
    def _create_header(self):
        """Créer l'en-tête avec logo et titre"""
        # Card principale
        main_card = ctk.CTkFrame(
            self.dialog,
            width=400,
            height=400,
            fg_color=COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=COLORS['input_border']
        )
        main_card.place(x=20, y=25)
        
        # Logo/Icône principal
        logo_label = Label(
            main_card,
            text="🔐",
            bg=COLORS['card_bg'],
            fg=COLORS['text_accent'],
            font=('Segoe UI', 48)
        )
        logo_label.place(x=200, y=20)
        
        # Titre principal
        title_label = ctk.CTkLabel(
            main_card,
            text="Password Vault",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title_label.place(x=110, y=90)
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            main_card,
            text="Gestionnaire sécurisé de mots de passe",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.place(x=100, y=130)
        
        # Ligne décorative
        line = Canvas(
            main_card,
            width=300,
            height=2,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        line.place(x=100, y=160)
    
    def _create_password_field(self):
        """Créer le champ de mot de passe"""
        # Récupérer la référence à main_card depuis le parent
        main_card = self.dialog.winfo_children()[0]
        
        # Label
        password_label = ctk.CTkLabel(
            main_card,
            text="🔑 Mot de passe maître :",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS['text_secondary']
        )
        password_label.place(x=50, y=170)
        
        # Entry moderne
        self.password_entry = ctk.CTkEntry(
            main_card,
            width=300,
            height=40,
            show="*",
            placeholder_text="Saisissez votre mot de passe maître",
            fg_color=COLORS['input_bg'],
            border_color=COLORS['input_border'],
            text_color=COLORS['input_text'],
            font=ctk.CTkFont(family="Segoe UI", size=12),
            corner_radius=10
        )
        self.password_entry.place(x=50, y=200)
        self.password_entry.focus_set()
        
        # Lier Enter à la connexion
        self.password_entry.bind('<Return>', lambda e: self._on_login())
    
    def _create_buttons(self):
        """Créer les boutons d'action"""
        # Récupérer la référence à main_card
        main_card = self.dialog.winfo_children()[0]
        
        # Bouton Se connecter
        login_btn = ctk.CTkButton(
            main_card,
            text="🚪 Se connecter",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._on_login,
            width=140,
            height=40,
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15
        )
        login_btn.place(x=50, y=270)
        
        # Bouton Quitter
        quit_btn = ctk.CTkButton(
            main_card,
            text="❌ Quitter",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._on_cancel,
            width=140,
            height=40,
            fg_color=COLORS['button_danger'],
            hover_color='#ff5252',
            corner_radius=15
        )
        quit_btn.place(x=210, y=270)
    
    def _create_footer(self):
        """Créer le pied de page"""
        footer_label = Label(
            self.dialog,
            text="© 2024 Password Vault - Sécurisé par chiffrement AES-256",
            bg=COLORS['primary_bg'],
            fg=COLORS['text_secondary'],
            font=('Segoe UI', 8)
        )
        footer_label.place(x=120, y=500)
    
    def _on_login(self):
        """Gestionnaire de connexion"""
        password = self.password_entry.get()
        
        if not password.strip():
            show_error(self.dialog, "Veuillez saisir votre mot de passe")
            self.password_entry.focus_set()
            return
        
        # Vérifier le mot de passe
        if self.db_manager.verify_master_password(password):
            print("[✓] Connexion réussie")
            if self.on_success_callback:
                self.on_success_callback()
            self._close()
        else:
            show_error(self.dialog, "Mot de passe incorrect")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
    
    def _on_cancel(self):
        """Gestionnaire d'annulation"""
        if self.on_cancel_callback:
            self.on_cancel_callback()
        self._close()
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.focus_set()
        self.dialog.wait_window()

class StartupWelcomeDialog:
    """Dialog de bienvenue pour la première utilisation"""
    
    def __init__(self, parent, on_continue_callback=None):
        self.parent = parent
        self.on_continue_callback = on_continue_callback
        
        self.dialog = None
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'])
        config = WINDOW_CONFIG['startup_welcome']
        GeometryUtils.apply_window_config(self.dialog, config)
        
        # Empêcher la fermeture par X
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_continue)
        
    def _setup_ui(self):
        """Configurer l'interface"""
        # Card principale
        welcome_card = ctk.CTkFrame(
            self.dialog,
            width=450,  # Ajusté pour la nouvelle taille
            height=400,  # Ajusté pour la nouvelle taille
            fg_color=COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=COLORS['input_border']
        )
        welcome_card.place(x=15, y=20)
        
        # Icône de bienvenue
        welcome_icon = Label(
            welcome_card,
            text="🎉",
            bg=COLORS['card_bg'],
            fg=COLORS['text_accent'],
            font=('Segoe UI', 48)
        )
        welcome_icon.place(x=250, y=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            welcome_card,
            text="Bienvenue dans Password Vault !",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title_label.place(x=75, y=90)
        
        # Message de bienvenue
        welcome_text = """🔐 Première utilisation détectée !

Pour sécuriser vos mots de passe, vous devez d'abord 
définir un mot de passe maître.

Ce mot de passe sera nécessaire à chaque ouverture 
de l'application et permettra de chiffrer toutes 
vos données.

⚠️  Important : N'oubliez pas ce mot de passe !
Il ne peut pas être récupéré si vous l'oubliez."""
        
        message_label = ctk.CTkLabel(
            welcome_card,
            text=welcome_text,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS['text_secondary'],
            justify="left"
        )
        message_label.place(x=75, y=130)
        
        # Bouton Continuer
        continue_btn = ctk.CTkButton(
            welcome_card,
            text="🚀 Créer mon mot de passe maître",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._on_continue,
            width=300,
            height=40,
            fg_color=COLORS['button_success'],
            hover_color='#40c057',
            corner_radius=15
        )
        continue_btn.place(x=75, y=340)
    
    def _on_continue(self):
        """Continuer vers la création du mot de passe"""
        if self.on_continue_callback:
            self.on_continue_callback()
        self._close()
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.focus_set()
        self.dialog.wait_window()