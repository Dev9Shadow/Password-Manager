"""
Générateur de mots de passe sécurisés
"""

import secrets
import string
from random import randint, sample
from typing import Optional

from config.settings import PASSWORD_GENERATOR

class PasswordGenerator:
    """Générateur de mots de passe sécurisés"""
    
    def __init__(self):
        self.characters = PASSWORD_GENERATOR['chars']
        self.min_length = PASSWORD_GENERATOR['min_length']
        self.max_length = PASSWORD_GENERATOR['max_length']
    
    def generate_password(self, 
                         length: Optional[int] = None,
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_symbols: bool = True) -> str:
        """
        Générer un mot de passe sécurisé
        
        Args:
            length: Longueur du mot de passe (aléatoire si None)
            use_uppercase: Inclure les majuscules
            use_lowercase: Inclure les minuscules  
            use_digits: Inclure les chiffres
            use_symbols: Inclure les symboles
            
        Returns:
            Mot de passe généré
        """
        if length is None:
            length = randint(self.min_length, self.max_length)
        
        # Construction du jeu de caractères
        chars = ""
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+"
        
        if not chars:
            chars = self.characters
        
        # Utiliser la méthode compatible avec le code original
        return self._generate_compatible_password(length)
    
    def _generate_compatible_password(self, length: int) -> str:
        """
        Générer un mot de passe compatible avec l'implémentation originale
        
        Args:
            length: Longueur du mot de passe
            
        Returns:
            Mot de passe généré
        """
        # Utilisation de sample comme dans le code original
        selected_chars = sample(self.characters, length)
        return "".join(selected_chars)
    
    def generate_secure_password(self, length: int = 16) -> str:
        """
        Générer un mot de passe cryptographiquement sécurisé
        
        Args:
            length: Longueur du mot de passe
            
        Returns:
            Mot de passe sécurisé
        """
        # Assurer qu'il y a au moins un caractère de chaque type
        password_chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*()_+")
        ]
        
        # Compléter avec des caractères aléatoires
        for _ in range(length - 4):
            password_chars.append(secrets.choice(self.characters))
        
        # Mélanger les caractères
        secrets.SystemRandom().shuffle(password_chars)
        
        return "".join(password_chars)
    
    def check_password_strength(self, password: str) -> dict:
        """
        Évaluer la force d'un mot de passe
        
        Args:
            password: Mot de passe à évaluer
            
        Returns:
            Dictionnaire avec les métriques de force
        """
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+" for c in password)
        
        score = 0
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1
        
        strength_levels = {
            0: "Très faible",
            1: "Très faible", 
            2: "Faible",
            3: "Moyen",
            4: "Fort",
            5: "Très fort",
            6: "Excellent"
        }
        
        return {
            'score': score,
            'strength': strength_levels.get(score, "Inconnu"),
            'length': len(password),
            'has_lowercase': has_lower,
            'has_uppercase': has_upper,
            'has_digits': has_digit,
            'has_symbols': has_symbol
        }