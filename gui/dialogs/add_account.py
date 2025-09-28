"""
Dialog pour ajouter un nouveau compte
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
        from customtkinter import set_appearance_mode, set_default_color_theme
        
        # Mode sombre par défaut
        set_appearance_mode("dark")
        
        self.dialog = Toplevel(self.parent)
        self.dialog.configure(bg=COLORS['primary_bg'])
        
        config = WINDOW_CONFIG['add_account']
        GeometryUtils.apply_window_config(self.dialog, config)
        
        # Masquer la fenêtre parent
        self.parent.withdraw()
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_site_field()
        self._create_login_field()
        self._create_password_field()
        self._create_buttons()
    
    def _setup_ui(self):
        """Configurer l'interface moderne"""
        from gui.widgets.custom_widgets import ModernCard, ModernLabel, ModernEntry, ModernButton
        
        # Card principale
        main_card = ModernCard(self.dialog)
        main_card.place(x=25, y=25, width=300, height=450)
        
        # Titre
        title = ModernLabel(main_card, text="✨ Nouveau Compte", style="title")
        title.place(x=20, y=20)
        
        # Site Web
        ModernLabel(main_card, text="🌐 Site Web", style="subtitle").place(x=20, y=80)
        self.site_entry = ModernEntry(main_card, placeholder_text="ex: google.com")
        self.site_entry.place(x=20, y=110, width=260)
        
        # Username  
        ModernLabel(main_card, text="👤 Nom d'utilisateur", style="subtitle").place(x=20, y=160)
        self.login_entry = ModernEntry(main_card, placeholder_text="Votre nom d'utilisateur")
        self.login_entry.place(x=20, y=190, width=260)
        
        # Password
        ModernLabel(main_card, text="🔐 Mot de passe", style="subtitle").place(x=20, y=240)
        self.password_entry = ModernEntry(main_card, placeholder_text="Mot de passe sécurisé", show="*")
        self.password_entry.place(x=20, y=270, width=220)
        
        # Bouton générateur
        gen_btn = ModernButton(
            main_card,
            text="🎲",
            command=self._generate_password,
            width=30,
            height=35,
            style="secondary"
        )
        gen_btn.place(x=250, y=270)
        
        # Boutons d'action
        save_btn = ModernButton(
            main_card,
            text="💾 Sauvegarder",
            command=self._on_save,
            style="success",
            width=120
        )
        save_btn.place(x=20, y=380)
        
        cancel_btn = ModernButton(
            main_card,
            text="❌ Annuler", 
            command=self._on_back,
            style="danger",
            width=120
        )
        cancel_btn.place(x=160, y=380)
    
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