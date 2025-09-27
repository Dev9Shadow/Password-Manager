"""
Gestionnaire de base de données pour le password manager
"""

import sqlite3
from typing import List, Tuple, Optional
from pathlib import Path
import logging

from config.settings import DATABASE_PATH
from core.encryption import EncryptionManager

class DatabaseManager:
    """Gestionnaire de la base de données SQLite"""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self.encryption = EncryptionManager()
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialiser la base de données avec les tables nécessaires"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table des comptes
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        site TEXT NOT NULL,
                        login TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                """)
                
                # Table pour le mot de passe maître
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS MasterPassword (
                        id INTEGER PRIMARY KEY,
                        password_hash TEXT NOT NULL
                    )
                """)
                
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de l'initialisation de la base de données : {e}")
            raise
    
    def create_account(self, site: str, login: str, password: str) -> int:
        """
        Créer un nouveau compte
        
        Args:
            site: Nom du site
            login: Nom d'utilisateur
            password: Mot de passe
            
        Returns:
            ID du compte créé
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Accounts (site, login, password)
                    VALUES (?, ?, ?)
                """, (
                    self.encryption.encrypt(site),
                    self.encryption.encrypt(login),
                    self.encryption.encrypt(password)
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la création du compte : {e}")
            raise
    
    def get_all_accounts(self) -> List[Tuple[str, str, str, int]]:
        """
        Récupérer tous les comptes
        
        Returns:
            Liste des comptes (site, login, password, id)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT site, login, password, id FROM Accounts")
                accounts = cursor.fetchall()
                
                # Décrypter les données
                decrypted_accounts = []
                for site, login, password, account_id in accounts:
                    decrypted_accounts.append((
                        self.encryption.decrypt(site) if site else site,
                        self.encryption.decrypt(login) if login else login,
                        self.encryption.decrypt(password) if password else password,
                        account_id
                    ))
                
                return decrypted_accounts
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la récupération des comptes : {e}")
            return []
    
    def update_account(self, account_id: int, site: str, login: str, password: str):
        """
        Mettre à jour un compte
        
        Args:
            account_id: ID du compte
            site: Nouveau nom du site
            login: Nouveau nom d'utilisateur
            password: Nouveau mot de passe
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Accounts 
                    SET site = ?, login = ?, password = ?
                    WHERE id = ?
                """, (
                    self.encryption.encrypt(site),
                    self.encryption.encrypt(login),
                    self.encryption.encrypt(password),
                    account_id
                ))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour du compte : {e}")
            raise
    
    def delete_account(self, account_id: int):
        """
        Supprimer un compte
        
        Args:
            account_id: ID du compte à supprimer
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Accounts WHERE id = ?", (account_id,))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la suppression du compte : {e}")
            raise
    
    def set_master_password(self, password: str):
        """
        Définir ou mettre à jour le mot de passe maître
        
        Args:
            password: Nouveau mot de passe maître
        """
        try:
            hashed_password = self.encryption.hash_password(password)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO MasterPassword (id, password_hash)
                    VALUES (1, ?)
                """, (hashed_password,))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la définition du mot de passe maître : {e}")
            raise
    
    def verify_master_password(self, password: str) -> bool:
        """
        Vérifier le mot de passe maître
        
        Args:
            password: Mot de passe à vérifier
            
        Returns:
            True si le mot de passe est correct
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password_hash FROM MasterPassword WHERE id = 1")
                result = cursor.fetchone()
                
                if result:
                    return self.encryption.verify_password(password, result[0])
                return False
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la vérification du mot de passe maître : {e}")
            return False
    
    def has_master_password(self) -> bool:
        """
        Vérifier si un mot de passe maître existe
        
        Returns:
            True si un mot de passe maître existe
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM MasterPassword WHERE id = 1")
                count = cursor.fetchone()[0]
                return count > 0
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la vérification de l'existence du mot de passe maître : {e}")
            return False