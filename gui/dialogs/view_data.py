"""
Dialog pour visualiser les données d'un compte après vérification du mot de passe maître
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas
from PIL import ImageTk, Image

from config.settings import COLORS, WINDOW_CONFIG, IMAGES_DIR
from utils.geometry import GeometryUtils
from gui.widgets.custom_widgets import CustomEntry
from gui.dialogs.master_password import MasterPasswordVerificationDialog
from core.database import DatabaseManager

class ViewDataDialog:
    """Dialog pour visualiser les données d'un compte"""
    
    def __init__(self, parent, account_data):
        self.parent = parent
        self.account_data = account_data
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.site_entry = None
        self.login_entry = None
        self.password_entry = None
        
        # Demander d'abord la vérification du mot de passe maître
        self._verify_master_password()
    
    def _verify_master_password(self):
        """Vérifier le mot de passe maître avant d'afficher les données"""
        verification_dialog = MasterPasswordVerificationDialog(
            self.parent,
            on_success_callback=self._on_master_password_verified,
            title="Confirmation - Master Password"
        )
        verification_dialog.show()
    
    def _on_master_password_verified(self):
        """Callback appelé après vérification réussie du mot de passe maître"""
        self._create_dialog()
        self._setup_ui()
        self._populate_fields()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'], highlightthickness=0)
        config = WINDOW_CONFIG['add_account'].copy()
        config['title'] = 'View Data'
        GeometryUtils.apply_window_config(self.dialog, config)
        
        # Masquer la fenêtre parent
        self.parent.withdraw()
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_site_field()
        self._create_login_field()
        self._create_password_field()
        self._create_close_button()
    
    def _create_site_field(self):
        """Créer le champ site web (lecture seule)"""
        # Label
        site_label = Label(
            self.dialog,
            text="Site Web",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        site_label.place(x=40, y=115)
        
        # Entry en lecture seule
        self.site_entry = CustomEntry(self.dialog, state='readonly')
        self.site_entry.place(x=70, y=149, width=200)
        
        # Ligne décorative
        site_line = Canvas(
            self.dialog,
            width=270,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        site_line.place(x=38, y=174)
        
        # Icône
        self._add_icon("site_icon.png", x=40, y=145)
    
    def _create_login_field(self):
        """Créer le champ nom d'utilisateur (lecture seule)"""
        # Label
        login_label = Label(
            self.dialog,
            text="Username",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        login_label.place(x=40, y=195)
        
        # Entry en lecture seule
        self.login_entry = CustomEntry(self.dialog, state='readonly')
        self.login_entry.place(x=70, y=229, width=200)
        
        # Ligne décorative
        login_line = Canvas(
            self.dialog,
            width=270,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        login_line.place(x=40, y=255)
        
        # Icône
        self._add_icon("login_icon.png", x=40, y=227)
    
    def _create_password_field(self):
        """Créer le champ mot de passe (lecture seule)"""
        # Label
        password_label = Label(
            self.dialog,
            text="Password",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        password_label.place(x=40, y=275)
        
        # Entry en lecture seule
        self.password_entry = CustomEntry(self.dialog, state='readonly')
        self.password_entry.place(x=70, y=309, width=200)
        
        # Ligne décorative
        password_line = Canvas(
            self.dialog,
            width=270,
            height=2.0,
            bg=COLORS['line_color'],
            highlightthickness=0
        )
        password_line.place(x=40, y=336)
        
        # Icône
        self._add_icon("pwd_icon.png", x=40, y=307)
    
    def _create_close_button(self):
        """Créer le bouton de fermeture"""
        from customtkinter import CTkButton
        
        close_btn = CTkButton(
            self.dialog,
            text="Close",
            command=self._close,
            width=165,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            font=("Arial", 10, "bold"),
            corner_radius=20,
            border_color="black",
            border_width=1
        )
        close_btn.place(x=95, y=380)
    
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
    
    def _populate_fields(self):
        """Pré-remplir les champs avec les vraies données du compte"""
        if self.account_data and len(self.account_data) >= 4:
            account_id = self.account_data[3]
            
            try:
                # Récupérer les vraies données depuis la base de données
                accounts = self.db_manager.get_all_accounts()
                account = next((acc for acc in accounts if acc[3] == int(account_id)), None)
                
                if account:
                    site, login, password, _ = account
                    
                    # Activer temporairement les champs pour les remplir
                    self.site_entry.config(state='normal')
                    self.login_entry.config(state='normal')
                    self.password_entry.config(state='normal')
                    
                    # Remplir les champs
                    self.site_entry.insert(0, site)
                    self.login_entry.insert(0, login)
                    self.password_entry.insert(0, password)
                    
                    # Remettre en lecture seule
                    self.site_entry.config(state='readonly')
                    self.login_entry.config(state='readonly')
                    self.password_entry.config(state='readonly')
                    
            except Exception as e:
                print(f"Erreur lors du chargement des données : {e}")
    
    def _close(self):
        """Fermer le dialogue et restaurer la fenêtre parent"""
        if self.dialog:
            self.dialog.destroy()
        self.parent.deiconify()
    
    def show(self):
        """Afficher le dialogue"""
        if self.dialog:
            self.dialog.grab_set()  # Modal
            self.dialog.wait_window()