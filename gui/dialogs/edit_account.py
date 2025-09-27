"""
Dialog pour éditer un compte existant
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas, PhotoImage
from PIL import ImageTk, Image
from customtkinter import CTkButton

from config.settings import COLORS, WINDOW_CONFIG, IMAGES_DIR
from utils.geometry import GeometryUtils
from utils.validators import Validator
from gui.widgets.custom_widgets import CustomEntry, show_error
from core.password_generator import PasswordGenerator

class EditAccountDialog:
    """Dialog pour éditer un compte existant"""
    
    def __init__(self, parent, account_data, on_save_callback=None):
        self.parent = parent
        self.account_data = account_data  # (site, login, password, id)
        self.on_save_callback = on_save_callback
        self.validator = Validator()
        self.password_generator = PasswordGenerator()
        
        self.dialog = None
        self.site_entry = None
        self.login_entry = None
        self.password_entry = None
        
        self._create_dialog()
        self._setup_ui()
        self._populate_fields()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        self.dialog = Toplevel(self.parent, bg=COLORS['primary_bg'], highlightthickness=0)
        config = WINDOW_CONFIG['edit_account']
        GeometryUtils.apply_window_config(self.dialog, config)
        
        # Masquer la fenêtre parent
        self.parent.withdraw()
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_site_field()
        self._create_login_field()
        self._create_password_field()
        self._create_buttons()
    
    def _create_site_field(self):
        """Créer le champ site web"""
        # Label
        site_label = Label(
            self.dialog,
            text="Site Web",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        site_label.place(x=40, y=115)
        
        # Entry
        self.site_entry = CustomEntry(self.dialog)
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
        """Créer le champ nom d'utilisateur"""
        # Label
        login_label = Label(
            self.dialog,
            text="Username",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        login_label.place(x=40, y=195)
        
        # Entry
        self.login_entry = CustomEntry(self.dialog)
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
        """Créer le champ mot de passe"""
        # Label
        password_label = Label(
            self.dialog,
            text="Password",
            fg=COLORS['text_secondary'],
            bg=COLORS['primary_bg'],
            font=('yu gothic ui', 13, 'bold')
        )
        password_label.place(x=40, y=275)
        
        # Entry
        self.password_entry = CustomEntry(self.dialog)
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
        
        # Bouton générateur de mot de passe
        try:
            generate_icon = PhotoImage(file=IMAGES_DIR / "icon" / "generate_icon.png")
            generate_btn = CTkButton(
                self.dialog,
                text='',
                image=generate_icon,
                command=self._generate_password,
                width=24,
                height=24,
                fg_color=COLORS['primary_bg'],
                hover_color=COLORS['primary_bg']
            )
            generate_btn.place(x=310, y=309)
        except Exception as e:
            print(f"Impossible de charger l'icône de génération : {e}")
    
    def _create_buttons(self):
        """Créer les boutons d'action"""
        # Bouton retour
        try:
            back_icon = PhotoImage(file=IMAGES_DIR / "icon" / "back_icon.png")
            back_btn = CTkButton(
                self.dialog,
                text='',
                image=back_icon,
                command=self._on_back,
                width=24,
                height=24,
                fg_color=COLORS['primary_bg'],
                hover_color=COLORS['primary_bg']
            )
            back_btn.place(x=5, y=5)
        except Exception as e:
            print(f"Impossible de charger l'icône de retour : {e}")
        
        # Bouton sauvegarder
        save_btn = CTkButton(
            self.dialog,
            text="Save Account",
            command=self._on_save,
            width=165,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            font=("Arial", 10, "bold"),
            corner_radius=20,
            border_color="black",
            border_width=1
        )
        save_btn.place(x=95, y=380)
    
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
        """Pré-remplir les champs avec les données existantes"""
        if self.account_data and len(self.account_data) >= 3:
            # Récupérer les vraies données (non masquées) depuis la base de données
            # Pour l'instant, on utilise les données fournies
            site = self.account_data[0] if self.account_data[0] else ""
            login = self.account_data[1] if self.account_data[1] else ""
            # Le mot de passe est masqué dans le tableau, il faudra le récupérer de la DB
            
            self.site_entry.insert(0, site)
            self.login_entry.insert(0, login)
            # Ne pas pré-remplir le mot de passe pour des raisons de sécurité
    
    def _generate_password(self):
        """Générer un mot de passe aléatoire"""
        password = self.password_generator.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
    
    def _on_save(self):
        """Gestionnaire du bouton sauvegarder"""
        # Récupérer les valeurs
        site = self.site_entry.get().strip()
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Si le mot de passe est vide, garder l'ancien
        if not password and len(self.account_data) >= 3:
            password = self.account_data[2]  # Mot de passe original
        
        # Valider les données
        is_valid, error_message = self.validator.validate_account_data(site, login, password)
        
        if not is_valid:
            show_error(self.dialog, error_message)
            return
        
        # Appeler le callback de sauvegarde
        if self.on_save_callback:
            try:
                account_id = self.account_data[3] if len(self.account_data) > 3 else None
                self.on_save_callback(account_id, site, login, password)
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