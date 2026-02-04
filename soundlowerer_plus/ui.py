import os, sys, json
from typing import List, Dict
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QAbstractItemView, QSpinBox, QCheckBox, QSplitter, QListWidget,
    QListWidgetItem, QToolBar, QAction, QStatusBar, QSystemTrayIcon, QMenu,
    QMessageBox, QGroupBox, QSlider, QScrollArea, QFrame, QApplication, QSizePolicy,
    QDialog, QDialogButtonBox, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPainter, QPen


# Traductions
TRANSLATIONS = {
    "fr": {
        "app_title": "SoundLowerer Plus",
        "services": "Services",
        "service": "Service",
        "name": "Nom",
        "target_apps": "Applications Cibles",
        "filter_apps": "Filtrer les applications...",
        "refresh": "Actualiser",
        "invert_whitelist": "Inverser (whitelist)",
        "hotkey": "Raccourci Clavier",
        "record": "Enregistrer...",
        "audio_params": "Paramètres Audio",
        "reduction": "Réduction",
        "mode": "Mode",
        "fade": "Fondu",
        "curve": "Courbe",
        "actions": "Actions",
        "save_changes": "Enregistrer les modifications",
        "new_service": "Nouveau service",
        "test": "Tester",
        "presets": "Presets...",
        "export": "Exporter",
        "import_btn": "Importer",
        "start": "Démarrer",
        "stop": "Arrêter",
        "delete": "Supprimer",
        "duplicate": "Dupliquer",
        "settings": "Paramètres",
        "language": "Langue",
        "theme": "Thème",
        "dark": "Sombre",
        "light": "Clair",
        "cancel": "Annuler",
        "ok": "OK",
        "no_hotkey": "Pas de raccourci",
        "press_keys": "Appuyez...",
        "service_started": "Service '{}' démarré",
        "service_stopped": "Service '{}' arrêté",
        "service_created": "Service '{}' créé",
        "service_modified": "Service '{}' modifié",
        "service_deleted": "Service supprimé",
        "service_duplicated": "Service dupliqué - configurez le raccourci",
        "config_saved": "Configuration sauvegardée",
        "all_stopped": "Tous les services arrêtés",
        "all_started": "Tous les services démarrés",
        "restored": "{} service(s) restauré(s)",
        "preset_applied": "Preset '{}' appliqué - configurez le raccourci",
        "hotkey_recorded": "Raccourci enregistré: {}",
        "hotkey_cancelled": "Enregistrement annulé ou timeout",
        "test_applied": "Test: réduction appliquée - restauration dans 0.8s",
        "confirm_delete": "Supprimer '{}' ?",
        "validation": "Validation",
        "missing_hotkey": "Raccourci manquant.",
        "invalid_hotkey": "Format de raccourci invalide: {}",
        "hotkey_conflict": "Conflit: {} déjà utilisé par '{}'.",
        "export_success": "Service exporté: {}",
        "import_success": "Service '{}' importé",
        "import_error": "Erreur lors de l'import",
        "export_filter": "Service SoundLowerer (*.slp)",
        "import_filter": "Service SoundLowerer (*.slp)",
        # Tooltips
        "tooltip_service_name": "Nom pour identifier ce service dans la liste",
        "tooltip_filter_apps": "Tapez pour filtrer la liste des applications",
        "tooltip_add_app": "Ajouter un programme manuellement",
        "tooltip_add": "Ajouter",
        "tooltip_hotkey": "Raccourci clavier pour activer/désactiver ce service",
        "tooltip_reduction": "Pourcentage de réduction du volume\n75% = le volume passe à 25% de l'original",
        "tooltip_mode": "hold: maintenir la touche appuyée pour réduire\ntoggle: appuyer pour activer/désactiver",
        "tooltip_fade": "Durée de la transition de volume en millisecondes\n0 = changement instantané",
        "tooltip_curve": "linear: transition à vitesse constante\nexpo: transition plus naturelle (rapide au début)",
        "tooltip_invert": "Réduit TOUT sauf les applications sélectionnées",
        # Paramètres supplémentaires
        "close_to_tray": "Réduire dans la barre des tâches",
        "close_to_tray_desc": "Fermer la fenêtre réduit l'app dans la zone de notification",
        "behavior": "Comportement",
        "replay_tutorial": "Revoir le tutoriel",
        "tray_open": "Ouvrir",
        "tray_quit": "Quitter",
        "tray_toggle_all": "Activer/Désactiver tous",
        "minimized_to_tray": "SoundLowerer réduit dans la barre des tâches",
    },
    "en": {
        "app_title": "SoundLowerer Plus",
        "services": "Services",
        "service": "Service",
        "name": "Name",
        "target_apps": "Target Applications",
        "filter_apps": "Filter applications...",
        "refresh": "Refresh",
        "invert_whitelist": "Invert (whitelist)",
        "hotkey": "Keyboard Shortcut",
        "record": "Record...",
        "audio_params": "Audio Settings",
        "reduction": "Reduction",
        "mode": "Mode",
        "fade": "Fade",
        "curve": "Curve",
        "actions": "Actions",
        "save_changes": "Save changes",
        "new_service": "New service",
        "test": "Test",
        "presets": "Presets...",
        "export": "Export",
        "import_btn": "Import",
        "start": "Start",
        "stop": "Stop",
        "delete": "Delete",
        "duplicate": "Duplicate",
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "cancel": "Cancel",
        "ok": "OK",
        "no_hotkey": "No shortcut",
        "press_keys": "Press...",
        "service_started": "Service '{}' started",
        "service_stopped": "Service '{}' stopped",
        "service_created": "Service '{}' created",
        "service_modified": "Service '{}' modified",
        "service_deleted": "Service deleted",
        "service_duplicated": "Service duplicated - configure shortcut",
        "config_saved": "Configuration saved",
        "all_stopped": "All services stopped",
        "all_started": "All services started",
        "restored": "{} service(s) restored",
        "preset_applied": "Preset '{}' applied - configure shortcut",
        "hotkey_recorded": "Shortcut recorded: {}",
        "hotkey_cancelled": "Recording cancelled or timeout",
        "test_applied": "Test: reduction applied - restoring in 0.8s",
        "confirm_delete": "Delete '{}' ?",
        "validation": "Validation",
        "missing_hotkey": "Shortcut missing.",
        "invalid_hotkey": "Invalid shortcut format: {}",
        "hotkey_conflict": "Conflict: {} already used by '{}'.",
        "export_success": "Service exported: {}",
        "import_success": "Service '{}' imported",
        "import_error": "Import error",
        "export_filter": "SoundLowerer Service (*.slp)",
        "import_filter": "SoundLowerer Service (*.slp)",
        # Tooltips
        "tooltip_service_name": "Name to identify this service in the list",
        "tooltip_filter_apps": "Type to filter the application list",
        "tooltip_add_app": "Add a program manually",
        "tooltip_add": "Add",
        "tooltip_hotkey": "Keyboard shortcut to activate/deactivate this service",
        "tooltip_reduction": "Volume reduction percentage\n75% = volume goes to 25% of original",
        "tooltip_mode": "hold: keep the key pressed to reduce\ntoggle: press to activate/deactivate",
        "tooltip_fade": "Volume transition duration in milliseconds\n0 = instant change",
        "tooltip_curve": "linear: constant speed transition\nexpo: more natural transition (fast at start)",
        "tooltip_invert": "Reduce ALL except selected applications",
        # Additional settings
        "close_to_tray": "Minimize to system tray",
        "close_to_tray_desc": "Closing the window minimizes the app to notification area",
        "behavior": "Behavior",
        "replay_tutorial": "Replay tutorial",
        "tray_open": "Open",
        "tray_quit": "Quit",
        "tray_toggle_all": "Toggle all",
        "minimized_to_tray": "SoundLowerer minimized to system tray",
    }
}

# Variables globales
_current_lang = "fr"
_current_theme = "dark"

def tr(key: str) -> str:
    """Retourne la traduction pour la clé donnée"""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["fr"]).get(key, key)

def is_dark_theme() -> bool:
    return _current_theme == "dark"


