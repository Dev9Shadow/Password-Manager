"""
Widgets personnalisés pour l'interface utilisateur
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Toplevel, Label, Canvas
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel
from config.settings import COLORS, WINDOW_CONFIG,VISUAL_EFFECTS
from utils.geometry import GeometryUtils

class MessageDialog:
    """Dialog personnalisé pour afficher des messages"""
    
    def __init__(self, parent, title: str, message: str, btn1_text: str = "OK", btn2_text: str = None):
        self.result = None
        self._create_dialog(parent, title, message, btn1_text, btn2_text)
    
    def _create_dialog(self, parent, title: str, message: str, btn1_text: str, btn2_text: str):
        """Créer le dialog de message"""
        self.dialog = Toplevel(parent)
        self.dialog.title(title)
        self.dialog.config(bg="white")
        self.dialog.geometry(GeometryUtils.center_on_parent(parent, 400, 150))
        self.dialog.minsize(400, 150)
        self.dialog.maxsize(400, 150)
        self.dialog.grab_set()  # Modal
        
        # Message
        msg_label = Label(
            self.dialog, 
            text=message, 
            font=('yu gothic ui', 13, 'bold'), 
            bg='white'
        )
        msg_label.pack(pady=20)
        
        # Ligne décorative - CORRIGÉ
        line = Canvas(
            self.dialog, 
            bg=COLORS['text_accent'],  # Changé de 'accent' à 'text_accent'
            width=400, 
            height=20, 
            highlightthickness=0
        )
        line.place(x=0, y=135)
        
        # Bouton principal
        btn1 = CTkButton(
            self.dialog,
            text=btn1_text,
            command=self._on_btn1_click,
            width=100,
            text_color='black',
            bg_color="white",
            fg_color=COLORS['text_accent'],  # Changé de 'accent' à 'text_accent'
            font=('yu gothic ui', 12, 'bold'),
            border_width=1,
            border_color='black',
            corner_radius=4
        )
        btn1.place(x=150, y=75)
        
        # Bouton secondaire optionnel
        if btn2_text:
            btn2 = CTkButton(
                self.dialog,
                text=btn2_text,
                command=self._on_btn2_click,
                width=100,
                text_color='black',
                bg_color="white",
                fg_color=COLORS['text_accent'],  # Changé de 'accent' à 'text_accent'
                font=('yu gothic ui', 12, 'bold'),
                border_width=1,
                border_color='black',
                corner_radius=4
            )
            btn2.place(x=150, y=110)
    
    def _on_btn1_click(self):
        """Gestionnaire du premier bouton"""
        self.result = "btn1"
        self.dialog.destroy()
    
    def _on_btn2_click(self):
        """Gestionnaire du second bouton"""
        self.result = "btn2"
        self.dialog.destroy()
    
    def show(self):
        """Afficher le dialog et retourner le résultat"""
        self.dialog.wait_window()
        return self.result

class CustomEntry(tk.Entry):
    """Entry personnalisé avec style cohérent"""
    
    def __init__(self, parent, show_text=False, **kwargs):
        default_config = {
            'relief': tk.FLAT,
            'fg': COLORS['input_text'],
            'bg': COLORS['primary_bg'],
            'highlightthickness': 0,
            'font': ('yu gothic ui', 12, 'bold')
        }
        
        if show_text:
            default_config['show'] = '*'
        
        # Fusionner avec les options personnalisées
        default_config.update(kwargs)
        
        super().__init__(parent, **default_config)

class StyledButton(CTkButton):
    """Bouton avec style par défaut"""
    
    def __init__(self, parent, **kwargs):
        default_config = {
            'text_color': COLORS['text_primary'],
            'fg_color': COLORS['button_primary'],
            'hover_color': COLORS['button_hover'],
            'font': ("Arial", 10, "bold"),
            'corner_radius': 15,
            'border_color': "black",
            'border_width': 1
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)

class ModernCard(CTkFrame):
    """Carte moderne avec effet glassmorphism"""
    
    def __init__(self, parent, width=200, height=100, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            fg_color=COLORS['card_bg'],
            corner_radius=VISUAL_EFFECTS['border_radius'],
            border_width=1,
            border_color=COLORS['input_border'],
            **kwargs
        )

class ModernButton(CTkButton):
    """Bouton moderne avec effets hover"""
    
    def __init__(self, parent, style="primary", **kwargs):
        styles = {
            'primary': {
                'fg_color': [COLORS['button_primary'], COLORS['button_hover']],
                'hover_color': COLORS['button_hover'],
                'border_color': COLORS['accent_glow']
            },
            'secondary': {
                'fg_color': COLORS['button_secondary'],
                'hover_color': COLORS['button_primary'],
                'border_color': COLORS['button_secondary']
            },
            'danger': {
                'fg_color': COLORS['button_danger'],
                'hover_color': '#ff5252',
                'border_color': COLORS['button_danger']
            },
            'success': {
                'fg_color': COLORS['button_success'],
                'hover_color': '#40c057',
                'border_color': COLORS['button_success']
            }
        }
        
        style_config = styles.get(style, styles['primary'])
        
        default_config = {
            'corner_radius': VISUAL_EFFECTS['border_radius'],
            'border_width': 2,
            'font': ('Segoe UI', 12, 'bold'),
            'text_color': COLORS['text_primary'],
            'height': 40,
            **style_config
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)

class ModernEntry(CTkEntry):
    """Entry moderne avec effet glow"""
    
    def __init__(self, parent, **kwargs):
        default_config = {
            'fg_color': COLORS['input_bg'],
            'border_color': COLORS['input_border'],
            'text_color': COLORS['input_text'],
            'placeholder_text_color': COLORS['text_secondary'],
            'corner_radius': 10,
            'border_width': 2,
            'font': ('Segoe UI', 11),
            'height': 35
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)

class GradientFrame(tk.Frame):
    """Frame avec fond dégradé"""
    
    def __init__(self, parent, colors=None, **kwargs):
        self.colors = colors or COLORS['gradient_bg']
        super().__init__(parent, **kwargs)
        self.bind('<Configure>', self._on_configure)
    
    def _on_configure(self, event=None):
        """Créer le dégradé lors du redimensionnement"""
        self.create_gradient()
    
    def create_gradient(self):
        """Créer l'effet de dégradé (simplifié pour tkinter)"""
        self.config(bg=self.colors[0] if isinstance(self.colors, list) else self.colors)

