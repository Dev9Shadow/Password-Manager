"""
Dialog pour rechercher des comptes
"""

import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkButton, CTkEntry, CTkLabel, CTkFrame

from config.settings import COLORS, WINDOW_CONFIG
from utils.geometry import GeometryUtils
from core.database import DatabaseManager

class SearchAccountsDialog:
    """Dialog pour rechercher des comptes"""
    
    def __init__(self, parent, on_search_callback=None):
        self.parent = parent
        self.on_search_callback = on_search_callback
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.search_entry = None
        self.search_type = "all"  # all, site, login
        
        self._create_dialog()
        self._setup_ui()
    
    def _create_dialog(self):
        """Créer la fenêtre de dialogue"""
        ctk.set_appearance_mode("dark")
        
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.configure(fg_color=COLORS['primary_bg'])
        
        self.dialog.title("Rechercher des comptes")
        self.dialog.geometry(GeometryUtils.center_window(self.dialog, 400, 300))
        self.dialog.minsize(400, 300)
        self.dialog.maxsize(400, 300)
        self.dialog.resizable(False, False)
        
        # Masquer la fenêtre parent
        self.parent.withdraw()
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Card principale
        main_card = CTkFrame(
            self.dialog,
            width=360,
            height=260,
            fg_color=COLORS['card_bg'],
            corner_radius=15
        )
        main_card.place(x=20, y=20)
        
        # Titre
        title = CTkLabel(
            main_card,
            text="🔍 Rechercher des Comptes",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.place(x=20, y=20)
        
        # Champ de recherche
        CTkLabel(
            main_card,
            text="Terme de recherche :",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=COLORS['text_accent']
        ).place(x=20, y=70)
        
        self.search_entry = CTkEntry(
            main_card,
            width=320,
            placeholder_text="Tapez votre recherche...",
            fg_color=COLORS['input_bg'],
            border_color=COLORS['input_border'],
            text_color=COLORS['input_text']
        )
        self.search_entry.place(x=20, y=100)
        
        # Options de recherche
        CTkLabel(
            main_card,
            text="Rechercher dans :",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=COLORS['text_accent']
        ).place(x=20, y=140)
        
        # Boutons radio pour le type de recherche
        self.radio_var = tk.StringVar(value="all")
        
        all_radio = ctk.CTkRadioButton(
            main_card,
            text="Tous les champs",
            variable=self.radio_var,
            value="all",
            text_color=COLORS['text_primary']
        )
        all_radio.place(x=20, y=170)
        
        site_radio = ctk.CTkRadioButton(
            main_card,
            text="Site uniquement",
            variable=self.radio_var,
            value="site",
            text_color=COLORS['text_primary']
        )
        site_radio.place(x=150, y=170)
        
        login_radio = ctk.CTkRadioButton(
            main_card,
            text="Login uniquement",
            variable=self.radio_var,
            value="login",
            text_color=COLORS['text_primary']
        )
        login_radio.place(x=270, y=170)
        
        # Boutons d'action
        search_btn = CTkButton(
            main_card,
            text="🔍 Rechercher",
            command=self._on_search,
            fg_color=COLORS['button_primary'],
            hover_color=COLORS['button_hover'],
            width=100
        )
        search_btn.place(x=20, y=210)
        
        clear_btn = CTkButton(
            main_card,
            text="🗑️ Effacer",
            command=self._on_clear,
            fg_color=COLORS['button_secondary'],
            hover_color=COLORS['button_primary'],
            width=100
        )
        clear_btn.place(x=130, y=210)
        
        cancel_btn = CTkButton(
            main_card,
            text="❌ Fermer",
            command=self._on_close,
            fg_color=COLORS['button_danger'],
            hover_color="#ff5252",
            width=100
        )
        cancel_btn.place(x=240, y=210)
    
    def _on_search(self):
        """Effectuer la recherche"""
        search_term = self.search_entry.get().strip().lower()
        search_type = self.radio_var.get()
        
        if not search_term:
            return
        
        try:
            # Récupérer tous les comptes
            all_accounts = self.db_manager.get_all_accounts()
            filtered_accounts = []
            
            for account in all_accounts:
                site, login, password, account_id = account
                
                # Effectuer la recherche selon le type
                if search_type == "all":
                    if (search_term in site.lower() or 
                        search_term in login.lower()):
                        filtered_accounts.append(account)
                elif search_type == "site":
                    if search_term in site.lower():
                        filtered_accounts.append(account)
                elif search_type == "login":
                    if search_term in login.lower():
                        filtered_accounts.append(account)
            
            # Appeler le callback avec les résultats
            if self.on_search_callback:
                self.on_search_callback(filtered_accounts, search_term)
            
            self._close()
            
        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
    
    def _on_clear(self):
        """Effacer les filtres et afficher tous les comptes"""
        if self.on_search_callback:
            try:
                all_accounts = self.db_manager.get_all_accounts()
                self.on_search_callback(all_accounts, "")
                self._close()
            except Exception as e:
                print(f"Erreur lors de l'effacement : {e}")
    
    def _on_close(self):
        """Fermer le dialogue"""
        self._close()
    
    def _close(self):
        """Fermer le dialogue et restaurer la fenêtre parent"""
        self.dialog.destroy()
        self.parent.deiconify()
    
    def show(self):
        """Afficher le dialogue"""
        self.dialog.grab_set()  # Modal
        self.dialog.wait_window()