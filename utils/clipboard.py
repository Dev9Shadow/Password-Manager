"""
Gestionnaire du presse-papiers
"""

import pyperclip
import logging

class ClipboardManager:
    """Gestionnaire des opérations de presse-papiers"""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Copier du texte dans le presse-papiers
        
        Args:
            text: Texte à copier
            
        Returns:
            True si la copie a réussi
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la copie : {e}")
            return False
    
    @staticmethod
    def get_from_clipboard() -> str:
        """
        Récupérer le contenu du presse-papiers
        
        Returns:
            Contenu du presse-papiers
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du presse-papiers : {e}")
            return ""
    
    @staticmethod
    def clear_clipboard():
        """Vider le presse-papiers"""
        try:
            pyperclip.copy("")
        except Exception as e:
            logging.error(f"Erreur lors du vidage du presse-papiers : {e}")