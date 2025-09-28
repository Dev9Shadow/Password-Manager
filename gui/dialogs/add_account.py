"""
Dialog pour ajouter un nouveau compte
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas
import customtkinter as ctk
from customtkinter import CTkButton, CTkEntry, CTkLabel, CTkFrame

from config.settings import COLORS, WINDOW_CONFIG
from utils.geometry import GeometryUtils
from utils.validators import Validator
from gui.widgets.custom_widgets import show_error
from core.password_generator import PasswordGenerator

class AddAccountDialog:
    """Dialog pour ajouter un nouveau compte"""
    
    def __init__(self, parent, on_save_callback=None):
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.validator = Validator()
        self.password_generator = PasswordGenerator()
        
        self.dialog = None
        self.site_entry = None
        self.login_entry = None
        self.password_entry = None
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue moderne"""
        ctk.set_appearance_mode("dark")
        
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.configure(fg_color=COLORS['primary_bg'])
        
        config = WINDOW_CONFIG['add_account']
        self.dialog.title(config['title'])
        self.dialog.geometry(GeometryUtils.center_window(
            self.dialog, config['width'], config['height']
        ))
        self.dialog.minsize(config['width'], config['height'])
        self.dialog.maxsize(config['width'], config['height'])
        self.dialog.resizable(*config['resizable'])
        
        # Masquer la fenêtre parent
        self.parent.withdraw()
    
    def _setup_ui(self):
        """Configurer l'interface moderne"""
        # Card principale avec width/height dans le constructeur
        main_card = CTkFrame(
            self.dialog,
            width=300,
            height=450,
            fg_color=COLORS['card_bg'],
            corner_radius=15
        )
        main_card.place(x=25, y=25)
        
        # Titre
        title = CTkLabel(
            main_card,
            text="✨ Nouveau Compte",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.place(x=20, y=20)
        
        # Site Web
        CTkLabel(
            main_card,
            text="🌐 Site Web",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS['text_accent']
        ).place(x=20, y=80)
        
        self.site_entry = CTkEntry(
            main_card,
            width=260,
            placeholder_text="ex: google.com",
            fg_color=COLORS['input_bg'],
            border_color=COLORS['input_border'],
            text_color=COLORS['input_text']
        )
        self.site_entry.place(x=20, y=110)
        
        # Username  
        CTkLabel(
            main_card,
            text="👤 Nom d'utilisateur",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS['text_accent']
        ).place(x=20, y=160)
        
        self.login_entry = CTkEntry(
            main_card,
            width=260,
            placeholder_text="Votre nom d'utilisateur",
            fg_color=COLORS['input_bg'],
            border_color=COLORS['input_border'],
            text_color=COLORS['input_text']
        )
        self.login_entry.place(x=20, y=190)
        
        # Password
        CTkLabel(
            main_card,
            text="🔒 Mot de passe",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS['text_accent']
        ).place(x=20, y=240)
        
        self.password_entry = CTkEntry(
            main_card,
            width=220,
            placeholder_text="Mot de passe sécurisé",
            show="*",
            fg_color=COLORS['input_bg'],
            border_color=COLORS['input_border'],
            text_color=COLORS['input_text']
        )
        self.password_entry.place(x=20, y=270)
        
        # Bouton générateur
        gen_btn = CTkButton(
            main_card,
            text="🎲",
            command=self._generate_password,
            width=30,
            height=35,
            fg_color=COLORS['button_secondary'],
            hover_color=COLORS['button_primary']
        )
        gen_btn.place(x=250, y=270)
        
        # Boutons d'action
        save_btn = CTkButton(
            main_card,
            text="💾 Sauvegarder",
            command=self._on_save,
            fg_color=COLORS['button_success'],
            hover_color="#40c057",
            width=120
        )
        save_btn.place(x=20, y=380)
        
        cancel_btn = CTkButton(
            main_card,
            text="❌ Annuler", 
            command=self._on_back,
            fg_color=COLORS['button_danger'],
            hover_color="#ff5252",
            width=120
        )
        cancel_btn.place(x=160, y=380)
    
    def _generate_password(self):
        """Générer un mot de passe aléatoire"""
        password = self.password_generator.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
    
    def _clear_entries(self):
        """Vider tous les champs de saisie"""
        self.site_entry.delete(0, tk.END)
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def _on_save(self):
        """Gestionnaire du bouton sauvegarder"""
        # Récupérer les valeurs
        site = self.site_entry.get().strip()
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Valider les données
        is_valid, error_message = self.validator.validate_account_data(site, login, password)
        
        if not is_valid:
            show_error(self.dialog, error_message)
            self._clear_entries()
            return
        
        # Appeler le callback de sauvegarde
        if self.on_save_callback:
            try:
                self.on_save_callback(site, login, password)
                self._close()
            except Exception as e:
                show_error(self.dialog, f"Erreur lors de la sauvegarde : {str(e)}")
    
    def _on_back(self):
        """Gestionnaire du bouton retour"""
        self._close()
    
    def _close(self):
        """Fermer le dialogue et restaurer la fenêtre parent"""
        self.dialog.destroy()
        self.parent.deiconify()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()