"""
Gestionnaire de chiffrement et de hachage pour le password manager
"""

import hashlib
import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

class EncryptionManager:
    """Gestionnaire des opérations de chiffrement et hachage"""
    
    def __init__(self):
        self._key = None
        self._fernet = None
        self._initialize_key()
    
    def _initialize_key(self):
        """Initialiser la clé de chiffrement"""
        # En production, cette clé devrait être dérivée du mot de passe maître
        # Pour la compatibilité avec le code existant, on utilise une clé fixe
        password = b"default_password"  # À remplacer par le mot de passe maître
        salt = b"salt_"  # En production, utiliser un salt aléatoire stocké
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self._fernet = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Chiffrer une chaîne de caractères
        
        Args:
            data: Données à chiffrer
            
        Returns:
            Données chiffrées encodées en base64
        """
        try:
            if not data:
                return data
            
            encrypted_data = self._fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logging.error(f"Erreur lors du chiffrement : {e}")
            return data  # Retourner les données non chiffrées en cas d'erreur
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Déchiffrer une chaîne de caractères
        
        Args:
            encrypted_data: Données chiffrées en base64
            
        Returns:
            Données déchiffrées
        """
        try:
            if not encrypted_data:
                return encrypted_data
            
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self._fernet.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logging.error(f"Erreur lors du déchiffrement : {e}")
            return encrypted_data  # Retourner les données telles quelles en cas d'erreur
    
    def hash_password(self, password: str) -> str:
        """
        Hacher un mot de passe avec salt
        
        Args:
            password: Mot de passe à hacher
            
        Returns:
            Hash du mot de passe avec salt
        """
        try:
            # Générer un salt aléatoire
            salt = secrets.token_hex(16)
            
            # Créer le hash avec le salt
            pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                         password.encode('utf-8'), 
                                         salt.encode('utf-8'), 
                                         100000)
            
            # Retourner le salt + hash encodé en base64
            return salt + base64.b64encode(pwd_hash).decode('utf-8')
        except Exception as e:
            logging.error(f"Erreur lors du hachage du mot de passe : {e}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Vérifier un mot de passe contre son hash
        
        Args:
            password: Mot de passe à vérifier
            hashed_password: Hash stocké
            
        Returns:
            True si le mot de passe correspond
        """
        try:
            # Extraire le salt (32 premiers caractères)
            salt = hashed_password[:32]
            stored_hash = hashed_password[32:]
            
            # Recalculer le hash avec le même salt
            pwd_hash = hashlib.pbkdf2_hmac('sha256',
                                         password.encode('utf-8'),
                                         salt.encode('utf-8'),
                                         100000)
            
            calculated_hash = base64.b64encode(pwd_hash).decode('utf-8')
            
            return calculated_hash == stored_hash
        except Exception as e:
            logging.error(f"Erreur lors de la vérification du mot de passe : {e}")
            return False
    
    def multi_hashing(self, text: str = "") -> str:
        """
        Fonction de compatibilité avec l'ancien système de hachage
        (pour maintenir la compatibilité avec le code existant)
        
        Args:
            text: Texte à hacher
            
        Returns:
            Hash du texte ou texte original si vide
        """
        if not text:
            return ""
        
        # Utiliser SHA-256 pour la compatibilité
        return hashlib.sha256(text.encode()).hexdigest()