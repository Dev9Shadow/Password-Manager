"""
Fonctions de validation des données
"""

from typing import Tuple, Optional
from config.settings import VALIDATION, MESSAGES

class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""
    pass

class Validator:
    """Validateur de données pour le password manager"""
    
    @staticmethod
    def validate_account_data(site: str, login: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Valider les données d'un compte
        
        Args:
            site: Nom du site
            login: Nom d'utilisateur
            password: Mot de passe
            
        Returns:
            Tuple (is_valid, error_message)
        """
        # Vérifier que les champs ne sont pas vides
        if not site or len(site.strip()) <= 1:
            return False, MESSAGES['error']['fill_fields']
        
        if not login or len(login.strip()) < VALIDATION['min_username_length']:
            return False, MESSAGES['error']['username_length']
        
        if not password or len(password.strip()) <= 1:
            return False, MESSAGES['error']['fill_fields']
        
        return True, None
    
    @staticmethod
    def validate_master_password(password: str, confirmation: str) -> Tuple[bool, Optional[str]]:
        """
        Valider un mot de passe maître et sa confirmation
        
        Args:
            password: Mot de passe maître
            confirmation: Confirmation du mot de passe
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if password != confirmation:
            return False, MESSAGES['error']['invalid_credentials']
        
        if len(password) < VALIDATION['min_password_length']:
            return False, MESSAGES['error']['invalid_credentials']
        
        return True, None
    
    @staticmethod
    def validate_field_not_empty(value: str, field_name: str = "champ") -> Tuple[bool, Optional[str]]:
        """
        Valider qu'un champ n'est pas vide
        
        Args:
            value: Valeur à valider
            field_name: Nom du champ pour le message d'erreur
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, f"Le {field_name} ne peut pas être vide"
        
        return True, None
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """
        Nettoyer une entrée utilisateur
        
        Args:
            value: Valeur à nettoyer
            
        Returns:
            Valeur nettoyée
        """
        if not value:
            return ""
        
        return value.strip()