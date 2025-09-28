"""
Fenêtre principale - Version corrigée et moderne
"""

import tkinter as tk
from tkinter import Canvas, Label
from customtkinter import CTkButton
import customtkinter as ctk

from config.settings import WINDOW_CONFIG, COLORS
from utils.geometry import GeometryUtils
from core.database import DatabaseManager
from gui.widgets.account_table import AccountTable
from gui.widgets.custom_widgets import show_error, show_success

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
        # Configurer CustomTkinter
        ctk.set_appearance_mode("dark")
        
        self.root = ctk.CTk()  # Utiliser CTk au lieu de Tk
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
        
        # Couleur de fond moderne
        self.root.configure(fg_color=COLORS['primary_bg'])
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        self._create_background()
        self._create_header()
        self._create_account_table()
        self._create_action_buttons()
    
    def _create_background(self):
        """Créer les éléments de fond modernes"""
        # Panel gauche pour les boutons
        self.left_panel = ctk.CTkFrame(
            self.root,
            width=220,
            height=460,
            fg_color=COLORS['secondary_bg'],
            corner_radius=15
        )
        self.left_panel.place(x=20, y=20)
        
        # Panel principal pour le contenu
        self.main_panel = ctk.CTkFrame(
            self.root,
            width=740,
            height=460,
            fg_color=COLORS['tertiary_bg'],
            corner_radius=15
        )
        self.main_panel.place(x=260, y=20)
    
    def _create_header(self):
        """Créer le header moderne"""
        # Titre principal
        title = ctk.CTkLabel(
            self.main_panel,
            text="🔐 Password Vault",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.place(x=30, y=20)
        
        # Sous-titre
        subtitle = ctk.CTkLabel(
            self.main_panel,
            text="Gestionnaire sécurisé de mots de passe",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS['text_secondary']
        )
        subtitle.place(x=30, y=55)
        
        # Bouton paramètres
        settings_btn = ctk.CTkButton(
            self.main_panel,
            text="⚙️ Settings",
            width=100,
            height=30,
            command=self._open_settings,
            fg_color=COLORS['button_secondary'],
            hover_color=COLORS['button_primary']
        )
        settings_btn.place(x=620, y=25)
    
    def _create_account_table(self):
        """Créer le tableau des comptes"""
        try:
            # Frame pour le tableau
            table_frame = ctk.CTkFrame(
                self.main_panel,
                width=680,
                height=320,
                fg_color=COLORS['card_bg'],
                corner_radius=10
            )
            table_frame.place(x=30, y=100)
            
            self.account_table = AccountTable(table_frame, on_view_data=self._view_account_data)
            self.account_table.place(x=20, y=20, width=810, height=360)
            
        except Exception as e:
            print(f"Erreur lors de la création du tableau : {e}")
            self.account_table = None
    
    def _create_action_buttons(self):
        """Créer les boutons d'action"""
        # Titre de la section
        section_title = ctk.CTkLabel(
            self.left_panel,
            text="Actions",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        section_title.place(x=20, y=20)
        
        # Configuration des boutons
        buttons = [
            {
                "text": "➕ Ajouter",
                "command": self._add_account,
                "y": 70,
                "fg_color": COLORS['button_primary'],
                "hover_color": COLORS['button_hover']
            },
            {
                "text": "🗑️ Supprimer", 
                "command": self._remove_account,
                "y": 130,
                "fg_color": COLORS['button_danger'],
                "hover_color": "#ff5252"
            },
            {
                "text": "✏️ Modifier",
                "command": self._edit_account,
                "y": 190,
                "fg_color": COLORS['button_secondary'],
                "hover_color": COLORS['button_primary']
            },
            {
                "text": "🔍 Rechercher",
                "command": self._search_accounts,
                "y": 250,
                "fg_color": COLORS['button_secondary'],
                "hover_color": COLORS['button_primary']
            }
        ]
        
        for btn_config in buttons:
            try:
                btn = ctk.CTkButton(
                    self.left_panel,
                    text=btn_config["text"],
                    width=180,
                    height=45,
                    command=btn_config["command"],
                    fg_color=btn_config["fg_color"],
                    hover_color=btn_config["hover_color"],
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    corner_radius=10
                )
                btn.place(x=20, y=btn_config["y"])
            except Exception as e:
                print(f"Erreur création bouton : {e}")
    
    # Toutes vos méthodes existantes restent identiques
    def _load_accounts(self):
        """Charger les comptes depuis la base de données"""
        try:
            accounts = self.db_manager.get_all_accounts()
            if self.account_table:
                self.account_table.load_accounts(accounts)
                if accounts:
                    self.current_count = max(account[3] for account in accounts) + 1
        except Exception as e:
            print(f"Erreur lors du chargement des comptes : {e}")

    def _add_account(self):
        """Ouvrir le dialogue d'ajout de compte"""
        try:
            from gui.dialogs.add_account import AddAccountDialog
            dialog = AddAccountDialog(self.root, self._on_account_saved)
            dialog.show()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du dialogue : {e}")

    def _on_account_saved(self, site: str, login: str, password: str):
        """Callback appelé quand un compte est sauvegardé"""
        try:
            account_id = self.db_manager.create_account(site, login, password)
            if self.account_table:
                self.account_table.insert_account(site, login, password, account_id)
            self.current_count += 1
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            raise

    def _remove_account(self):
        """Supprimer le compte sélectionné"""
        if not self.account_table:
            return
            
        account_id = self.account_table.get_selected_id()
        
        if not account_id:
            show_error(self.root, "Veuillez sélectionner un compte à supprimer")
            return
        
        try:
            self.db_manager.delete_account(int(account_id))
            self.account_table.remove_selected()
            show_success(self.root, "Le compte a été supprimé")
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
            show_error(self.root, "Erreur lors de la suppression du compte")

    def _edit_account(self):
        """Éditer le compte sélectionné"""
        if not self.account_table:
            return
            
        selected_data = self.account_table.get_selected_data()
        
        if not selected_data:
            show_error(self.root, "Veuillez sélectionner un compte à modifier")
            return
        
        # Récupérer les vraies données depuis la base de données (non masquées)
        try:
            account_id = selected_data[3]
            accounts = self.db_manager.get_all_accounts()
            account = next((acc for acc in accounts if acc[3] == int(account_id)), None)
            
            if account:
                # Ouvrir le dialogue d'édition avec les vraies données
                from gui.dialogs.edit_account import EditAccountDialog
                dialog = EditAccountDialog(self.root, account, self._on_account_edited)
                dialog.show()
            else:
                show_error(self.root, "Compte introuvable")
                
        except Exception as e:
            print(f"Erreur lors de l'ouverture du dialogue d'édition : {e}")
            show_error(self.root, "Erreur lors de l'ouverture du dialogue d'édition")

    def _on_account_edited(self, account_id: int, site: str, login: str, password: str):
        """Callback appelé quand un compte est modifié"""
        try:
            self.db_manager.update_account(account_id, site, login, password)
            if self.account_table:
                self.account_table.update_account(str(account_id), site, login, password)
            show_success(self.root, "Le compte a été modifié avec succès")
        except Exception as e:
            print(f"Erreur lors de la modification : {e}")
            show_error(self.root, "Erreur lors de la modification du compte")

    def _view_account_data(self, account_data):
        """Afficher les données d'un compte"""
        print(f"Visualisation du compte : {account_data}")  # Placeholder

    def _open_settings(self):
        """Ouvrir le dialogue des paramètres"""
        try:
            from gui.dialogs.settings import SettingsDialog
            dialog = SettingsDialog(self.root, self._on_settings_changed)
            dialog.show()
        except Exception as e:
            print(f"Erreur lors de l'ouverture des paramètres : {e}")
            show_error(self.root, "Erreur lors de l'ouverture des paramètres")

    def _on_settings_changed(self, settings):
        """Callback appelé quand les paramètres sont modifiés"""
        try:
            print(f"Paramètres modifiés : {settings}")
            
            # Ici vous pouvez appliquer les changements en temps réel
            # Par exemple, changer le thème, etc.
            
            # Exemple d'application du thème
            if settings.get('theme') == 'Clair':
                # Appliquer le thème clair
                pass
            elif settings.get('theme') == 'Sombre':
                # Appliquer le thème sombre (par défaut)
                pass
            
            show_success(self.root, "Paramètres appliqués !")
            
        except Exception as e:
            print(f"Erreur lors de l'application des paramètres : {e}")
            show_error(self.root, "Erreur lors de l'application des paramètres")

    def _search_accounts(self):
        """Fonction de recherche"""
        try:
            from gui.dialogs.search_accounts import SearchAccountsDialog
            dialog = SearchAccountsDialog(self.root, self._on_search_results)
            dialog.show()
        except Exception as e:
            print(f"Erreur lors de l'ouverture de la recherche : {e}")
            
    def _on_search_results(self, filtered_accounts, search_term):
        """Callback appelé avec les résultats de recherche"""
        try:
            if self.account_table:
                self.account_table.load_accounts(filtered_accounts)
                
                # Mettre à jour le statut
                if search_term:
                    result_count = len(filtered_accounts)
                    if result_count == 0:
                        self._update_search_status(f"Aucun résultat pour '{search_term}'")
                        show_error(self.root, f"Aucun résultat trouvé pour '{search_term}'")
                    else:
                        self._update_search_status(f"{result_count} résultat(s) pour '{search_term}'")
                else:
                    self._update_search_status("")
                    
        except Exception as e:
            print(f"Erreur lors de l'affichage des résultats : {e}")
    
    def _create_search_status_label(self):
        """Créer un label pour afficher le statut de recherche"""
        self.search_status_label = ctk.CTkLabel(
            self.main_panel,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLORS['text_secondary']
        )
        self.search_status_label.place(x=30, y=75)

    def _update_search_status(self, message):
        """Mettre à jour le statut de recherche"""
        if hasattr(self, 'search_status_label'):
            self.search_status_label.configure(text=message)
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()