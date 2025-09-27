"""
Configuration globale de l'application
"""

import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
DATABASE_PATH = DATA_DIR / "databasee.db"

# Interface utilisateur
WINDOW_CONFIG = {
    'main': {
        'width': 1000,
        'height': 500,
        'title': 'Password Vault',
        'resizable': (False, False)
    },
    'add_account': {
        'width': 350,
        'height': 500,
        'title': 'Add account',
        'resizable': (False, False)
    },
    'edit_account': {
        'width': 350,
        'height': 500,
        'title': 'Edit Account',
        'resizable': (False, False)
    },
    'settings': {
        'width': 500,
        'height': 500,
        'title': 'Settings',
        'resizable': (False, False)
    },
    'master_password': {
        'width': 350,
        'height': 500,
        'title': 'Settings - Master Password',
        'resizable': (False, False)
    }
}

# Couleurs
COLORS = {
    'primary_bg': '#394054',
    'secondary_bg': '#B0C0D4',
    'tertiary_bg': '#E0E2E8',
    'button_primary': '#004792',
    'button_hover': '#3F7CAF',
    'text_primary': '#CED0C3',
    'text_secondary': '#040405',
    'input_text': '#6B6A69',
    'line_color': '#bdb9b1',
    'accent': '#87CEEB'
}

# Messages
MESSAGES = {
    'error': {
        'invalid_credentials': "L'adresse mail ou le mot de passe est incorrecte",
        'fill_fields': "Veuillez remplir tout les champs",
        'username_length': "Le nom d'utilisateur doit contenir minimum 5 caractères",
        'select_account': "Veuillez selectionner un compte à supprimer",
        'select_account_edit': "Veuillez selectionner un compte à modifier",
        'invalid_master': "Le mot de passe maitre est invalide"
    },
    'success': {
        'master_changed': "Le mot de passe maître à été modifié",
        'account_deleted': "Le compte à été supprimé"
    }
}

# Validation
VALIDATION = {
    'min_username_length': 5,
    'min_password_length': 5
}

# Générateur de mots de passe
PASSWORD_GENERATOR = {
    'chars': "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+",
    'min_length': 5,
    'max_length': 16
}

# S'assurer que les répertoires existent
def ensure_directories():
    """Créer les répertoires nécessaires s'ils n'existent pas"""
    DATA_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)

# Créer les répertoires au moment de l'import
ensure_directories()