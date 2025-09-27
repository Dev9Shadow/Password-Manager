# Password Manager

Un gestionnaire de mots de passe sécurisé développé en Python avec une interface graphique moderne.

## ✨ Fonctionnalités

- 🔐 **Chiffrement sécurisé** : Tous les mots de passe sont chiffrés avant stockage
- 🔑 **Mot de passe maître** : Protection par mot de passe maître avec hachage sécurisé
- ➕ **Gestion des comptes** : Ajout, modification et suppression de comptes
- 🎲 **Générateur de mots de passe** : Génération automatique de mots de passe sécurisés
- 📋 **Presse-papiers** : Copie rapide des informations dans le presse-papiers
- 🎨 **Interface moderne** : Interface utilisateur élégante avec CustomTkinter
- 💾 **Base de données SQLite** : Stockage local sécurisé

## 🚀 Installation

### Prérequis

- Python 3.7 ou plus récent
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Dépendances principales

- `customtkinter` : Interface utilisateur moderne
- `pillow` : Gestion des images
- `cryptography` : Chiffrement des données
- `pyperclip` : Gestion du presse-papiers

## 📁 Structure du projet

```
password_manager/
│
├── main.py                     # Point d'entrée principal
├── requirements.txt            # Dépendances
├── config/
│   └── settings.py            # Configuration globale
├── core/
│   ├── database.py            # Gestionnaire de base de données
│   ├── encryption.py          # Fonctions de chiffrement
│   └── password_generator.py  # Générateur de mots de passe
├── gui/
│   ├── main_window.py         # Fenêtre principale
│   ├── dialogs/               # Dialogues de l'application
│   └── widgets/               # Widgets personnalisés
├── utils/
│   ├── geometry.py           # Utilitaires pour la géométrie
│   ├── clipboard.py          # Gestionnaire du presse-papiers
│   └── validators.py         # Fonctions de validation
├── assets/
│   └── images/               # Images et icônes
└── data/
    └── database/             # Fichiers de base de données
```

## 🎮 Utilisation

### Démarrage de l'application

```bash
python main.py
```

### Première utilisation

1. Au premier démarrage, définissez un mot de passe maître fort
2. Utilisez ce mot de passe pour protéger l'accès à vos données

### Fonctionnalités principales

#### Ajout d'un compte

- Cliquez sur "Add Account"
- Remplissez les champs : Site Web, Nom d'utilisateur, Mot de passe
- Utilisez le générateur pour créer un mot de passe sécurisé
- Cliquez sur "Save Account"

#### Modification d'un compte

- Sélectionnez un compte dans le tableau
- Cliquez sur "Edit Account"
- Modifiez les informations souhaitées
- Sauvegardez les modifications

#### Suppression d'un compte

- Sélectionnez un compte dans le tableau
- Cliquez sur "Supp Account"
- Confirmez la suppression

#### Visualisation des données

- Clic droit sur un compte dans le tableau
- Sélectionnez "View data"
- Saisissez votre mot de passe maître pour déchiffrer les données

#### Menu contextuel

- **Copy Site** : Copier le nom du site
- **Copy Login** : Copier le nom d'utilisateur
- **Copy Password** : Copier le mot de passe
- **View data** : Voir les données déchiffrées

## 🔒 Sécurité

### Chiffrement

- Utilisation de `Fernet` (cryptographie symétrique AES 128)
- Dérivation de clé avec PBKDF2 et SHA-256
- Salt unique pour chaque dérivation de clé

### Mot de passe maître

- Hachage avec PBKDF2-HMAC-SHA256
- 100 000 itérations pour la résistance aux attaques par force brute
- Salt aléatoire de 16 bytes

### Base de données

- Chiffrement de toutes les données sensibles avant stockage
- Base de données SQLite locale (pas de transmission réseau)

## 🛠️ Architecture technique

### Modèle MVC

- **Model** : `core/database.py`, `core/encryption.py`
- **View** : `gui/` (fenêtres et widgets)
- **Controller** : `gui/main_window.py`

### Patterns utilisés

- **Factory Pattern** : Création des dialogues
- **Observer Pattern** : Callbacks pour les événements
- **Strategy Pattern** : Différentes stratégies de validation

### Bonnes pratiques

- Séparation des responsabilités
- Code modulaire et réutilisable
- Gestion d'erreurs robuste
- Configuration centralisée
- Logging des erreurs

## 🔧 Configuration

La configuration se trouve dans `config/settings.py` :

- **Couleurs** : Personnalisation du thème visuel
- **Dimensions** : Tailles des fenêtres
- **Messages** : Textes d'interface
- **Validation** : Règles de validation
- **Générateur** : Configuration du générateur de mots de passe

## 📝 Développement

### Ajout de nouvelles fonctionnalités

1. **Nouveau dialogue** : Créer dans `gui/dialogs/`
2. **Nouveau widget** : Ajouter dans `gui/widgets/`
3. **Nouvelle fonctionnalité métier** : Développer dans `core/`
4. **Nouveaux utilitaires** : Placer dans `utils/`

### Tests

Pour ajouter des tests :

```bash
mkdir tests
# Ajouter vos fichiers de tests
```

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🐛 Problèmes connus

- Les icônes peuvent ne pas s'afficher si le dossier `assets/images/` n'existe pas
- Compatible Python 3.7+ uniquement
- Interface optimisée pour les résolutions 1920x1080 et plus

## 💡 Améliorations futures

- [ ] Export/Import des données
- [ ] Sauvegarde cloud optionnelle
- [ ] Authentification à deux facteurs
- [ ] Générateur de mots de passe avancé
- [ ] Mode sombre/clair
- [ ] Support multi-langues
- [ ] Détection de fuites de mots de passe
- [ ] Auto-remplissage navigateur

## 👤 Auteur

Votre nom - votre.email@example.com

Projet Link: [https://github.com/votre-username/password-manager](https://github.com/votre-username/password-manager)
