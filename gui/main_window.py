"""
Fenêtre principale de l'application Password Manager
"""

import tkinter as tk
from tkinter import PhotoImage, Label, Canvas
from PIL import ImageTk, Image
from customtkinter import CTkButton

from config.settings import WINDOW_CONFIG, COLORS, IMAGES_DIR
from utils.geometry import GeometryUtils
from core.database import DatabaseManager
from gui.widgets.account_table import AccountTable
from gui.widgets.custom_widgets import show_error, show_success
from gui.dialogs.add_account import AddAccountDialog

class PasswordManagerApp:
    """Application principale du gestionnaire de mots de passe"""
    
    def __init__(self):
        self.root = None
        self.db_manager = DatabaseManager()
        self.account_table = None
        self.current_count = 1
        
        self._initialize_app()
    
    def _initialize_app(self):
        """Initialiser l'application"""
        self.root = tk.Tk()
        self._setup_main_window()
        self._setup_ui()
        self._load_accounts()
    
    def _setup_main_window(self):
        """Configurer la fenêtre principale"""
        config = WINDOW_CONFIG['main']
        self.root.title(config['title'])
        self.root.geometry(GeometryUtils.center_window(
            self.root, config['width'], config['height']
        ))
        self.root.minsize(config['width'], config['height'])
        self.root.maxsize(config['width'], config['height'])
        self.root.resizable(*config['resizable'])
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_background()
        self._create_decorative_elements()
        self._create_account_table()
        self._create_action_buttons()
    
    def _create_background(self):
        """Créer les éléments de fond"""
        # Canvas de gauche (barre latérale)
        canvas_bg1 = Canvas(
            self.root,
            width=225,
            height=500,
            bg=COLORS['primary_bg'],
            borderwidth=0,
            highlightthickness=0
        )
        canvas_bg1.place(x=0, y=0)
        
        # Canvas principal
        canvas_bg2 = Canvas(
            self.root,
            width=1000,
            height=500,
            bg=COLORS['secondary_bg'],
            highlightthickness=0
        )
        canvas_bg2.place(x=225, y=0)
        
        # Canvas pour les boutons
        self.canvas_btn = Canvas(
            self.root,
            width=189,
            height=239,
            bg=COLORS['tertiary_bg'],
            highlightthickness=0
        )
        self.canvas_btn.place(x=130, y=130)
        
        # Canvas pour le tableau
        Canvas(
            self.root,
            width=544,
            height=186,
            bg=COLORS['tertiary_bg'],
            highlightthickness=0
        ).place(x=385, y=160)
    
    def _create_decorative_elements(self):
        """Créer les éléments décoratifs"""
        # Bouton paramètres
        try:
            setting_icon = PhotoImage(file=IMAGES_DIR / "icon" / "setting_icon.png")
            CTkButton(
                self.root,
                text='',
                image=setting_icon,
                command=self._open_settings,
                fg_color=COLORS['secondary_bg'],
                hover=False,
                border_width=0
            ).place(x=910, y=5)
        except Exception as e:
            print(f"Impossible de charger l'icône des paramètres : {e}")
        
        # Image décorative (boucle)
        try:
            boucle_img = ImageTk.PhotoImage(Image.open(IMAGES_DIR / "main" / "boucle.png"))
            Label(image=boucle_img, bg=COLORS['secondary_bg']).place(x=620, y=320)
        except Exception as e:
            print(f"Impossible de charger l'image décorative : {e}")
        
        # Nom du projet
        try:
            name_img = PhotoImage(file=IMAGES_DIR / "main" / "main_name.png")
            Label(image=name_img, bg=COLORS['secondary_bg']).place(x=500, y=90)
        except Exception as e:
            print(f"Impossible de charger le nom du projet : {e}")
    
    def _create_account_table(self):
        """Créer le tableau des comptes"""
        self.account_table = AccountTable(self.root, on_view_data=self._view_account_data)
        self.account_table.place(x=410, y=180)
    
    def _create_action_buttons(self):
        """Créer les boutons d'action"""
        # Bouton Ajouter
        try:
            add_icon = PhotoImage(file=IMAGES_DIR / "icon" / "add_icon.png")
        except:
            add_icon = None
        
        add_btn = CTkButton(
            self.canvas_btn,
            text="Add Account",
            font=("Arial", 10, "bold"),
            command=self._add_account,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15,
            width=165,
            border_color="black",
            border_width=1,
            image=add_icon if add_icon else None
        )
        add_btn.place(x=11, y=30)
        
        # Bouton Supprimer
        try:
            remove_icon = PhotoImage(file=IMAGES_DIR / "icon" / "remove_icon.png")
        except:
            remove_icon = None
        
        remove_btn = CTkButton(
            self.canvas_btn,
            text="Supp Account",
            font=("Arial", 10, "bold"),
            command=self._remove_account,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15,
            width=165,
            border_color="black",
            border_width=1,
            image=remove_icon if remove_icon else None
        )
        remove_btn.place(x=11, y=105)
        
        # Bouton Éditer
        try:
            edit_icon = PhotoImage(file=IMAGES_DIR / "icon" / "edit_icon.png")
        except:
            edit_icon = None
        
        edit_btn = CTkButton(
            self.canvas_btn,
            text="Edit Account",
            font=("Arial", 10, "bold"),
            command=self._edit_account,
            text_color=COLORS['text_primary'],
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            corner_radius=15,
            width=165,
            border_color="black",
            border_width=1,
            image=edit_icon if edit_icon else None
        )
        edit_btn.place(x=11, y=180)
    
    def _load_accounts(self):
        """Charger les comptes depuis la base de données"""
        try:
            accounts = self.db_manager.get_all_accounts()
            self.account_table.load_accounts(accounts)
            # Mettre à jour le compteur
            if accounts:
                self.current_count = max(account[3] for account in accounts) + 1
        except Exception as e:
            print(f"Erreur lors du chargement des comptes : {e}")
            show_error(self.root, "Erreur lors du chargement des comptes")
    
    def _add_account(self):
        """Ouvrir le dialogue d'ajout de compte"""
        dialog = AddAccountDialog(self.root, self._on_account_saved)
        dialog.show()
    
    def _on_account_saved(self, site: str, login: str, password: str):
        """
        Callback appelé quand un compte est sauvegardé
        
        Args:
            site: Nom du site
            login: Nom d'utilisateur  
            password: Mot de passe
        """
        try:
            # Sauvegarder en base
            account_id = self.db_manager.create_account(site, login, password)
            
            # Ajouter au tableau
            self.account_table.insert_account(site, login, password, account_id)
            
            self.current_count += 1
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            raise
    
    def _remove_account(self):
        """Supprimer le compte sélectionné"""
        account_id = self.account_table.get_selected_id()
        
        if not account_id:
            show_error(self.root, "Veuillez sélectionner un compte à supprimer")
            return
        
        try:
            # Supprimer de la base de données
            self.db_manager.delete_account(int(account_id))
            
            # Supprimer du tableau
            self.account_table.remove_selected()
            
            show_success(self.root, "Le compte a été supprimé")
            
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
            show_error(self.root, "Erreur lors de la suppression du compte")
    
    def _edit_account(self):
        """Éditer le compte sélectionné"""
        selected_data = self.account_table.get_selected_data()
        
        if not selected_data:
            show_error(self.root, "Veuillez sélectionner un compte à modifier")
            return
        
        from gui.dialogs.edit_account import EditAccountDialog
        dialog = EditAccountDialog(self.root, selected_data, self._on_account_edited)
        dialog.show()
    
    def _on_account_edited(self, account_id: int, site: str, login: str, password: str):
        """
        Callback appelé quand un compte est édité
        
        Args:
            account_id: ID du compte
            site: Nouveau nom du site
            login: Nouveau nom d'utilisateur  
            password: Nouveau mot de passe
        """
        try:
            # Mettre à jour en base
            self.db_manager.update_account(account_id, site, login, password)
            
            # Mettre à jour dans le tableau
            self.account_table.update_account(str(account_id), site, login, password)
            
            show_success(self.root, "Le compte a été mis à jour")
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour : {e}")
            raise
    
    def _view_account_data(self, account_data):
        """
        Afficher les données d'un compte
        
        Args:
            account_data: Données du compte sélectionné
        """
        from gui.dialogs.view_data import ViewDataDialog
        dialog = ViewDataDialog(self.root, account_data)
        dialog.show()
    
    def _open_settings(self):
        """Ouvrir le dialogue des paramètres"""
        from gui.dialogs.settings import SettingsDialog
        dialog = SettingsDialog(self.root)
        dialog.show()
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()