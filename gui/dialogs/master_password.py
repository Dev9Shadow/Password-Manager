"""
Dialog pour la gestion du mot de passe maître
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas
from PIL import ImageTk, Image
from customtkinter import CTkButton

from config.settings import COLORS, WINDOW_CONFIG, IMAGES_DIR, MESSAGES
from utils.geometry import GeometryUtils
from utils.validators import Validator
from gui.widgets.custom_widgets import CustomEntry, show_error, show_success
from core.database import DatabaseManager

class MasterPasswordDialog:
    """Dialog pour définir/modifier le mot de passe maître"""
    
    def __init__(self, parent, on_success_callback=None):
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.validator = Validator()
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.password_entry = None
        self.confirmation_entry = None
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'])
        config = WINDOW_CONFIG['master_password']
        GeometryUtils.apply_window_config(self.dialog, config)
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_title()
        self._create_password_field()
        self._create_confirmation_field()
        self._create_save_button()
    
    def _create_title(self):
        """Créer le titre du dialog"""
        title_label = Label(
            self.dialog,
            text="🔐 Nouveau mot de passe maître",
            fg=COLORS['text_primary'],
            bg=COLORS['primary_bg'],
            font=('Segoe UI', 16, 'bold')
        )
        title_label.place(x=50, y=30)
        
        # Ligne décorative
        line = Canvas(
            self.dialog,
            width=250,
            height=2,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        line.place(x=50, y=70)
    
    def _create_password_field(self):
        """Créer le champ mot de passe maître"""
        # Label
        password_label = Label(
            self.dialog,
            text="Nouveau mot de passe :",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('Segoe UI', 12, 'bold')
        )
        password_label.place(x=40, y=100)
        
        # Entry
        self.password_entry = CustomEntry(self.dialog, show_text=True)
        self.password_entry.place(x=70, y=130, width=200)
        
        # Focus sur le premier champ
        self.password_entry.focus_set()
        
        # Ligne décorative
        password_line = Canvas(
            self.dialog,
            width=200,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        password_line.place(x=70, y=155)
        
        # Icône (optionnelle, sans erreur si pas trouvée)
        self._add_icon("🔑", x=40, y=130)
    
    def _create_confirmation_field(self):
        """Créer le champ de confirmation"""
        # Label
        confirmation_label = Label(
            self.dialog,
            text="Confirmer le mot de passe :",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('Segoe UI', 12, 'bold')
        )
        confirmation_label.place(x=40, y=180)
        
        # Entry
        self.confirmation_entry = CustomEntry(self.dialog, show_text=True)
        self.confirmation_entry.place(x=70, y=210, width=200)
        
        # Ligne décorative
        confirmation_line = Canvas(
            self.dialog,
            width=200,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        confirmation_line.place(x=70, y=235)
        
        # Icône
        self._add_icon("🔐", x=40, y=210)
        
        # Lier Enter à la sauvegarde
        self.confirmation_entry.bind('<Return>', lambda e: self._on_save())
    
    def _create_save_button(self):
        """Créer les boutons"""
        # Bouton Sauvegarder
        save_btn = CTkButton(
            self.dialog,
            text="💾 Sauvegarder",
            font=("Segoe UI", 12, "bold"),
            command=self._on_save,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15,
            width=120,
            height=40,
            border_color="black",
            border_width=1
        )
        save_btn.place(x=30, y=220)
        
        # Bouton Annuler
        cancel_btn = CTkButton(
            self.dialog,
            text="❌ Annuler",
            font=("Segoe UI", 12, "bold"),
            command=self._close,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_secondary'],
            hover_color=COLORS['button_primary'],
            corner_radius=15,
            width=120,
            height=40,
            border_color="black",
            border_width=1
        )
        cancel_btn.place(x=160, y=220)
        
        # Instructions
        info_label = Label(
            self.dialog,
            text="Le mot de passe doit contenir au moins 5 caractères",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('Segoe UI', 9)
        )
        info_label.place(x=40, y=250)
    
    def _add_icon(self, icon_text: str, x: int, y: int):
        """Ajouter une icône emoji ou texte"""
        try:
            icon_label = Label(
                self.dialog, 
                text=icon_text, 
                bg=COLORS['primary_bg'],
                fg=COLORS['text_accent'],
                font=('Segoe UI', 12)
            )
            icon_label.place(x=x, y=y)
        except Exception as e:
            print(f"Impossible d'ajouter l'icône : {e}")
    
    def _on_save(self):
        """Gestionnaire du bouton sauvegarder"""
        password = self.password_entry.get()
        confirmation = self.confirmation_entry.get()
        
        # Valider les mots de passe
        is_valid, error_message = self.validator.validate_master_password(password, confirmation)
        
        if not is_valid:
            show_error(self.dialog, error_message)
            self._clear_entries()
            return
        
        try:
            # Sauvegarder le mot de passe maître
            self.db_manager.set_master_password(password)
            show_success(self.dialog, MESSAGES['success']['master_changed'])
            
            # Appeler le callback de succès
            if self.on_success_callback:
                self.on_success_callback()
            
            self._close()
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du mot de passe maître : {e}")
            show_error(self.dialog, "Erreur lors de la sauvegarde")
    
    def _clear_entries(self):
        """Vider les champs de saisie"""
        self.password_entry.delete(0, tk.END)
        self.confirmation_entry.delete(0, tk.END)
        self.password_entry.focus_set()
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()

class MasterPasswordVerificationDialog:
    """Dialog pour vérifier le mot de passe maître"""
    
    def __init__(self, parent, on_success_callback=None, title="Vérification du mot de passe maître"):
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.db_manager = DatabaseManager()
        self.dialog_title = title
        
        self.dialog = None
        self.password_entry = None
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'])
        config = WINDOW_CONFIG['master_password'].copy()
        config['title'] = self.dialog_title
        config['height'] = 300  # Plus petit pour la vérification
        GeometryUtils.apply_window_config(self.dialog, config)
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_title()
        self._create_password_field()
        self._create_buttons()
    
    def _create_title(self):
        """Créer le titre"""
        title_label = Label(
            self.dialog,
            text="🔒 Vérification requise",
            fg=COLORS['text_primary'],
            bg=COLORS['primary_bg'],
            font=('Segoe UI', 16, 'bold')
        )
        title_label.place(x=70, y=30)
        
        # Ligne décorative
        line = Canvas(
            self.dialog,
            width=250,
            height=2,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        line.place(x=50, y=65)
    
    def _create_password_field(self):
        """Créer le champ mot de passe maître"""
        # Label
        password_label = Label(
            self.dialog,
            text="Mot de passe maître actuel :",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('Segoe UI', 12, 'bold')
        )
        password_label.place(x=40, y=90)
        
        # Entry
        self.password_entry = CustomEntry(self.dialog, show_text=True)
        self.password_entry.place(x=70, y=120, width=200)
        self.password_entry.focus_set()
        
        # Ligne décorative
        password_line = Canvas(
            self.dialog,
            width=200,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        password_line.place(x=70, y=145)
        
        # Icône
        self._add_icon("🔑", x=40, y=120)
        
        # Lier Enter à la vérification
        self.password_entry.bind('<Return>', lambda e: self._on_verify())
    
    def _create_buttons(self):
        """Créer les boutons"""
        # Bouton Vérifier
        verify_btn = CTkButton(
            self.dialog,
            text="✅ Vérifier",
            font=("Segoe UI", 12, "bold"),
            command=self._on_verify,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_success'],
            hover_color='#40c057',
            corner_radius=15,
            width=120,
            height=40,
            border_color="black",
            border_width=1
        )
        verify_btn.place(x=15, y=180)
        
        # Bouton Annuler
        cancel_btn = CTkButton(
            self.dialog,
            text="❌ Annuler",
            font=("Segoe UI", 12, "bold"),
            command=self._close,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_danger'],
            hover_color='#ff5252',
            corner_radius=15,
            width=120,
            height=40,
            border_color="black",
            border_width=1
        )
        cancel_btn.place(x=145, y=180)
    
    def _add_icon(self, icon_text: str, x: int, y: int):
        """Ajouter une icône"""
        try:
            icon_label = Label(
                self.dialog, 
                text=icon_text, 
                bg=COLORS['primary_bg'],
                fg=COLORS['text_accent'],
                font=('Segoe UI', 12)
            )
            icon_label.place(x=x, y=y)
        except Exception as e:
            print(f"Impossible d'ajouter l'icône : {e}")
    
    def _on_verify(self):
        """Vérifier le mot de passe maître"""
        password = self.password_entry.get()
        
        if not password.strip():
            show_error(self.dialog, "Veuillez saisir le mot de passe")
            return
        
        if self.db_manager.verify_master_password(password):
            if self.on_success_callback:
                self.on_success_callback()
            self._close()
        else:
            show_error(self.dialog, MESSAGES['error']['invalid_master'])
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()