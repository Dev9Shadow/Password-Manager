"""
Widget du tableau des comptes - Version corrigée
"""

import tkinter as tk
from tkinter import ttk, Menu
from typing import List, Tuple, Optional
from utils.clipboard import ClipboardManager
from config.settings import COLORS

class AccountTable:
    """Widget personnalisé pour afficher les comptes"""
    
    def __init__(self, parent, on_view_data=None):
        self.parent = parent
        self.on_view_data = on_view_data
        self.clipboard = ClipboardManager()
        self._setup_style()
        self._create_table()
        self._create_context_menu()
    
    def _setup_style(self):
        """Configurer le style moderne du tableau"""
        self.style = ttk.Style()
        
        # Configurer le thème
        self.style.theme_use('clam')
        
        # Style pour le tableau
        self.style.configure(
            "Modern.Treeview",
            background=COLORS['card_bg'],
            foreground=COLORS['text_primary'],
            fieldbackground=COLORS['card_bg'],
            borderwidth=1,
            relief="solid",
            font=('Segoe UI', 10),
            rowheight=25
        )
        
        # Style pour les en-têtes
        self.style.configure(
            "Modern.Treeview.Heading",
            background=COLORS['button_primary'],
            foreground=COLORS['text_primary'],
            relief='flat',
            font=('Segoe UI', 11, 'bold'),
            borderwidth=1
        )
        
        # Couleurs de sélection
        self.style.map('Modern.Treeview',
            background=[('selected', COLORS['button_primary'])],
            foreground=[('selected', COLORS['text_primary'])]
        )
        
        # Style pour la scrollbar
        self.style.configure(
            "Modern.Vertical.TScrollbar",
            background=COLORS['secondary_bg'],
            troughcolor=COLORS['primary_bg'],
            borderwidth=0,
            arrowcolor=COLORS['text_primary'],
            darkcolor=COLORS['button_primary'],
            lightcolor=COLORS['button_primary']
        )
    
    def _create_table(self):
        """Créer le tableau des comptes"""
        # Frame pour contenir le tableau et la scrollbar
        self.table_frame = tk.Frame(self.parent, bg=COLORS['card_bg'])
        
        # Création du tableau avec le style moderne
        self.table = ttk.Treeview(
            self.table_frame,
            height=12,
            show="headings",
            columns=("Site", "Login", "Password", "ID"),
            style="Modern.Treeview"
        )
        
        # Configuration des colonnes
        columns_config = {
            "Site": {"width": 150, "anchor": tk.W, "text": "🌐 Site Web"},
            "Login": {"width": 130, "anchor": tk.W, "text": "👤 Login"},
            "Password": {"width": 100, "anchor": tk.CENTER, "text": "🔐 Password"},
            "ID": {"width": 50, "anchor": tk.CENTER, "text": "🪪 ID"}
        }
        
        for col, config in columns_config.items():
            self.table.column(
                col, 
                width=config["width"], 
                minwidth=config["width"], 
                anchor=config["anchor"]
            )
            self.table.heading(col, text=config["text"], anchor=tk.CENTER)
        
        # Scrollbar moderne
        self.scrollbar = ttk.Scrollbar(
            self.table_frame, 
            orient="vertical", 
            command=self.table.yview,
            style="Modern.Vertical.TScrollbar"
        )
        self.table.configure(yscrollcommand=self.scrollbar.set)
        
        # Placement dans le frame
        self.table.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configuration du redimensionnement
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
    
    def _create_context_menu(self):
        """Créer le menu contextuel moderne"""
        self.context_menu = Menu(
            self.parent, 
            tearoff=0, 
            bg=COLORS['secondary_bg'], 
            fg=COLORS['text_primary'],
            activebackground=COLORS['button_primary'],
            activeforeground=COLORS['text_primary'],
            font=('Segoe UI', 9)
        )
        
        self.context_menu.add_command(label="📋 Copier le Site", command=self._copy_site)
        self.context_menu.add_command(label="📋 Copier le Login", command=self._copy_login)
        self.context_menu.add_command(label="📋 Copier le Password", command=self._copy_password)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="👁️ Voir les données", command=self._view_data)
        
        # Lier le menu contextuel
        self.table.bind("<Button-3>", self._show_context_menu)
    
    def _show_context_menu(self, event):
        """Afficher le menu contextuel"""
        # Sélectionner l'élément sous le curseur
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.table.focus(item)
        
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _get_selected_values(self):
        """Récupérer les valeurs de l'élément sélectionné"""
        selected = self.table.focus()
        if selected:
            return self.table.item(selected, 'values')
        return None
    
    def _copy_site(self):
        """Copier le site dans le presse-papiers"""
        values = self._get_selected_values()
        if values and len(values) > 0:
            self.clipboard.copy_to_clipboard(values[0])
            print(f"Site copié : {values[0]}")
    
    def _copy_login(self):
        """Copier le login dans le presse-papiers"""
        values = self._get_selected_values()
        if values and len(values) > 1:
            self.clipboard.copy_to_clipboard(values[1])
            print(f"Login copié : {values[1]}")
    
    def _copy_password(self):
        """Copier le mot de passe dans le presse-papiers"""
        values = self._get_selected_values()
        if values and len(values) > 2:
            # Le mot de passe est masqué dans l'affichage, il faut le récupérer de la DB
            print("Mot de passe copié (fonctionnalité à implémenter)")
    
    def _view_data(self):
        """Afficher les données détaillées"""
        if self.on_view_data:
            selected = self.table.focus()
            if selected:
                values = self.table.item(selected, 'values')
                self.on_view_data(values)
    
    def insert_account(self, site: str, login: str, password: str, account_id: int):
        """Insérer un nouveau compte dans le tableau"""
        # Masquer le mot de passe pour l'affichage
        masked_password = "•" * min(8, len(password)) if password else ""
        
        self.table.insert(
            parent='',
            index='end',
            iid=str(account_id),
            values=(site, login, masked_password, account_id)
        )
    
    def update_account(self, item_id: str, site: str, login: str, password: str):
        """Mettre à jour un compte dans le tableau"""
        masked_password = "•" * min(8, len(password)) if password else ""
        self.table.item(item_id, values=(site, login, masked_password, item_id))
    
    def remove_selected(self):
        """Supprimer l'élément sélectionné"""
        selected = self.table.focus()
        if selected:
            values = self.table.item(selected, 'values')
            if values:
                self.table.delete(selected)
                return values[3]
        return None
    
    def get_selected_id(self):
        """Récupérer l'ID de l'élément sélectionné"""
        selected = self.table.focus()
        if selected:
            values = self.table.item(selected, 'values')
            if values and len(values) > 3:
                return values[3]
        return None
    
    def get_selected_data(self):
        """Récupérer toutes les données de l'élément sélectionné"""
        return self._get_selected_values()
    
    def clear_all(self):
        """Vider le tableau"""
        for item in self.table.get_children():
            self.table.delete(item)
    
    def load_accounts(self, accounts):
        """Charger une liste de comptes dans le tableau"""
        self.clear_all()
        for site, login, password, account_id in accounts:
            self.insert_account(site, login, password, account_id)
    
    def place(self, **kwargs):
        """Positionner le tableau"""
        # Ajuster la taille par défaut si non spécifiée
        if 'width' not in kwargs:
            kwargs['width'] = 900
        if 'height' not in kwargs:
            kwargs['height'] = 300
            
        self.table_frame.place(**kwargs)
    
    def pack(self, **kwargs):
        """Empaqueter le tableau"""
        self.table_frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Placer le tableau dans une grille"""
        self.table_frame.grid(**kwargs)