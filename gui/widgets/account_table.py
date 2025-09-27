"""
Widget du tableau des comptes
"""

import tkinter as tk
from tkinter import ttk, Menu
from typing import List, Tuple, Optional, Callable
from utils.clipboard import ClipboardManager

class AccountTable:
    """Widget personnalisé pour afficher les comptes"""
    
    def __init__(self, parent, on_view_data: Callable = None):
        self.parent = parent
        self.on_view_data = on_view_data
        self.clipboard = ClipboardManager()
        self._create_table()
        self._create_context_menu()
    
    def _create_table(self):
        """Créer le tableau des comptes"""
        self.table = ttk.Treeview(
            self.parent, 
            height=6, 
            show="headings", 
            columns=("Site Web", "Login", "Password", "ID")
        )
        
        # Configuration des colonnes
        self.table.column("Site Web", anchor=tk.W, width=123, minwidth=123)
        self.table.column("Login", anchor=tk.W, width=123, minwidth=123)
        self.table.column("Password", anchor=tk.W, width=123, minwidth=123)
        self.table.column("ID", anchor=tk.W, width=123, minwidth=123)
        
        # En-têtes
        self.table.heading("Site Web", text="Site Web", anchor=tk.CENTER)
        self.table.heading("Login", text="Login", anchor=tk.CENTER)
        self.table.heading("Password", text="Password", anchor=tk.CENTER)
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
    
    def _create_context_menu(self):
        """Créer le menu contextuel"""
        self.context_menu = Menu(self.parent, tearoff=0, bg="white", fg="black")
        self.context_menu.add_command(label="Copy Site", command=self._copy_site)
        self.context_menu.add_command(label="Copy Login", command=self._copy_login)
        self.context_menu.add_command(label="Copy Password", command=self._copy_password)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Paste", command=self._paste_data)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="View data", command=self._view_data)
        
        # Lier le menu contextuel
        self.table.bind("<Button-3>", self._show_context_menu)
    
    def _show_context_menu(self, event):
        """Afficher le menu contextuel"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _get_selected_values(self) -> Optional[Tuple]:
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
    
    def _copy_login(self):
        """Copier le login dans le presse-papiers"""
        values = self._get_selected_values()
        if values and len(values) > 1:
            self.clipboard.copy_to_clipboard(values[1])
    
    def _copy_password(self):
        """Copier le mot de passe dans le presse-papiers"""
        values = self._get_selected_values()
        if values and len(values) > 2:
            self.clipboard.copy_to_clipboard(values[2])
    
    def _paste_data(self):
        """Coller des données depuis le presse-papiers"""
        # Cette fonction peut être étendue selon les besoins
        clipboard_content = self.clipboard.get_from_clipboard()
        # Pour l'instant, juste afficher dans la console
        print(f"Contenu du presse-papiers: {clipboard_content}")
    
    def _view_data(self):
        """Afficher les données détaillées"""
        if self.on_view_data:
            selected = self.table.focus()
            if selected:
                values = self.table.item(selected, 'values')
                self.on_view_data(values)
    
    def insert_account(self, site: str, login: str, password: str, account_id: int):
        """
        Insérer un nouveau compte dans le tableau
        
        Args:
            site: Nom du site
            login: Nom d'utilisateur
            password: Mot de passe (affiché masqué)
            account_id: ID du compte
        """
        # Masquer le mot de passe pour l'affichage
        masked_password = "*" * len(password) if password else ""
        
        self.table.insert(
            parent='',
            index='end',
            iid=account_id,
            values=(site, login, masked_password, account_id)
        )
    
    def update_account(self, item_id: str, site: str, login: str, password: str):
        """
        Mettre à jour un compte dans le tableau
        
        Args:
            item_id: ID de l'élément dans le tableau
            site: Nouveau nom du site
            login: Nouveau nom d'utilisateur
            password: Nouveau mot de passe
        """
        masked_password = "*" * len(password) if password else ""
        self.table.item(item_id, values=(site, login, masked_password, item_id))
    
    def remove_selected(self) -> Optional[str]:
        """
        Supprimer l'élément sélectionné
        
        Returns:
            ID de l'élément supprimé ou None
        """
        selected = self.table.focus()
        if selected:
            values = self.table.item(selected, 'values')
            if values:
                self.table.delete(selected)
                return values[3]  # Retourner l'ID
        return None
    
    def get_selected_id(self) -> Optional[str]:
        """
        Récupérer l'ID de l'élément sélectionné
        
        Returns:
            ID de l'élément sélectionné ou None
        """
        selected = self.table.focus()
        if selected:
            values = self.table.item(selected, 'values')
            if values and len(values) > 3:
                return values[3]
        return None
    
    def get_selected_data(self) -> Optional[Tuple]:
        """
        Récupérer toutes les données de l'élément sélectionné
        
        Returns:
            Tuple des données ou None
        """
        return self._get_selected_values()
    
    def clear_all(self):
        """Vider le tableau"""
        for item in self.table.get_children():
            self.table.delete(item)
    
    def load_accounts(self, accounts: List[Tuple[str, str, str, int]]):
        """
        Charger une liste de comptes dans le tableau
        
        Args:
            accounts: Liste des comptes (site, login, password, id)
        """
        self.clear_all()
        for site, login, password, account_id in accounts:
            self.insert_account(site, login, password, account_id)
    
    def place(self, **kwargs):
        """Positionner le tableau"""
        self.table.place(**kwargs)
    
    def pack(self, **kwargs):
        """Empaqueter le tableau"""
        self.table.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Placer le tableau dans une grille"""
        self.table.grid(**kwargs)