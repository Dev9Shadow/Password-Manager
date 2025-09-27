"""
Utilitaires pour la géométrie des fenêtres
"""

import tkinter as tk

class GeometryUtils:
    """Utilitaires pour le positionnement des fenêtres"""
    
    @staticmethod
    def center_window(window: tk.Tk, width: int, height: int) -> str:
        """
        Centrer une fenêtre sur l'écran
        
        Args:
            window: Fenêtre à centrer
            width: Largeur de la fenêtre
            height: Hauteur de la fenêtre
            
        Returns:
            String de géométrie formatée
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        return f'{width}x{height}+{x}+{y}'
    
    @staticmethod
    def center_on_parent(parent: tk.Tk, width: int, height: int) -> str:
        """
        Centrer une fenêtre sur sa fenêtre parent
        
        Args:
            parent: Fenêtre parent
            width: Largeur de la nouvelle fenêtre
            height: Hauteur de la nouvelle fenêtre
            
        Returns:
            String de géométrie formatée
        """
        parent.update_idletasks()
        
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        return f'{width}x{height}+{x}+{y}'
    
    @staticmethod
    def apply_window_config(window: tk.Toplevel, config: dict):
        """
        Appliquer une configuration de fenêtre
        
        Args:
            window: Fenêtre à configurer
            config: Configuration contenant width, height, title, resizable
        """
        width = config.get('width', 400)
        height = config.get('height', 300)
        title = config.get('title', 'Window')
        resizable = config.get('resizable', (True, True))
        
        window.title(title)
        window.geometry(GeometryUtils.center_window(window, width, height))
        window.minsize(width, height)
        window.maxsize(width, height)
        window.resizable(*resizable)