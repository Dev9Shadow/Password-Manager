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
        self._create_password_field()
        self._create_confirmation_field()
        self._create_save_button()
    
    def _create_password_field(self):
        """Créer le champ mot de passe maître"""
        # Label
        password_label = Label(
            self.dialog,
            text="New Master Password",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        password_label.place(x=40, y=115)
        
        # Entry
        self.password_entry = CustomEntry(self.dialog, show_text=True)
        self.password_entry.place(x=70, y=149, width=200)
        
        # Ligne décorative
        password_line = Canvas(
            self.dialog,
            width=270,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        password_line.place(x=38, y=174)
        
        # Icône
        self._add_icon("masterpwd_icon.png", x=40, y=145)
    
    def _create_confirmation_field(self):
        """Créer le champ de confirmation"""
        # Label
        confirmation_label = Label(
            self.dialog,
            text="Confirmation",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        confirmation_label.place(x=40, y=195)
        
        # Entry
        self.confirmation_entry = CustomEntry(self.dialog, show_text=True)
        self.confirmation_entry.place(x=70, y=229, width=200)
        
        # Ligne décorative
        confirmation_line = Canvas(
            self.dialog,
            width=270,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        confirmation_line.place(x=40, y=255)
        
        # Icône
        self._add_icon("masterpwd_confirm_icon.png", x=40, y=227)
    
    def _create_save_button(self):
        """Créer le bouton de sauvegarde"""
        save_btn = CTkButton(
            self.dialog,
            text="Save",
            font=("Arial", 10, "bold"),
            command=self._on_save,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15,
            width=165,
            border_color="black",
            border_width=1
        )
        save_btn.place(x=90, y=300)
    
    def _add_icon(self, icon_name: str, x: int, y: int):
        """
        Ajouter une icône à la position spécifiée
        
        Args:
            icon_name: Nom du fichier d'icône
            x, y: Position de l'icône
        """
        try:
            icon_path = IMAGES_DIR / "icon" / icon_name
            if icon_path.exists():
                icon = ImageTk.PhotoImage(Image.open(icon_path))
                icon_label = Label(self.dialog, image=icon, bg=COLORS['primary_bg'])
                icon_label.image = icon  # Garde une référence
                icon_label.place(x=x, y=y)
        except Exception as e:
            print(f"Impossible de charger l'icône {icon_name}: {e}")
    
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
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()

class MasterPasswordVerificationDialog:
    """Dialog pour vérifier le mot de passe maître"""
    
    def __init__(self, parent, on_success_callback=None, title="Confirmation - Master Password"):
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
        GeometryUtils.apply_window_config(self.dialog, config)
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_password_field()
        self._create_ok_button()
    
    def _create_password_field(self):
        """Créer le champ mot de passe maître"""
        # Label
        password_label = Label(
            self.dialog,
            text="Master Password",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        password_label.place(x=40, y=115)
        
        # Entry
        self.password_entry = CustomEntry(self.dialog, show_text=True)
        self.password_entry.place(x=70, y=149, width=200)
        
        # Ligne décorative
        password_line = Canvas(
            self.dialog,
            width=270,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        password_line.place(x=38, y=174)
        
        # Icône
        self._add_icon("masterpwd_icon.png", x=40, y=145)
    
    def _create_ok_button(self):
        """Créer le bouton OK"""
        ok_btn = CTkButton(
            self.dialog,
            text="OK",
            font=("Arial", 10, "bold"),
            command=self._on_verify,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=20,
            width=165,
            border_color="black",
            border_width=1
        )
        ok_btn.place(x=95, y=380)
    
    def _add_icon(self, icon_name: str, x: int, y: int):
        """Ajouter une icône"""
        try:
            icon_path = IMAGES_DIR / "icon" / icon_name
            if icon_path.exists():
                icon = ImageTk.PhotoImage(Image.open(icon_path))
                icon_label = Label(self.dialog, image=icon, bg=COLORS['primary_bg'])
                icon_label.image = icon
                icon_label.place(x=x, y=y)
        except Exception as e:
            print(f"Impossible de charger l'icône {icon_name}: {e}")
    
    def _on_verify(self):
        """Vérifier le mot de passe maître"""
        password = self.password_entry.get()
        
        if self.db_manager.verify_master_password(password):
            if self.on_success_callback:
                self.on_success_callback()
            self._close()
        else:
            show_error(self.dialog, MESSAGES['error']['invalid_master'])
            self.password_entry.delete(0, tk.END)
    
    def _close(self):
        """Fermer le dialogue"""
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()