class ModernLabel(CTkLabel):
    """Label moderne avec styles prédéfinis"""
    
    def __init__(self, parent, style="primary", **kwargs):
        styles = {
            'primary': {
                'text_color': COLORS['text_primary'],
                'font': ('Segoe UI', 11)
            },
            'secondary': {
                'text_color': COLORS['text_secondary'],
                'font': ('Segoe UI', 10)
            },
            'title': {
                'text_color': COLORS['text_primary'],
                'font': ('Segoe UI', 16, 'bold')
            },
            'subtitle': {
                'text_color': COLORS['text_accent'],
                'font': ('Segoe UI', 13, 'bold')
            }
        }
        
        style_config = styles.get(style, styles['primary'])
        default_config = {
            'fg_color': 'transparent',
            **style_config
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)


def show_message(parent, title: str, message: str, msg_type: str = "info"):
    """
    Afficher un message avec le style personnalisé
    
    Args:
        parent: Fenêtre parent
        title: Titre du message
        message: Contenu du message
        msg_type: Type de message (info, error, success)
    """
    dialog = MessageDialog(parent, title, message)
    return dialog.show()

def show_error(parent, message: str):
    """Afficher un message d'erreur"""
    return show_message(parent, "Erreur", message, "error")

def show_success(parent, message: str):
    """Afficher un message de succès"""
    return show_message(parent, "Succès", message, "success")

def show_info(parent, message: str):
    """Afficher un message d'information"""
    return show_message(parent, "Information", message, "info")