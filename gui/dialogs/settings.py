"""
Dialog des paramètres de l'application
"""

import tkinter as tk
from tkinter import Toplevel, PhotoImage
from customtkinter import CTkButton

from config.settings import WINDOW_CONFIG, COLORS, IMAGES_DIR
from utils.geometry import GeometryUtils
from gui.dialogs.master_password import MasterPasswordDialog

class SettingsDialog:
    """Dialog des paramètres de l'application"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent)
        config = WINDOW_CONFIG['settings']
        GeometryUtils.apply_window_config(self.dialog, config)
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_master_password_button()
    
    def _create_master_password_button(self):
        """Créer le bouton de modification du mot de passe maître"""
        try:
            edit_icon = PhotoImage(file=IMAGES_DIR / "icon" / "edit_icon.png")
        except:
            edit_icon = None
        
        master_pwd_btn = CTkButton(
            self.dialog,
            text="Edit Master Password",
            font=("Arial", 13, "bold"),
            command=self._edit_master_password,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15,
            width=200,
            border_color="black",
            border_width=1,
            image=edit_icon if edit_icon else None
        )
        master_pwd_btn.place(x=150, y=50)
    
    def _edit_master_password(self):
        """Ouvrir le dialogue de modification du mot de passe maître"""
        self.dialog.withdraw()
        dialog = MasterPasswordDialog(self.parent, self._on_master_password_changed)
        dialog.show()
        self.dialog.destroy()
    
    def _on_master_password_changed(self):
        """Callback appelé quand le mot de passe maître est changé"""
        # Fermer le dialogue des paramètres
        if self.dialog.winfo_exists():
            self.dialog.destroy()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()