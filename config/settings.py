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
    # Thème sombre moderne avec gradients
    'primary_bg': '#1a1a2e',           # Bleu très sombre
    'secondary_bg': '#16213e',         # Bleu marine sombre  
    'tertiary_bg': '#0f3460',         # Bleu accent
    'card_bg': '#1e1e2f',             # Cartes/panels
    'sidebar_bg': '#16213e',          # Barre latérale
    
    # Boutons avec effet glassmorphism
    'button_primary': '#4facfe',       # Bleu électrique
    'button_hover': '#00c9ff',         # Cyan vibrant
    'button_secondary': '#667eea',     # Violet doux
    'button_danger': '#ff6b6b',        # Rouge moderne
    'button_success': '#51cf66',       # Vert moderne
    
    # Texte et éléments
    'text_primary': '#ffffff',         # Blanc pur
    'text_secondary': '#a8a8b3',       # Gris clair
    'text_accent': '#4facfe',          # Bleu accent
    'input_text': '#ffffff',           # Texte des inputs en blanc
    'input_bg': '#1e1e2f',            # Fond des inputs
    'input_border': '#4facfe',         # Bordure des inputs
    
    # Accents et effets
    'accent_glow': '#00c9ff',          # Couleur de glow
    'line_color': '#4facfe',           # Lignes décoratives
    'shadow': 'rgba(0, 201, 255, 0.3)', # Ombre avec glow
    
    # Gradients (nouveaux)
    'gradient_primary': ['#4facfe', '#00c9ff'],
    'gradient_secondary': ['#667eea', '#764ba2'],
    'gradient_bg': ['#1a1a2e', '#16213e', '#0f3460']
}

# Version sombre noir et blanc 

# COLORS = {
#     # Thème sombre moderne compatible CustomTkinter
#     'primary_bg': '#212121',          # Gris très sombre
#     'secondary_bg': '#2b2b2b',        # Gris sombre
#     'tertiary_bg': '#333333',         # Gris moyen sombre
#     'card_bg': '#3d3d3d',             # Gris pour les cartes
    
#     # Boutons modernes
#     'button_primary': '#1f538d',      # Bleu CustomTkinter
#     'button_hover': '#14375e',        # Bleu hover
#     'button_secondary': '#565b5e',    # Gris pour boutons secondaires
#     'button_danger': '#d32f2f',       # Rouge pour supprimer
#     'button_success': '#388e3c',      # Vert pour succès
    
#     # Texte
#     'text_primary': '#ffffff',        # Blanc
#     'text_secondary': '#b0b0b0',      # Gris clair
#     'text_accent': '#1f538d',         # Bleu accent
#     'input_text': '#ffffff',
#     'input_bg': '#3d3d3d',
#     'input_border': '#1f538d',
#     'line_color': '#1f538d',
#     'accent': '#1f538d'
# }

VISUAL_EFFECTS = {
    'border_radius': 15,
    'shadow_blur': 10,
    'glow_intensity': 0.3,
    'animation_speed': 200,
    'card_padding': 20,
    'button_hover_scale': 1.05
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