class TutorialDialog(QDialog):
    """Dialogue du tutoriel"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial" if _current_lang == "en" else "Tutoriel")
        self.setMinimumSize(500, 400)
        self._current_step = 0

        # Contenu du tutoriel
        self._steps = self._get_steps()

        # Style selon le thème
        if is_dark_theme():
            self.setStyleSheet("""
                QDialog { background: #1e1e1e; }
                QLabel { color: #e0e0e0; }
                QLabel#title { font-size: 18px; font-weight: bold; color: #7eb8c9; }
                QLabel#step { font-size: 11px; color: #808080; }
                QLabel#content { font-size: 13px; line-height: 1.5; }
                QPushButton { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 6px; padding: 10px 20px; }
                QPushButton:hover { background: #353535; }
                QPushButton#primary { background: #3d6a7a; color: white; border: none; }
                QPushButton#primary:hover { background: #4a7a8a; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background: #f5f5f5; }
                QLabel { color: #333333; }
                QLabel#title { font-size: 18px; font-weight: bold; color: #2563eb; }
                QLabel#step { font-size: 11px; color: #666666; }
                QLabel#content { font-size: 13px; line-height: 1.5; }
                QPushButton { background: #e8e8e8; color: #333333; border: 1px solid #d0d0d0; border-radius: 6px; padding: 10px 20px; }
                QPushButton:hover { background: #d8d8d8; }
                QPushButton#primary { background: #2563eb; color: white; border: none; }
                QPushButton#primary:hover { background: #1d4ed8; }
            """)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Indicateur d'étape
        self.step_label = QLabel()
        self.step_label.setObjectName("step")
        layout.addWidget(self.step_label)

        # Titre
        self.title_label = QLabel()
        self.title_label.setObjectName("title")
        layout.addWidget(self.title_label)

        # Contenu
        self.content_label = QLabel()
        self.content_label.setObjectName("content")
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.content_label, 1)

        # Boutons
        btn_layout = QHBoxLayout()

        self.prev_btn = QPushButton("← " + ("Previous" if _current_lang == "en" else "Précédent"))
        self.prev_btn.clicked.connect(self._prev_step)
        btn_layout.addWidget(self.prev_btn)

        btn_layout.addStretch()

        self.skip_btn = QPushButton("Skip" if _current_lang == "en" else "Passer")
        self.skip_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.skip_btn)

        self.next_btn = QPushButton(("Next" if _current_lang == "en" else "Suivant") + " →")
        self.next_btn.setObjectName("primary")
        self.next_btn.clicked.connect(self._next_step)
        btn_layout.addWidget(self.next_btn)

        layout.addLayout(btn_layout)

        self._update_display()

    def _get_steps(self):
        if _current_lang == "en":
            return [
                {
                    "title": "Welcome to SoundLowerer Plus!",
                    "content": "This application allows you to automatically lower the volume of certain applications when you press a keyboard shortcut.\n\nPerfect for:\n• Lowering music when someone talks to you\n• Reducing game sounds to hear voice chat\n• Any situation where you need quick volume control"
                },
                {
                    "title": "Step 1: Create a Service",
                    "content": "A 'service' is a volume reduction rule.\n\n1. Give it a name (e.g., 'Lower Spotify')\n\n2. Select the target applications whose volume should be reduced\n\n3. Configure a keyboard shortcut by clicking 'Record...' and pressing your desired key combination"
                },
                {
                    "title": "Step 2: Audio Settings",
                    "content": "• Reduction: How much to lower the volume (75% = volume goes to 25%)\n\n• Mode:\n  - Hold: Keep the key pressed to reduce\n  - Toggle: Press once to reduce, press again to restore\n\n• Fade: Transition duration in milliseconds\n\n• Curve: Linear (constant) or Expo (more natural)"
                },
                {
                    "title": "Step 3: Start the Service",
                    "content": "Once configured:\n\n1. Click 'New service' to add it to the list\n\n2. Double-click on a service or use the ▶ button to start it\n\n3. The indicator turns green when active\n\n4. Use your shortcut to control the volume!\n\nTip: Services are automatically restored when you reopen the app."
                },
                {
                    "title": "You're Ready!",
                    "content": "You now know the basics of SoundLowerer Plus.\n\nOther features:\n• Right-click on a service for more options\n• Export/import your services to share them\n• Access settings via the ⚙ button\n\nEnjoy! 🎵"
                }
            ]
        else:
            return [
                {
                    "title": "Bienvenue dans SoundLowerer Plus !",
                    "content": "Cette application vous permet de baisser automatiquement le volume de certaines applications quand vous appuyez sur un raccourci clavier.\n\nParfait pour :\n• Baisser la musique quand quelqu'un vous parle\n• Réduire les sons d'un jeu pour entendre le chat vocal\n• Toute situation où vous avez besoin d'un contrôle rapide du volume"
                },
                {
                    "title": "Étape 1 : Créer un Service",
                    "content": "Un 'service' est une règle de réduction de volume.\n\n1. Donnez-lui un nom (ex: 'Baisser Spotify')\n\n2. Sélectionnez les applications cibles dont le volume doit être réduit\n\n3. Configurez un raccourci clavier en cliquant sur 'Enregistrer...' et en appuyant sur la combinaison souhaitée"
                },
                {
                    "title": "Étape 2 : Paramètres Audio",
                    "content": "• Réduction : De combien baisser le volume (75% = le volume passe à 25%)\n\n• Mode :\n  - Hold : Maintenir la touche appuyée pour réduire\n  - Toggle : Appuyer une fois pour réduire, encore pour restaurer\n\n• Fondu : Durée de la transition en millisecondes\n\n• Courbe : Linéaire (constante) ou Expo (plus naturelle)"
                },
                {
                    "title": "Étape 3 : Démarrer le Service",
                    "content": "Une fois configuré :\n\n1. Cliquez sur 'Nouveau service' pour l'ajouter à la liste\n\n2. Double-cliquez sur un service ou utilisez le bouton ▶ pour le démarrer\n\n3. L'indicateur devient vert quand il est actif\n\n4. Utilisez votre raccourci pour contrôler le volume !\n\nAstuce : Les services sont automatiquement restaurés quand vous rouvrez l'app."
                },
                {
                    "title": "Vous êtes prêt !",
                    "content": "Vous connaissez maintenant les bases de SoundLowerer Plus.\n\nAutres fonctionnalités :\n• Clic droit sur un service pour plus d'options\n• Exportez/importez vos services pour les partager\n• Accédez aux paramètres via le bouton ⚙\n\nBonne utilisation ! 🎵"
                }
            ]

    def _update_display(self):
        step = self._steps[self._current_step]
        total = len(self._steps)

        self.step_label.setText(f"{'Step' if _current_lang == 'en' else 'Étape'} {self._current_step + 1}/{total}")
        self.title_label.setText(step["title"])
        self.content_label.setText(step["content"])

        self.prev_btn.setEnabled(self._current_step > 0)

        if self._current_step == total - 1:
            self.next_btn.setText("Finish" if _current_lang == "en" else "Terminer")
            self.skip_btn.hide()
        else:
            self.next_btn.setText(("Next" if _current_lang == "en" else "Suivant") + " →")
            self.skip_btn.show()

    def _next_step(self):
        if self._current_step < len(self._steps) - 1:
            self._current_step += 1
            self._update_display()
        else:
            self.accept()

    def _prev_step(self):
        if self._current_step > 0:
            self._current_step -= 1
            self._update_display()


class SettingsDialog(QDialog):
    """Dialogue des paramètres"""
    def __init__(self, current_lang: str, current_theme: str, close_to_tray: bool = True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("settings"))
        self.setMinimumWidth(320)
        self._close_to_tray = close_to_tray

        # Appliquer le style selon le thème
        if is_dark_theme():
            self.setStyleSheet("""
                QDialog { background: #1e1e1e; }
                QLabel { color: #e0e0e0; }
                QGroupBox { font-weight: 600; color: #7eb8c9; border: 1px solid #2d2d2d; border-radius: 8px;
                    margin-top: 12px; padding: 16px 12px 12px 12px; background: #252525; }
                QGroupBox::title { subcontrol-origin: margin; left: 12px; top: 2px; padding: 0 6px; background: #252525; }
                QComboBox { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 6px; padding: 8px; }
                QComboBox::drop-down { border: none; width: 24px; }
                QComboBox::down-arrow { border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #888; }
                QComboBox QAbstractItemView { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; selection-background-color: #3d6a7a; }
                QPushButton { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 6px; padding: 8px 16px; }
                QPushButton:hover { background: #353535; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background: #f5f5f5; }
                QLabel { color: #333333; }
                QGroupBox { font-weight: 600; color: #2563eb; border: 1px solid #d0d0d0; border-radius: 8px;
                    margin-top: 12px; padding: 16px 12px 12px 12px; background: #ffffff; }
                QGroupBox::title { subcontrol-origin: margin; left: 12px; top: 2px; padding: 0 6px; background: #ffffff; }
                QComboBox { background: #ffffff; color: #333333; border: 1px solid #d0d0d0; border-radius: 6px; padding: 8px; }
                QComboBox::drop-down { border: none; width: 24px; }
                QComboBox::down-arrow { border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #666; }
                QComboBox QAbstractItemView { background: #ffffff; color: #333333; border: 1px solid #d0d0d0; selection-background-color: #2563eb; selection-color: white; }
                QPushButton { background: #e8e8e8; color: #333333; border: 1px solid #d0d0d0; border-radius: 6px; padding: 8px 16px; }
                QPushButton:hover { background: #d8d8d8; }
            """)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)

        # Langue
        lang_group = QGroupBox(tr("language"))
        lang_layout = QHBoxLayout(lang_group)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Français", "fr")
        self.lang_combo.addItem("English", "en")
        idx = self.lang_combo.findData(current_lang)
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)
        lang_layout.addWidget(self.lang_combo)
        layout.addWidget(lang_group)

        # Thème
        theme_group = QGroupBox(tr("theme"))
        theme_layout = QHBoxLayout(theme_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("dark"), "dark")
        self.theme_combo.addItem(tr("light"), "light")
        idx = self.theme_combo.findData(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        theme_layout.addWidget(self.theme_combo)
        layout.addWidget(theme_group)

        # Comportement
        behavior_group = QGroupBox(tr("behavior"))
        behavior_layout = QVBoxLayout(behavior_group)
        self.close_to_tray_chk = QCheckBox(tr("close_to_tray"))
        self.close_to_tray_chk.setToolTip(tr("close_to_tray_desc"))
        self.close_to_tray_chk.setChecked(self._close_to_tray)
        behavior_layout.addWidget(self.close_to_tray_chk)
        layout.addWidget(behavior_group)

        # Bouton tutoriel
        tutorial_btn = QPushButton("🎓 " + tr("replay_tutorial"))
        tutorial_btn.clicked.connect(self._show_tutorial)
        layout.addWidget(tutorial_btn)

        layout.addSpacing(8)

        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        ok_btn = QPushButton(tr("ok"))
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)

        self._tutorial_requested = False

    def _show_tutorial(self):
        self._tutorial_requested = True
        self.accept()

    def tutorial_requested(self) -> bool:
        return self._tutorial_requested

    def get_settings(self) -> Dict:
        return {
            "language": self.lang_combo.currentData(),
            "theme": self.theme_combo.currentData(),
            "close_to_tray": self.close_to_tray_chk.isChecked()
        }
from audio_backend import unique_apps
from service import VolumeServiceController
from hotkeys import record_hotkey_once, validate_hotkey
from config import load_config, save_config

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

# Presets d'applications courantes
APP_PRESETS = {
    "Discord": ["discord.exe"],
    "Spotify": ["spotify.exe"],
    "Chrome": ["chrome.exe"],
    "Firefox": ["firefox.exe"],
    "Microsoft Edge": ["msedge.exe"],
    "OBS Studio": ["obs64.exe", "obs32.exe"],
    "Microsoft Teams": ["teams.exe", "ms-teams.exe"],
    "Zoom": ["zoom.exe"],
    "VLC": ["vlc.exe"],
    "Steam": ["steam.exe", "steamwebhelper.exe"],
    "Jeux (tout)": ["game", "unity", "unreal"],
}


class StatusIndicator(QWidget):
    """Petit rond coloré pour indiquer le statut"""
    def __init__(self, active=False, parent=None):
        super().__init__(parent)
        self._active = active
        self.setFixedSize(12, 12)

    def set_active(self, active: bool):
        self._active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self._active:
            painter.setBrush(QColor("#22c55e"))  # Vert
        else:
            if is_dark_theme():
                painter.setBrush(QColor("#525252"))  # Gris foncé
            else:
                painter.setBrush(QColor("#d0d0d0"))  # Gris clair
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 10, 10)


class ServiceItemWidget(QWidget):
    """Widget personnalisé pour afficher un service dans la liste"""
    clicked = pyqtSignal(int)
    doubleClicked = pyqtSignal(int)

    def __init__(self, index: int, name: str, hotkey: str, active: bool = False, parent=None):
        super().__init__(parent)
        self.index = index
        self._selected = False
        self.setMinimumHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        self.setAutoFillBackground(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Indicateur de statut
        self.indicator = StatusIndicator(active)
        layout.addWidget(self.indicator)

        # Infos du service
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        self.name_label = QLabel(name)
        self.hotkey_label = QLabel(hotkey if hotkey else tr("no_hotkey"))

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.hotkey_label)

        layout.addLayout(info_layout, 1)

        self._update_style()

    def set_active(self, active: bool):
        self.indicator.set_active(active)

    def set_selected(self, selected: bool):
        self._selected = selected
        self._update_style()

    def _update_style(self):
        if is_dark_theme():
            if self._selected:
                self.setStyleSheet("ServiceItemWidget { background: #3d6d8f; border-radius: 8px; }")
                self.name_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #ffffff; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #cde4f0; background: transparent;")
            else:
                self.setStyleSheet("ServiceItemWidget { background: #242424; border-radius: 8px; } ServiceItemWidget:hover { background: #2e2e2e; }")
                self.name_label.setStyleSheet("font-weight: 500; font-size: 13px; color: #e0e0e0; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #808080; background: transparent;")
        else:
            if self._selected:
                self.setStyleSheet("ServiceItemWidget { background: #2563eb; border-radius: 8px; }")
                self.name_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #ffffff; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #bfdbfe; background: transparent;")
            else:
                self.setStyleSheet("ServiceItemWidget { background: #ffffff; border-radius: 8px; border: 1px solid #e0e0e0; } ServiceItemWidget:hover { background: #f0f0f0; }")
                self.name_label.setStyleSheet("font-weight: 500; font-size: 13px; color: #333333; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #666666; background: transparent;")

    def update_info(self, name: str, hotkey: str):
        self.name_label.setText(name)
        self.hotkey_label.setText(hotkey if hotkey else tr("no_hotkey"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit(self.index)
        super().mouseDoubleClickEvent(event)


class ServiceListWidget(QWidget):
    """Liste personnalisée de services"""
    selectionChanged = pyqtSignal(int)
    itemDoubleClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: List[ServiceItemWidget] = []
        self._selected_index = -1

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(4)
        self.layout.addStretch()

    def clear(self):
        for item in self._items:
            item.deleteLater()
        self._items.clear()
        self._selected_index = -1
        # Recréer le stretch
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.layout.addStretch()

    def add_item(self, index: int, name: str, hotkey: str, active: bool = False):
        item = ServiceItemWidget(index, name, hotkey, active)
        item.clicked.connect(self._on_item_clicked)
        item.doubleClicked.connect(self._on_item_double_clicked)

        # Insérer avant le stretch
        self.layout.insertWidget(self.layout.count() - 1, item)
        self._items.append(item)

    def _on_item_clicked(self, index: int):
        self.select(index)

    def _on_item_double_clicked(self, index: int):
        self.itemDoubleClicked.emit(index)

    def select(self, index: int):
        # Désélectionner l'ancien
        if 0 <= self._selected_index < len(self._items):
            self._items[self._selected_index].set_selected(False)

        self._selected_index = index

        # Sélectionner le nouveau
        if 0 <= index < len(self._items):
            self._items[index].set_selected(True)

        self.selectionChanged.emit(index)

    def selected_index(self) -> int:
        return self._selected_index

    def update_status(self, index: int, active: bool):
        if 0 <= index < len(self._items):
            self._items[index].set_active(active)

    def update_item(self, index: int, name: str, hotkey: str):
        if 0 <= index < len(self._items):
            self._items[index].update_info(name, hotkey)

    def get_item_at(self, pos) -> int:
        """Retourne l'index de l'item à la position donnée, ou -1"""
        for item in self._items:
            if item.geometry().contains(pos):
                return item.index
        return -1

    def contextMenuEvent(self, event):
        idx = self.get_item_at(event.pos())
        if idx >= 0:
            self.select(idx)
            # Le menu sera géré par le parent
            event.ignore()
        else:
            event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(resource_path("icons"), "tray.svg")))

        self.data = load_config()

        # Charger les paramètres
        global _current_lang
        _current_lang = self.data.get("settings", {}).get("language", "fr")
        self._current_theme = self.data.get("settings", {}).get("theme", "dark")
        self._close_to_tray = self.data.get("settings", {}).get("close_to_tray", True)
        self._force_quit = False  # Pour distinguer fermeture réelle de minimisation

        self.setWindowTitle(tr("app_title"))
        self.resize(900, 650)

        # Charger le thème
        self._apply_theme()
        self.services: List[Dict] = self.data.get("services", [])
        self.controllers: Dict[int, VolumeServiceController] = {}
        self._selected_index = -1  # Index du service sélectionné

        self._build_ui()
        self._load_list()
        self._refresh_apps()
        self._setup_tray()

        # Sauvegarde auto (debounce)
        self._dirty = False
        self.timer = QTimer(self)
        self.timer.setInterval(1500)
        self.timer.timeout.connect(self._autosave)
        self.timer.start()

        # Rafraîchissement périodique de la liste des applis audio
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(5000)
        self.refresh_timer.timeout.connect(self._refresh_apps)
        self.refresh_timer.start()

        # Timer pour rafraîchir les indicateurs de statut
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(500)
        self.status_timer.timeout.connect(self._update_status_indicators)
        self.status_timer.start()

        # Restaurer les services actifs de la session précédente
        self._restore_active_services()

        # Appliquer le thème une seconde fois pour les éléments créés après
        self._apply_theme()

        # Afficher le tutoriel au premier lancement
        if not self.data.get("settings", {}).get("tutorial_shown", False):
            QTimer.singleShot(500, self._show_tutorial_first_time)

    def _apply_theme(self):
        """Applique le thème actuel"""
        global _current_theme
        _current_theme = self._current_theme

        if self._current_theme == "light":
            self._apply_light_theme()
        else:
            try:
                with open(resource_path("style.qss"), "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
            except Exception:
                pass

        # Appliquer les couleurs à la liste des services et aux cibles
        if hasattr(self, 'service_scroll'):
            if self._current_theme == "light":
                self.service_scroll.setStyleSheet("background: #f5f5f5;")
                self.list_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2563eb; padding: 12px; background: #f5f5f5;")
                self.service_list.setStyleSheet("background: #f5f5f5;")
                self.targets_scroll.setStyleSheet("QScrollArea { border: 1px solid #d0d0d0; border-radius: 6px; background: #ffffff; }")
                self.targets_container.setStyleSheet("background: #ffffff;")
            else:
                self.service_scroll.setStyleSheet("background: #1a1a1a;")
                self.list_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #7eb8c9; padding: 12px; background: #1a1a1a;")
                self.service_list.setStyleSheet("background: #1a1a1a;")
                self.targets_scroll.setStyleSheet("QScrollArea { border: 1px solid #2d2d2d; border-radius: 6px; background: #222222; }")
                self.targets_container.setStyleSheet("background: #222222;")

        # Rafraîchir la liste des services pour appliquer les nouveaux styles
        if hasattr(self, 'service_list'):
            self._load_list()
            if self._selected_index >= 0:
                self.service_list.select(self._selected_index)

        # Rafraîchir les checkboxes des applications
        if hasattr(self, 'targets_checkboxes'):
            current = {name: cb.isChecked() for name, cb in self.targets_checkboxes.items()}
            self._rebuild_checkboxes(current)

    def _apply_light_theme(self):
        """Applique le thème clair"""
        self.setStyleSheet("""
            * { font-family: 'Segoe UI', 'Inter', Arial, sans-serif; font-size: 13px; }
            QMainWindow { background: #f5f5f5; }
            QLabel { color: #333333; }
            QGroupBox { font-weight: 600; font-size: 12px; color: #2563eb; border: 1px solid #d0d0d0;
                border-radius: 8px; margin-top: 14px; padding: 16px 12px 12px 12px; background: #ffffff; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; top: 2px; padding: 0 6px; background: #ffffff; }
            QLineEdit, QComboBox, QSpinBox { background-color: #ffffff; color: #333333; border: 1px solid #d0d0d0;
                border-radius: 6px; padding: 8px 10px; }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border-color: #2563eb; }
            QPushButton { background: #e8e8e8; color: #333333; border: 1px solid #d0d0d0; border-radius: 6px; padding: 10px 16px; }
            QPushButton:hover { background: #d8d8d8; }
            QPushButton#primaryBtn { background: #2563eb; color: white; border: none; font-weight: 600; }
            QPushButton#primaryBtn:hover { background: #1d4ed8; }
            QSlider::groove:horizontal { height: 6px; background: #d0d0d0; border-radius: 3px; }
            QSlider::sub-page:horizontal { background: #2563eb; border-radius: 3px; }
            QSlider::handle:horizontal { background: #2563eb; width: 16px; height: 16px; margin: -5px 0; border-radius: 8px; }
            QCheckBox { color: #333333; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #d0d0d0; background: #ffffff; }
            QCheckBox::indicator:checked { background: #2563eb; border-color: #2563eb; }
            QToolBar { background: #ffffff; border: none; border-bottom: 1px solid #e0e0e0; spacing: 4px; padding: 6px; }
            QToolBar QToolButton { background: transparent; border: none; border-radius: 6px; padding: 8px; }
            QToolBar QToolButton:hover { background: #e8e8e8; }
            QStatusBar { background: #ffffff; color: #666666; border-top: 1px solid #e0e0e0; }
            QScrollArea { background: #f5f5f5; border: none; }
            QScrollBar:vertical { background: #f0f0f0; width: 10px; border-radius: 5px; }
            QScrollBar::handle:vertical { background: #c0c0c0; border-radius: 5px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background: #a0a0a0; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
            QMenu { background: #ffffff; color: #333333; border: 1px solid #d0d0d0; border-radius: 6px; padding: 4px; }
            QMenu::item { padding: 8px 24px; border-radius: 4px; }
            QMenu::item:selected { background: #2563eb; color: white; }
            QToolTip { background: #ffffff; color: #333333; border: 1px solid #d0d0d0; border-radius: 4px; padding: 6px 10px; }
            ServiceListWidget { background: #f5f5f5; }
        """)

    # --- Construction UI ---
    def _build_ui(self):
        # Barre d'outils
        tb = QToolBar("Main", self)
        tb.setIconSize(QSize(20, 20))
        self.addToolBar(tb)

        icon = lambda name: QIcon(os.path.join(resource_path("icons"), name))

        start_act = QAction(icon("play.svg"), tr("start"), self)
        stop_act = QAction(icon("pause.svg"), tr("stop"), self)
        del_act = QAction(icon("delete.svg"), tr("delete"), self)

        start_act.setToolTip(tr("start"))
        stop_act.setToolTip(tr("stop"))
        del_act.setToolTip(tr("delete"))

        start_act.triggered.connect(self._start_selected)
        stop_act.triggered.connect(self._stop_selected)
        del_act.triggered.connect(self._delete_selected)

        for a in (start_act, stop_act, del_act):
            tb.addAction(a)

        tb.addSeparator()

        # Import
        import_act = QAction(icon("add.svg"), tr("import_btn"), self)
        import_act.setToolTip(tr("import_btn"))
        import_act.triggered.connect(self._import_service)
        tb.addAction(import_act)

        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tb.addWidget(spacer)

        # Settings
        settings_act = QAction(icon("settings.svg") if os.path.exists(os.path.join(resource_path("icons"), "settings.svg")) else QIcon(), tr("settings"), self)
        settings_act.setToolTip(tr("settings"))
        settings_act.triggered.connect(self._open_settings)
        tb.addAction(settings_act)

        # Splitter central: liste à gauche / formulaire à droite
        central = QSplitter(self)
        self.setCentralWidget(central)

        # === Liste des services ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.list_label = QLabel(tr("services"))
        self.list_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #7eb8c9; padding: 12px;")

        # Scroll area pour la liste
        scroll_list = QScrollArea()
        scroll_list.setWidgetResizable(True)
        scroll_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_list.setFrameShape(QFrame.NoFrame)
        self.service_scroll = scroll_list  # Garder référence pour le thème

        self.service_list = ServiceListWidget()
        self.service_list.selectionChanged.connect(self._on_service_selected)
        self.service_list.itemDoubleClicked.connect(self._toggle_service)
        self.service_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.service_list.customContextMenuRequested.connect(self._show_context_menu)

        scroll_list.setWidget(self.service_list)

        left_layout.addWidget(self.list_label)
        left_layout.addWidget(scroll_list)

        central.addWidget(left_widget)

        # === Panneau de droite avec scroll ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)

        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setSpacing(8)
        rv.setContentsMargins(12, 8, 12, 8)

        # === Groupe: Service ===
        grp_service = QGroupBox(tr("service"))
        grp_service_layout = QVBoxLayout(grp_service)
        grp_service_layout.setSpacing(8)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom du service..." if _current_lang == "fr" else "Service name...")
        self.name_edit.setToolTip(tr("tooltip_service_name"))

        lbl_name = QLabel(tr("name"))
        grp_service_layout.addWidget(lbl_name)
        grp_service_layout.addWidget(self.name_edit)

        rv.addWidget(grp_service)

        # === Groupe: Applications Cibles ===
        grp_targets = QGroupBox(tr("target_apps"))
        grp_targets_layout = QVBoxLayout(grp_targets)
        grp_targets_layout.setSpacing(8)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(tr("filter_apps"))
        self.filter_edit.setToolTip(tr("tooltip_filter_apps"))
        self.filter_edit.textChanged.connect(self._filter_apps)

        # Scroll area pour les checkboxes
        targets_scroll = QScrollArea()
        targets_scroll.setWidgetResizable(True)
        targets_scroll.setMinimumHeight(100)
        targets_scroll.setMaximumHeight(150)
        targets_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.targets_scroll = targets_scroll  # Garder référence pour le thème

        self.targets_container = QWidget()
        self.targets_layout = QVBoxLayout(self.targets_container)
        self.targets_layout.setContentsMargins(8, 8, 8, 8)
        self.targets_layout.setSpacing(4)
        self.targets_layout.addStretch()

        targets_scroll.setWidget(self.targets_container)
        self.targets_checkboxes: Dict[str, QCheckBox] = {}

        # Ajout manuel d'application
        add_app_row = QHBoxLayout()
        self.add_app_edit = QLineEdit()
        self.add_app_edit.setPlaceholderText("spotify.exe")
        self.add_app_edit.setToolTip(tr("tooltip_add_app"))
        self.add_app_edit.returnPressed.connect(self._add_manual_app)

        self.add_app_btn = QPushButton("+")
        self.add_app_btn.setFixedWidth(36)
        self.add_app_btn.setToolTip(tr("tooltip_add"))
        self.add_app_btn.clicked.connect(self._add_manual_app)

        add_app_row.addWidget(self.add_app_edit, 1)
        add_app_row.addWidget(self.add_app_btn)

        targets_btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton(tr("refresh"))
        self.refresh_btn.setToolTip(tr("refresh"))
        self.refresh_btn.clicked.connect(self._refresh_apps)

        self.all_except_chk = QCheckBox(tr("invert_whitelist"))
        self.all_except_chk.setToolTip(tr("tooltip_invert"))

        targets_btn_row.addWidget(self.refresh_btn)
        targets_btn_row.addWidget(self.all_except_chk)
        targets_btn_row.addStretch()

        grp_targets_layout.addWidget(self.filter_edit)
        grp_targets_layout.addWidget(targets_scroll)
        grp_targets_layout.addLayout(add_app_row)
        grp_targets_layout.addLayout(targets_btn_row)

        rv.addWidget(grp_targets)

        # === Groupe: Raccourci ===
        grp_hotkey = QGroupBox(tr("hotkey"))
        grp_hotkey_layout = QVBoxLayout(grp_hotkey)
        grp_hotkey_layout.setSpacing(8)

        hotkey_row = QHBoxLayout()
        self.hk_edit = QLineEdit()
        self.hk_edit.setPlaceholderText("ctrl+shift+m")
        self.hk_edit.setToolTip(tr("tooltip_hotkey"))

        self.hk_btn = QPushButton(tr("record"))
        self.hk_btn.setToolTip(tr("record"))
        self.hk_btn.clicked.connect(self._record_hotkey)

        hotkey_row.addWidget(self.hk_edit, 1)
        hotkey_row.addWidget(self.hk_btn)

        grp_hotkey_layout.addLayout(hotkey_row)

        rv.addWidget(grp_hotkey)

        # === Groupe: Paramètres Audio ===
        grp_audio = QGroupBox(tr("audio_params"))
        grp_audio_layout = QVBoxLayout(grp_audio)
        grp_audio_layout.setSpacing(12)

        # Slider de réduction
        reduction_row = QHBoxLayout()
        lbl_reduct = QLabel(tr("reduction"))
        self.reduct_slider = QSlider(Qt.Horizontal)
        self.reduct_slider.setRange(0, 100)
        self.reduct_slider.setValue(75)
        self.reduct_slider.setToolTip(tr("tooltip_reduction"))
        self.reduct_label = QLabel("75%")
        self.reduct_label.setMinimumWidth(40)
        self.reduct_slider.valueChanged.connect(lambda v: self.reduct_label.setText(f"{v}%"))

        reduction_row.addWidget(lbl_reduct)
        reduction_row.addWidget(self.reduct_slider, 1)
        reduction_row.addWidget(self.reduct_label)

        grp_audio_layout.addLayout(reduction_row)

        # Mode
        mode_row = QHBoxLayout()
        lbl_mode = QLabel(tr("mode"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["hold", "toggle"])
        self.mode_combo.setToolTip(tr("tooltip_mode"))
        mode_row.addWidget(lbl_mode)
        mode_row.addWidget(self.mode_combo, 1)

        grp_audio_layout.addLayout(mode_row)

        # Fondu et courbe
        fade_row = QHBoxLayout()
        lbl_fade = QLabel(tr("fade"))
        self.fade_spin = QSpinBox()
        self.fade_spin.setRange(0, 5000)
        self.fade_spin.setValue(300)
        self.fade_spin.setSuffix(" ms")
        self.fade_spin.setToolTip(tr("tooltip_fade"))

        lbl_curve = QLabel(tr("curve"))
        self.curve_combo = QComboBox()
        self.curve_combo.addItems(["linear", "expo"])
        self.curve_combo.setToolTip(tr("tooltip_curve"))

        fade_row.addWidget(lbl_fade)
        fade_row.addWidget(self.fade_spin)
        fade_row.addSpacing(16)
        fade_row.addWidget(lbl_curve)
        fade_row.addWidget(self.curve_combo)
        fade_row.addStretch()

        grp_audio_layout.addLayout(fade_row)

        rv.addWidget(grp_audio)

        # === Groupe: Actions ===
        grp_actions = QGroupBox(tr("actions"))
        grp_actions_layout = QVBoxLayout(grp_actions)
        grp_actions_layout.setSpacing(8)

        # Boutons principaux
        btn_row1 = QHBoxLayout()

        self.save_btn = QPushButton(tr("save_changes"))
        self.save_btn.setObjectName("primaryBtn")
        self.save_btn.setToolTip(tr("save_changes"))
        self.save_btn.clicked.connect(self._save_selected)
        self.save_btn.setEnabled(False)

        btn_row1.addWidget(self.save_btn)

        # Boutons secondaires
        btn_row2 = QHBoxLayout()

        self.add_btn = QPushButton(tr("new_service"))
        self.add_btn.setToolTip(tr("new_service"))
        self.add_btn.clicked.connect(self._add_new)

        self.test_btn = QPushButton(tr("test"))
        self.test_btn.setToolTip(tr("test"))
        self.test_btn.clicked.connect(self._test_current)

        self.preset_btn = QPushButton(tr("presets"))
        self.preset_btn.setToolTip(tr("presets"))
        self.preset_btn.clicked.connect(self._show_presets_menu)

        self.export_btn = QPushButton(tr("export"))
        self.export_btn.setToolTip(tr("export"))
        self.export_btn.clicked.connect(self._export_selected)
        self.export_btn.setEnabled(False)

        btn_row2.addWidget(self.add_btn)
        btn_row2.addWidget(self.test_btn)
        btn_row2.addWidget(self.preset_btn)
        btn_row2.addWidget(self.export_btn)

        grp_actions_layout.addLayout(btn_row1)
        grp_actions_layout.addLayout(btn_row2)

        rv.addWidget(grp_actions)

        rv.addStretch(1)

        scroll.setWidget(right)
        central.addWidget(scroll)
        central.setSizes([280, 500])

        # Barre de statut
        self.setStatusBar(QStatusBar())

    # --- Liste des services ---
    def _load_list(self):
        self.service_list.clear()
        for idx, svc in enumerate(self.services):
            self._add_list_item(svc, idx)

    def _add_list_item(self, svc: Dict, idx: int):
        is_active = idx in self.controllers
        name = svc.get("name", "Service sans nom")
        hotkey = svc.get("hotkey", "")
        self.service_list.add_item(idx, name, hotkey, is_active)

    def _update_status_indicators(self):
        for idx in range(len(self.services)):
            is_active = idx in self.controllers
            self.service_list.update_status(idx, is_active)

    def _on_service_selected(self, idx: int):
        if idx < 0 or idx >= len(self.services):
            self._selected_index = -1
            self.save_btn.setEnabled(False)
            self.export_btn.setEnabled(False)
            return

        self._selected_index = idx
        self.save_btn.setEnabled(True)
        self.export_btn.setEnabled(True)

        # Charger les données dans le formulaire
        svc = self.services[idx]
        self.name_edit.setText(svc.get("name", ""))
        self.hk_edit.setText(svc.get("hotkey", ""))
        self.reduct_slider.setValue(int(svc.get("reduction", 75)))
        self.mode_combo.setCurrentText(svc.get("mode", "hold"))
        self.fade_spin.setValue(int(svc.get("fade_ms", 300)))
        self.curve_combo.setCurrentText(svc.get("curve", "linear"))
        self.all_except_chk.setChecked(bool(svc.get("all_except", False)))

        # Ajouter les cibles aux apps manuelles si elles n'existent pas
        targets = set(svc.get("targets", []))
        if not hasattr(self, '_manual_apps'):
            self._manual_apps = set()
        for target in targets:
            if target not in self.targets_checkboxes:
                self._manual_apps.add(target)

        # Reconstruire si nécessaire pour afficher les nouvelles apps
        if any(t not in self.targets_checkboxes for t in targets):
            current = {name: cb.isChecked() for name, cb in self.targets_checkboxes.items()}
            for t in targets:
                current[t] = True
            self._rebuild_checkboxes(current)
        else:
            # Cocher les cibles
            for name, cb in self.targets_checkboxes.items():
                cb.setChecked(name in targets)

    def _toggle_service(self, idx: int):
        """Double-clic pour démarrer/arrêter"""
        if idx in self.controllers:
            self._stop_at_index(idx)
        else:
            self._start_at_index(idx)

    # --- Menu contextuel ---
    def _show_context_menu(self, pos):
        idx = self.service_list.get_item_at(pos)
        if idx < 0:
            return

        self.service_list.select(idx)
        menu = QMenu(self)

        if idx in self.controllers:
            stop_action = menu.addAction("Arrêter")
            stop_action.triggered.connect(lambda: self._stop_at_index(idx))
        else:
            start_action = menu.addAction("Démarrer")
            start_action.triggered.connect(lambda: self._start_at_index(idx))

        menu.addSeparator()

        dup_action = menu.addAction("Dupliquer")
        dup_action.triggered.connect(lambda: self._duplicate_at_index(idx))

        del_action = menu.addAction("Supprimer")
        del_action.triggered.connect(lambda: self._delete_at_index(idx))

        menu.exec_(self.service_list.mapToGlobal(pos))

    # --- Tray ---
    def _setup_tray(self):
        self.tray = QSystemTrayIcon(QIcon(os.path.join(resource_path("icons"), "tray.svg")), self)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray_menu = QMenu()
        self.toggle_all_act = self.tray_menu.addAction(tr("tray_toggle_all"))
        self.toggle_all_act.triggered.connect(self._toggle_all)
        self.tray_menu.addSeparator()
        self.open_act = self.tray_menu.addAction(tr("tray_open"))
        self.open_act.triggered.connect(self._show_from_tray)
        self.quit_act = self.tray_menu.addAction(tr("tray_quit"))
        self.quit_act.triggered.connect(self._quit_app)
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

    def _on_tray_activated(self, reason):
        """Double-clic sur l'icône du tray pour ouvrir la fenêtre"""
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_from_tray()

    def _show_from_tray(self):
        """Restaure la fenêtre depuis le tray"""
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _quit_app(self):
        """Quitte réellement l'application"""
        self._force_quit = True
        self.close()

    def _toggle_all(self):
        running = any(c.is_active() for c in self.controllers.values()) if self.controllers else False
        if running:
            for idx, c in list(self.controllers.items()):
                c.stop()
                del self.controllers[idx]
            self.statusBar().showMessage(tr("all_stopped"), 3000)
        else:
            for idx in range(len(self.services)):
                self._start_at_index(idx)
            self.statusBar().showMessage(tr("all_started"), 3000)

    # --- Persistance ---
    def _autosave(self):
        if self._dirty:
            self._dirty = False
            self.data["services"] = self.services
            save_config(self.data)
            self.statusBar().showMessage(tr("config_saved"), 3000)

    # --- Données audio ---
    def _add_manual_app(self):
        """Ajoute manuellement une application à la liste"""
        app_name = self.add_app_edit.text().strip()
        if not app_name:
            return

        # Ajouter à la liste des apps manuelles
        if not hasattr(self, '_manual_apps'):
            self._manual_apps = set()
        self._manual_apps.add(app_name)

        # Sauvegarder les sélections actuelles
        current = {name: cb.isChecked() for name, cb in self.targets_checkboxes.items()}
        current[app_name] = True  # Cocher la nouvelle app

        # Reconstruire les checkboxes
        self._rebuild_checkboxes(current)

        # Vider le champ
        self.add_app_edit.clear()

        self.statusBar().showMessage(
            f"'{app_name}' added" if _current_lang == "en" else f"'{app_name}' ajouté",
            3000
        )

    def _refresh_apps(self):
        # Sauvegarder les sélections actuelles
        current = {name: cb.isChecked() for name, cb in self.targets_checkboxes.items()}
        self._all_apps = unique_apps()
        self._rebuild_checkboxes(current)

    def _filter_apps(self, text: str):
        # Sauvegarder les sélections actuelles
        current = {name: cb.isChecked() for name, cb in self.targets_checkboxes.items()}
        self._rebuild_checkboxes(current)

    def _rebuild_checkboxes(self, current_selections: Dict[str, bool] = None):
        if current_selections is None:
            current_selections = {}

        # Supprimer les anciennes checkboxes
        for cb in self.targets_checkboxes.values():
            cb.deleteLater()
        self.targets_checkboxes.clear()

        # Supprimer le stretch
        while self.targets_layout.count():
            item = self.targets_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        filter_text = self.filter_edit.text().lower()
        apps = list(getattr(self, '_all_apps', []) or unique_apps())

        # Ajouter les apps manuelles
        manual_apps = getattr(self, '_manual_apps', set())
        for app in manual_apps:
            if app not in apps:
                apps.append(app)

        # Ajouter aussi les apps des sélections actuelles (pour garder les apps importées)
        for app in current_selections.keys():
            if app not in apps:
                apps.append(app)

        for name in apps:
            if filter_text and filter_text not in name.lower():
                continue
            cb = QCheckBox(name)
            if is_dark_theme():
                cb.setStyleSheet("QCheckBox { color: #c0c0c0; padding: 4px; background: transparent; }")
            else:
                cb.setStyleSheet("QCheckBox { color: #333333; padding: 4px; background: transparent; }")
            if name in current_selections and current_selections[name]:
                cb.setChecked(True)
            self.targets_layout.addWidget(cb)
            self.targets_checkboxes[name] = cb

        self.targets_layout.addStretch()

    # --- Formulaire ---
    def _form_to_service(self) -> Dict:
        targets = [name for name, cb in self.targets_checkboxes.items() if cb.isChecked()]
        return {
            "name": self.name_edit.text() or (targets[0] if targets else "Service"),
            "targets": targets,
            "hotkey": self.hk_edit.text().strip(),
            "reduction": int(self.reduct_slider.value()),
            "mode": self.mode_combo.currentText(),
            "fade_ms": int(self.fade_spin.value()),
            "curve": self.curve_combo.currentText(),
            "all_except": self.all_except_chk.isChecked()
        }

    def _validate(self, svc: Dict, exclude_idx: int = -1) -> str:
        if not svc["hotkey"]:
            return tr("missing_hotkey")
        if not validate_hotkey(svc["hotkey"]):
            return tr("invalid_hotkey").format(svc['hotkey'])
        # Note: On autorise plusieurs services avec le même raccourci
        return ""

    def _record_hotkey(self):
        original_text = self.hk_btn.text()
        self.hk_btn.setText(tr("press_keys"))
        self.hk_btn.setObjectName("recordingBtn")
        self.hk_btn.setStyle(self.hk_btn.style())
        self.hk_btn.setEnabled(False)
        self.hk_edit.setEnabled(False)

        QApplication.processEvents()

        hk = record_hotkey_once()

        self.hk_btn.setText(original_text)
        self.hk_btn.setObjectName("")
        self.hk_btn.setStyle(self.hk_btn.style())
        self.hk_btn.setEnabled(True)
        self.hk_edit.setEnabled(True)

        if hk:
            self.hk_edit.setText(hk)
            self.statusBar().showMessage(tr("hotkey_recorded").format(hk), 3000)
        else:
            self.statusBar().showMessage(tr("hotkey_cancelled"), 3000)

    def _show_presets_menu(self):
        menu = QMenu(self)
        for name, targets in APP_PRESETS.items():
            action = menu.addAction(name)
            action.setData({"name": name, "targets": targets})
        action = menu.exec_(self.preset_btn.mapToGlobal(self.preset_btn.rect().bottomLeft()))
        if action:
            data = action.data()
            self._apply_preset(data["name"], data["targets"])

    def _apply_preset(self, preset_name: str, targets: List[str]):
        self.name_edit.setText(preset_name)
        for app_name, cb in self.targets_checkboxes.items():
            matched = any(t.lower() in app_name.lower() or app_name.lower() in t.lower() for t in targets)
            cb.setChecked(matched)
        self.statusBar().showMessage(tr("preset_applied").format(preset_name), 3000)

    # --- Actions ---
    def _save_selected(self):
        """Sauvegarde les modifications du service sélectionné"""
        if self._selected_index < 0:
            return

        svc = self._form_to_service()
        msg = self._validate(svc, exclude_idx=self._selected_index)
        if msg:
            QMessageBox.warning(self, tr("validation"), msg)
            return

        # Si le service était actif, l'arrêter d'abord
        was_active = self._selected_index in self.controllers
        if was_active:
            self.controllers[self._selected_index].stop()
            del self.controllers[self._selected_index]

        # Mettre à jour les données
        self.services[self._selected_index] = svc
        self._dirty = True

        # Mettre à jour l'affichage dans la liste
        self.service_list.update_item(self._selected_index, svc['name'], svc['hotkey'])

        # Redémarrer si était actif
        if was_active:
            self._start_at_index(self._selected_index)

        self.statusBar().showMessage(tr("service_modified").format(svc['name']), 3000)

    def _add_new(self):
        """Crée un nouveau service"""
        svc = self._form_to_service()
        msg = self._validate(svc)
        if msg:
            QMessageBox.warning(self, tr("validation"), msg)
            return

        self.services.append(svc)
        idx = len(self.services) - 1
        self._add_list_item(svc, idx)
        self._dirty = True

        # Sélectionner le nouveau service
        self.service_list.select(idx)

        self.statusBar().showMessage(tr("service_created").format(svc['name']), 3000)

    def _delete_selected(self):
        if self._selected_index < 0:
            return
        self._delete_at_index(self._selected_index)

    def _delete_at_index(self, idx: int):
        if idx < 0 or idx >= len(self.services):
            return

        svc = self.services[idx]
        reply = QMessageBox.question(self, tr("delete"),
                                     tr("confirm_delete").format(svc.get('name', 'service')),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # Arrêter si actif
        if idx in self.controllers:
            self.controllers[idx].stop()
            del self.controllers[idx]

        # Supprimer
        self.services.pop(idx)
        self._dirty = True

        # Reconstruire les controllers avec les nouveaux index
        new_controllers = {}
        for old_idx, ctrl in self.controllers.items():
            if old_idx > idx:
                new_controllers[old_idx - 1] = ctrl
            else:
                new_controllers[old_idx] = ctrl
        self.controllers = new_controllers

        # Recharger la liste
        self._selected_index = -1
        self.save_btn.setEnabled(False)
        self._load_list()

        self.statusBar().showMessage(tr("service_deleted"), 3000)

    def _duplicate_at_index(self, idx: int):
        svc = dict(self.services[idx])
        svc["name"] = svc.get("name", "") + " (copie)"
        svc["hotkey"] = ""  # Vider le raccourci pour éviter les conflits

        self.services.append(svc)
        new_idx = len(self.services) - 1
        self._add_list_item(svc, new_idx)
        self._dirty = True

        self.service_list.select(new_idx)
        self.statusBar().showMessage(tr("service_duplicated"), 3000)

    def _start_selected(self):
        if self._selected_index < 0:
            return
        self._start_at_index(self._selected_index)

    def _start_at_index(self, idx: int):
        if idx in self.controllers:
            return
        if idx >= len(self.services):
            return

        s = self.services[idx]
        ctrl = VolumeServiceController(
            name=s.get("name", ""),
            targets=s.get("targets", []),
            hotkey=s.get("hotkey", ""),
            reduction_pct=int(s.get("reduction", 75)),
            mode=s.get("mode", "hold"),
            fade_ms=int(s.get("fade_ms", 300)),
            curve=s.get("curve", "linear"),
            all_except=bool(s.get("all_except", False))
        )
        self.controllers[idx] = ctrl
        ctrl.start()
        self.statusBar().showMessage(tr("service_started").format(s.get('name', '')), 3000)

    def _stop_selected(self):
        if self._selected_index < 0:
            return
        self._stop_at_index(self._selected_index)

    def _stop_at_index(self, idx: int):
        if idx not in self.controllers:
            return
        self.controllers[idx].stop()
        del self.controllers[idx]
        self.statusBar().showMessage(tr("service_stopped").format(self.services[idx].get('name', '')), 3000)

    def _test_current(self):
        svc = self._form_to_service()
        msg = self._validate(svc, exclude_idx=self._selected_index)
        if msg:
            QMessageBox.warning(self, tr("validation"), msg)
            return

        c = VolumeServiceController(
            name=svc["name"], targets=svc["targets"], hotkey=svc["hotkey"],
            reduction_pct=svc["reduction"], mode=svc["mode"],
            fade_ms=svc["fade_ms"], curve=svc["curve"], all_except=svc["all_except"]
        )
        c._apply_reduction()
        self.statusBar().showMessage(tr("test_applied"), 3000)
        from threading import Timer
        Timer(0.8, c._restore).start()

    def closeEvent(self, e):
        # Si close_to_tray est activé et qu'on ne force pas la fermeture
        if self._close_to_tray and not self._force_quit:
            e.ignore()
            self.hide()
            self.tray.showMessage(
                tr("app_title"),
                tr("minimized_to_tray"),
                QSystemTrayIcon.Information,
                2000
            )
            return

        # Fermeture réelle
        self.data["settings"]["active_services"] = list(self.controllers.keys())
        self._dirty = True
        self._autosave()
        for idx, ctrl in list(self.controllers.items()):
            ctrl.stop()
        self.tray.hide()
        e.accept()

    def _restore_active_services(self):
        if not self.data.get("settings", {}).get("resume_on_start", True):
            return
        active = self.data.get("settings", {}).get("active_services", [])
        for idx in active:
            if idx < len(self.services):
                self._start_at_index(idx)
        if active:
            self.statusBar().showMessage(tr("restored").format(len(active)), 3000)

    # --- Import/Export ---
    def _export_selected(self):
        """Exporte le service sélectionné dans un fichier"""
        if self._selected_index < 0:
            return

        svc = self.services[self._selected_index]
        default_name = f"{svc.get('name', 'service')}.slp"

        path, _ = QFileDialog.getSaveFileName(
            self, tr("export"), default_name, tr("export_filter")
        )
        if not path:
            return

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(svc, f, indent=2, ensure_ascii=False)
            self.statusBar().showMessage(tr("export_success").format(os.path.basename(path)), 3000)
        except Exception as e:
            QMessageBox.warning(self, tr("export"), str(e))

    def _import_service(self):
        """Importe un service depuis un fichier"""
        path, _ = QFileDialog.getOpenFileName(
            self, tr("import_btn"), "", tr("import_filter")
        )
        if not path:
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                svc = json.load(f)

            # Vérifier que c'est un service valide
            if not isinstance(svc, dict) or "hotkey" not in svc:
                raise ValueError("Invalid service file")

            # Éviter les conflits de hotkey
            existing_hotkeys = {s.get("hotkey") for s in self.services}
            if svc.get("hotkey") in existing_hotkeys:
                svc["hotkey"] = ""  # Vider pour éviter conflit

            self.services.append(svc)
            idx = len(self.services) - 1
            self._add_list_item(svc, idx)
            self._dirty = True

            self.service_list.select(idx)
            self.statusBar().showMessage(tr("import_success").format(svc.get("name", "Service")), 3000)

        except Exception as e:
            QMessageBox.warning(self, tr("import_btn"), tr("import_error") + f"\n{e}")

    # --- Paramètres ---
    def _open_settings(self):
        """Ouvre le dialogue des paramètres"""
        global _current_lang

        dialog = SettingsDialog(
            current_lang=_current_lang,
            current_theme=self._current_theme,
            close_to_tray=self._close_to_tray,
            parent=self
        )

        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()
            need_refresh = False

            # Appliquer la langue
            if settings["language"] != _current_lang:
                _current_lang = settings["language"]
                self.data.setdefault("settings", {})["language"] = _current_lang
                self._dirty = True
                need_refresh = True

            # Appliquer le thème
            if settings["theme"] != self._current_theme:
                self._current_theme = settings["theme"]
                self.data.setdefault("settings", {})["theme"] = self._current_theme
                self._apply_theme()
                self._dirty = True

            # Appliquer close_to_tray
            if settings["close_to_tray"] != self._close_to_tray:
                self._close_to_tray = settings["close_to_tray"]
                self.data.setdefault("settings", {})["close_to_tray"] = self._close_to_tray
                self._dirty = True

            # Rafraîchir l'UI si la langue a changé
            if need_refresh:
                self._refresh_ui_language()

            # Forcer la sauvegarde
            self._autosave()

            # Afficher le tutoriel si demandé
            if dialog.tutorial_requested():
                self._show_tutorial()

    def _show_tutorial(self):
        """Affiche le tutoriel"""
        dialog = TutorialDialog(self)
        dialog.exec_()

    def _show_tutorial_first_time(self):
        """Affiche le tutoriel au premier lancement et enregistre qu'il a été vu"""
        self._show_tutorial()
        self.data.setdefault("settings", {})["tutorial_shown"] = True
        self._dirty = True
        self._autosave()

    def _refresh_ui_language(self):
        """Rafraîchit tous les textes de l'UI avec la nouvelle langue"""
        # Titre de la fenêtre
        self.setWindowTitle(tr("app_title"))

        # Toolbar - recréer les actions avec les nouveaux textes
        toolbar = self.findChild(QToolBar)
        if toolbar:
            actions = toolbar.actions()
            for action in actions:
                if action.iconText() or action.text():
                    # Mapper les anciennes clés aux nouvelles traductions
                    text = action.text().lower()
                    if "start" in text or "démarrer" in text:
                        action.setText(tr("start"))
                        action.setToolTip(tr("start"))
                    elif "stop" in text or "arrêter" in text:
                        action.setText(tr("stop"))
                        action.setToolTip(tr("stop"))
                    elif "delet" in text or "supprimer" in text:
                        action.setText(tr("delete"))
                        action.setToolTip(tr("delete"))
                    elif "import" in text:
                        action.setText(tr("import_btn"))
                        action.setToolTip(tr("import_btn"))
                    elif "setting" in text or "paramètre" in text:
                        action.setText(tr("settings"))
                        action.setToolTip(tr("settings"))

        # Groupes
        for group in self.findChildren(QGroupBox):
            title = group.title().lower()
            if "service" in title:
                group.setTitle(tr("service"))
            elif "target" in title or "cible" in title or "application" in title:
                group.setTitle(tr("target_apps"))
            elif "hotkey" in title or "raccourci" in title or "keyboard" in title:
                group.setTitle(tr("hotkey"))
            elif "audio" in title or "paramètre" in title:
                group.setTitle(tr("audio_params"))
            elif "action" in title:
                group.setTitle(tr("actions"))

        # Boutons
        self.save_btn.setText(tr("save_changes"))
        self.save_btn.setToolTip(tr("save_changes"))
        self.add_btn.setText(tr("new_service"))
        self.add_btn.setToolTip(tr("new_service"))
        self.test_btn.setText(tr("test"))
        self.test_btn.setToolTip(tr("test"))
        self.preset_btn.setText(tr("presets"))
        self.preset_btn.setToolTip(tr("presets"))
        self.export_btn.setText(tr("export"))
        self.export_btn.setToolTip(tr("export"))
        self.refresh_btn.setText(tr("refresh"))
        self.refresh_btn.setToolTip(tr("refresh"))
        self.hk_btn.setText(tr("record"))
        self.hk_btn.setToolTip(tr("record"))

        # Checkbox
        self.all_except_chk.setText(tr("invert_whitelist"))
        self.all_except_chk.setToolTip(tr("invert_whitelist"))

        # Placeholders
        self.filter_edit.setPlaceholderText(tr("filter_apps"))
        self.add_app_edit.setPlaceholderText("spotify.exe")

        # Tooltips
        self.name_edit.setToolTip(tr("tooltip_service_name"))
        self.filter_edit.setToolTip(tr("tooltip_filter_apps"))
        self.add_app_edit.setToolTip(tr("tooltip_add_app"))
        self.add_app_btn.setToolTip(tr("tooltip_add"))
        self.hk_edit.setToolTip(tr("tooltip_hotkey"))
        self.reduct_slider.setToolTip(tr("tooltip_reduction"))
        self.mode_combo.setToolTip(tr("tooltip_mode"))
        self.fade_spin.setToolTip(tr("tooltip_fade"))
        self.curve_combo.setToolTip(tr("tooltip_curve"))
        self.all_except_chk.setToolTip(tr("tooltip_invert"))

        # Menu du tray
        if hasattr(self, 'tray_menu'):
            self.toggle_all_act.setText(tr("tray_toggle_all"))
            self.open_act.setText(tr("tray_open"))
            self.quit_act.setText(tr("tray_quit"))

        # Rafraîchir la liste des services pour mettre à jour "Pas de raccourci"
        self._load_list()
        if self._selected_index >= 0:
            self.service_list.select(self._selected_index)
