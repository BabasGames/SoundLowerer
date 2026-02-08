import os, sys, json
from typing import List, Dict
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QAbstractItemView, QSpinBox, QCheckBox, QSplitter, QListWidget,
    QListWidgetItem, QToolBar, QAction, QStatusBar, QSystemTrayIcon, QMenu,
    QMessageBox, QGroupBox, QSlider, QScrollArea, QFrame, QApplication, QSizePolicy,
    QDialog, QDialogButtonBox, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPainter, QPen, QKeySequence, QRadialGradient
from PyQt5.QtWidgets import QShortcut


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
        "duplicate_name": "Un service nommé '{}' existe déjà.",
        "schedule_invalid_time": "L'heure de fin doit être après l'heure de début.",
        "tray_stop_all": "Tout arrêter",
        "stop_all_done": "{} service(s) arrêté(s)",
        "reset_defaults": "Réinitialiser",
        "reset_defaults_confirm": "Réinitialiser tous les paramètres par défaut ?",
        "reset_defaults_done": "Paramètres réinitialisés",
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
        # Mode avancé
        "advanced_mode": "Mode avancé",
        "advanced_mode_desc": "Afficher les fonctionnalités avancées",
        "simple_mode": "Mode simple",
        "profiles": "Profils",
        "save_profile": "Sauvegarder le profil",
        "load_profile": "Charger un profil",
        "delete_profile": "Supprimer le profil",
        "profile_name": "Nom du profil",
        "profile_saved": "Profil '{}' sauvegardé",
        "profile_loaded": "Profil '{}' chargé",
        "profile_deleted": "Profil '{}' supprimé",
        "schedule": "Planification",
        "schedule_enabled": "Activer la planification",
        "schedule_start": "Heure de début",
        "schedule_end": "Heure de fin",
        "schedule_days": "Jours actifs",
        "auto_activation": "Auto-activation",
        "auto_activation_enabled": "Activer quand une application se lance",
        "auto_activation_desc": "Active automatiquement ce service quand une des applications ci-dessous est en cours",
        "auto_activation_filter": "Filtrer...",
        "default_volume": "Volume par défaut",
        "default_volume_enabled": "Définir le volume au démarrage",
        "default_volume_desc": "Remet les applications au volume spécifié au lancement",
        "startup_with_windows": "Démarrer avec Windows",
        "startup_enabled": "Lancer au démarrage de Windows",
        "statistics": "Statistiques",
        "usage_count": "Utilisations",
        "last_used": "Dernière utilisation",
        "check_updates": "Vérifier les mises à jour",
        "update_available": "Mise à jour disponible : v{}",
        "no_update": "Vous avez la dernière version",
        "auto_backup": "Sauvegarde automatique",
        "backup_enabled": "Activer la sauvegarde auto",
        "backup_interval": "Intervalle (heures)",
        "search_services": "Rechercher un service...",
        "monday": "Lundi",
        "tuesday": "Mardi",
        "wednesday": "Mercredi",
        "thursday": "Jeudi",
        "friday": "Vendredi",
        "saturday": "Samedi",
        "sunday": "Dimanche",
        "default_vol_apps": "Applications concernées",
        "default_vol_level": "Volume au démarrage (%)",
        "default_vol_applied": "Volume par défaut appliqué à {} application(s)",
        "schedule_active": "Planification active",
        "schedule_inactive": "Planification inactive",
        "app_detected": "Application détectée: {}",
        "service_auto_started": "Service '{}' démarré automatiquement",
        "service_auto_stopped": "Service '{}' arrêté automatiquement",
        "select_apps": "Sélectionner les applications...",
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
        "duplicate_name": "A service named '{}' already exists.",
        "schedule_invalid_time": "End time must be after start time.",
        "tray_stop_all": "Stop all",
        "stop_all_done": "{} service(s) stopped",
        "reset_defaults": "Reset",
        "reset_defaults_confirm": "Reset all settings to defaults?",
        "reset_defaults_done": "Settings reset to defaults",
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
        # Advanced mode
        "advanced_mode": "Advanced mode",
        "advanced_mode_desc": "Show advanced features",
        "simple_mode": "Simple mode",
        "profiles": "Profiles",
        "save_profile": "Save profile",
        "load_profile": "Load profile",
        "delete_profile": "Delete profile",
        "profile_name": "Profile name",
        "profile_saved": "Profile '{}' saved",
        "profile_loaded": "Profile '{}' loaded",
        "profile_deleted": "Profile '{}' deleted",
        "schedule": "Schedule",
        "schedule_enabled": "Enable scheduling",
        "schedule_start": "Start time",
        "schedule_end": "End time",
        "schedule_days": "Active days",
        "auto_activation": "Auto-activation",
        "auto_activation_enabled": "Enable when an application launches",
        "auto_activation_desc": "Automatically enables this service when one of the applications below is running",
        "auto_activation_filter": "Filter...",
        "default_volume": "Default volume",
        "default_volume_enabled": "Set volume on startup",
        "default_volume_desc": "Resets applications to specified volume on launch",
        "startup_with_windows": "Start with Windows",
        "startup_enabled": "Launch at Windows startup",
        "statistics": "Statistics",
        "usage_count": "Usage count",
        "last_used": "Last used",
        "check_updates": "Check for updates",
        "update_available": "Update available: v{}",
        "no_update": "You have the latest version",
        "auto_backup": "Auto backup",
        "backup_enabled": "Enable auto backup",
        "backup_interval": "Interval (hours)",
        "search_services": "Search services...",
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
        "default_vol_apps": "Target applications",
        "default_vol_level": "Volume on startup (%)",
        "default_vol_applied": "Default volume applied to {} application(s)",
        "schedule_active": "Schedule active",
        "schedule_inactive": "Schedule inactive",
        "app_detected": "Application detected: {}",
        "service_auto_started": "Service '{}' auto-started",
        "service_auto_stopped": "Service '{}' auto-stopped",
        "select_apps": "Select applications...",
    }
}

# Variables globales
_current_lang = "fr"
_current_theme = "dark"
_advanced_mode = False

def tr(key: str) -> str:
    """Retourne la traduction pour la clé donnée"""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["fr"]).get(key, key)

def is_dark_theme() -> bool:
    return _current_theme == "dark"

def is_advanced_mode() -> bool:
    return _advanced_mode


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
                    "content": "A 'service' is a volume reduction rule.\n\n1. Give it a name (e.g., 'Lower Spotify')\n\n2. Configure a keyboard shortcut by clicking 'Record...' and pressing your desired key combination\n\n3. Select the target applications whose volume should be reduced"
                },
                {
                    "title": "Step 2: Audio Settings",
                    "content": "• Reduction: How much to lower the volume (75% reduces the volume by 75% of its current level)\n\n• Mode:\n  - Hold: Keep the key pressed to reduce\n  - Toggle: Press once to reduce, press again to restore\n\n• Fade: Transition duration in milliseconds\n\n• Curve: Linear (constant) or Expo (more natural)"
                },
                {
                    "title": "Step 3: Start the Service",
                    "content": "Once configured:\n\n1. Click 'New service' to add it to the list\n   (action buttons are always visible at the bottom)\n\n2. Double-click on a service to start it\n\n3. The indicator turns green when active\n\n4. Use your shortcut to control the volume!\n\nTip: Services are automatically restored when you reopen the app."
                },
                {
                    "title": "You're Ready!",
                    "content": "You now know the basics of SoundLowerer Plus.\n\nOther features:\n• Right-click on a service for more options\n• Export/import your services to share them\n• Use keyboard shortcuts: Delete, Enter, Space\n• Drag & drop to reorder services\n• Search services by name\n• Enable Advanced Mode in settings for profiles, statistics, and more!\n\nEnjoy!"
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
                    "content": "Un 'service' est une règle de réduction de volume.\n\n1. Donnez-lui un nom (ex: 'Baisser Spotify')\n\n2. Configurez un raccourci clavier en cliquant sur 'Enregistrer...' et en appuyant sur la combinaison souhaitée\n\n3. Sélectionnez les applications cibles dont le volume doit être réduit"
                },
                {
                    "title": "Étape 2 : Paramètres Audio",
                    "content": "• Réduction : De combien baisser le volume (75% réduit le volume de 75% par rapport à son niveau actuel)\n\n• Mode :\n  - Hold : Maintenir la touche appuyée pour réduire\n  - Toggle : Appuyer une fois pour réduire, encore pour restaurer\n\n• Fondu : Durée de la transition en millisecondes\n\n• Courbe : Linéaire (constante) ou Expo (plus naturelle)"
                },
                {
                    "title": "Étape 3 : Démarrer le Service",
                    "content": "Une fois configuré :\n\n1. Cliquez sur 'Nouveau service' pour l'ajouter à la liste\n   (les boutons d'action sont toujours visibles en bas)\n\n2. Double-cliquez sur un service pour le démarrer\n\n3. L'indicateur devient vert quand il est actif\n\n4. Utilisez votre raccourci pour contrôler le volume !\n\nAstuce : Les services sont automatiquement restaurés quand vous rouvrez l'app."
                },
                {
                    "title": "Vous êtes prêt !",
                    "content": "Vous connaissez maintenant les bases de SoundLowerer Plus.\n\nAutres fonctionnalités :\n• Clic droit sur un service pour plus d'options\n• Exportez/importez vos services pour les partager\n• Utilisez les raccourcis clavier : Suppr, Entrée, Espace\n• Glissez-déposez pour réorganiser les services\n• Recherchez les services par nom\n• Activez le Mode Avancé dans les paramètres pour les profils, statistiques, et plus !\n\nBonne utilisation !"
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
    def __init__(self, current_lang: str, current_theme: str, close_to_tray: bool = True,
                 advanced_mode: bool = False, startup_with_windows: bool = False,
                 auto_backup: bool = False, backup_interval: int = 24,
                 default_volume_enabled: bool = False, default_volume_level: int = 100,
                 default_volume_apps: list = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("settings"))
        self.setMinimumWidth(400)
        self._close_to_tray = close_to_tray
        self._advanced_mode = advanced_mode
        self._startup_with_windows = startup_with_windows
        self._auto_backup = auto_backup
        self._backup_interval = backup_interval
        self._default_volume_enabled = default_volume_enabled
        self._default_volume_level = default_volume_level
        self._default_volume_apps = default_volume_apps or []

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

        # Mode avancé
        self.advanced_mode_chk = QCheckBox(tr("advanced_mode"))
        self.advanced_mode_chk.setToolTip(tr("advanced_mode_desc"))
        self.advanced_mode_chk.setChecked(self._advanced_mode)
        self.advanced_mode_chk.stateChanged.connect(self._on_advanced_mode_changed)
        behavior_layout.addWidget(self.advanced_mode_chk)

        layout.addWidget(behavior_group)

        # Options avancées (visibles seulement en mode avancé)
        self.advanced_group = QGroupBox(tr("advanced_mode"))
        advanced_layout = QVBoxLayout(self.advanced_group)

        # Démarrage avec Windows
        self.startup_chk = QCheckBox(tr("startup_enabled"))
        self.startup_chk.setChecked(self._startup_with_windows)
        advanced_layout.addWidget(self.startup_chk)

        # Backup automatique
        backup_row = QHBoxLayout()
        self.backup_chk = QCheckBox(tr("backup_enabled"))
        self.backup_chk.setChecked(self._auto_backup)
        backup_row.addWidget(self.backup_chk)

        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 168)
        self.backup_interval_spin.setValue(self._backup_interval)
        self.backup_interval_spin.setSuffix(" h")
        backup_row.addWidget(self.backup_interval_spin)
        backup_row.addStretch()

        advanced_layout.addLayout(backup_row)

        # Bouton vérifier mises à jour
        self.check_updates_btn = QPushButton(tr("check_updates"))
        self.check_updates_btn.clicked.connect(self._check_updates)
        advanced_layout.addWidget(self.check_updates_btn)

        layout.addWidget(self.advanced_group)

        # === Volume par défaut au démarrage ===
        self.default_vol_group = QGroupBox(tr("default_volume"))
        default_vol_layout = QVBoxLayout(self.default_vol_group)

        self.default_vol_chk = QCheckBox(tr("default_volume_enabled"))
        self.default_vol_chk.setToolTip(tr("default_volume_desc"))
        self.default_vol_chk.setChecked(self._default_volume_enabled)
        default_vol_layout.addWidget(self.default_vol_chk)

        # Slider pour le niveau de volume
        vol_row = QHBoxLayout()
        vol_row.addWidget(QLabel(tr("default_vol_level")))
        self.default_vol_slider = QSlider(Qt.Horizontal)
        self.default_vol_slider.setRange(0, 100)
        self.default_vol_slider.setValue(self._default_volume_level)
        self.default_vol_label = QLabel(f"{self._default_volume_level}%")
        self.default_vol_label.setMinimumWidth(40)
        self.default_vol_slider.valueChanged.connect(lambda v: self.default_vol_label.setText(f"{v}%"))
        vol_row.addWidget(self.default_vol_slider)
        vol_row.addWidget(self.default_vol_label)
        default_vol_layout.addLayout(vol_row)

        # Bouton pour sélectionner les applications
        self.default_vol_apps_btn = QPushButton(tr("select_apps"))
        self.default_vol_apps_btn.clicked.connect(self._select_default_vol_apps)
        default_vol_layout.addWidget(self.default_vol_apps_btn)

        # Label pour afficher les apps sélectionnées
        self.default_vol_apps_label = QLabel(", ".join(self._default_volume_apps) if self._default_volume_apps else "-")
        self.default_vol_apps_label.setWordWrap(True)
        self.default_vol_apps_label.setStyleSheet("font-size: 11px; color: #888;")
        default_vol_layout.addWidget(self.default_vol_apps_label)

        layout.addWidget(self.default_vol_group)
        self.default_vol_group.setVisible(self._advanced_mode)

        # Afficher/cacher selon le mode
        self.advanced_group.setVisible(self._advanced_mode)

        # Bouton tutoriel
        tutorial_btn = QPushButton(tr("replay_tutorial"))
        tutorial_btn.clicked.connect(self._show_tutorial)
        layout.addWidget(tutorial_btn)

        # Bouton réinitialiser
        reset_btn = QPushButton(tr("reset_defaults"))
        reset_btn.clicked.connect(self._reset_defaults)
        layout.addWidget(reset_btn)

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
        self._reset_requested = False

    def _show_tutorial(self):
        self._tutorial_requested = True
        self.accept()

    def _reset_defaults(self):
        reply = QMessageBox.question(self, tr("reset_defaults"),
                                     tr("reset_defaults_confirm"),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.lang_combo.setCurrentIndex(self.lang_combo.findData("fr"))
            self.theme_combo.setCurrentIndex(self.theme_combo.findData("dark"))
            self.close_to_tray_chk.setChecked(True)
            self.advanced_mode_chk.setChecked(False)
            self.startup_chk.setChecked(False)
            self.backup_chk.setChecked(False)
            self.backup_interval_spin.setValue(24)
            self.default_vol_chk.setChecked(False)
            self.default_vol_slider.setValue(100)
            self._default_volume_apps = []
            self.default_vol_apps_label.setText("-")
            self._reset_requested = True

    def _on_advanced_mode_changed(self, state):
        """Affiche/cache les options avancées"""
        visible = state == Qt.Checked
        self.advanced_group.setVisible(visible)
        if hasattr(self, 'default_vol_group'):
            self.default_vol_group.setVisible(visible)
        self.adjustSize()

    def _select_default_vol_apps(self):
        """Ouvre un dialogue pour sélectionner les applications pour le volume par défaut"""
        from audio_backend import unique_apps

        dialog = QDialog(self)
        dialog.setWindowTitle(tr("default_vol_apps"))
        dialog.setMinimumSize(300, 400)

        if is_dark_theme():
            dialog.setStyleSheet("""
                QDialog { background: #1e1e1e; }
                QLabel { color: #e0e0e0; }
                QListWidget { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; }
                QListWidget::item:selected { background: #3d6a7a; }
                QPushButton { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 6px 12px; }
                QPushButton:hover { background: #353535; }
            """)
        else:
            dialog.setStyleSheet("""
                QDialog { background: #f5f5f5; }
                QLabel { color: #333; }
                QListWidget { background: #fff; color: #333; border: 1px solid #d0d0d0; border-radius: 4px; }
                QListWidget::item:selected { background: #2563eb; color: white; }
                QPushButton { background: #e8e8e8; color: #333; border: 1px solid #d0d0d0; border-radius: 4px; padding: 6px 12px; }
                QPushButton:hover { background: #d8d8d8; }
            """)

        layout = QVBoxLayout(dialog)

        # Liste des applications
        app_list = QListWidget()
        app_list.setSelectionMode(QAbstractItemView.MultiSelection)

        # Récupérer les apps audio
        apps = unique_apps(force_refresh=True)

        # Ajouter les apps sélectionnées qui ne sont peut-être plus actives
        for app in self._default_volume_apps:
            if app not in apps:
                apps.append(app)

        for app in sorted(apps):
            item = QListWidgetItem(app)
            app_list.addItem(item)
            if app in self._default_volume_apps:
                item.setSelected(True)

        layout.addWidget(app_list)

        # Boutons
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.clicked.connect(dialog.reject)
        ok_btn = QPushButton(tr("ok"))
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

        if dialog.exec_() == QDialog.Accepted:
            self._default_volume_apps = [item.text() for item in app_list.selectedItems()]
            self.default_vol_apps_label.setText(", ".join(self._default_volume_apps) if self._default_volume_apps else "-")

    def _check_updates(self):
        """Vérifie les mises à jour sur GitHub"""
        try:
            import urllib.request
            url = "https://api.github.com/repos/BabasGames/SoundLowerer/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'SoundLowerer'})
            with urllib.request.urlopen(req, timeout=5) as response:
                import json
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "").lstrip("v")
                from version import VERSION
                current_version = VERSION.lstrip("v").split("-")[0]  # Enlever -beta etc.

                if latest_version and latest_version != current_version:
                    QMessageBox.information(self, tr("check_updates"),
                        tr("update_available").format(latest_version))
                else:
                    QMessageBox.information(self, tr("check_updates"), tr("no_update"))
        except Exception as e:
            QMessageBox.warning(self, tr("check_updates"), f"Erreur: {e}")

    def tutorial_requested(self) -> bool:
        return self._tutorial_requested

    def reset_requested(self) -> bool:
        return self._reset_requested

    def get_settings(self) -> Dict:
        return {
            "language": self.lang_combo.currentData(),
            "theme": self.theme_combo.currentData(),
            "close_to_tray": self.close_to_tray_chk.isChecked(),
            "advanced_mode": self.advanced_mode_chk.isChecked(),
            "startup_with_windows": self.startup_chk.isChecked(),
            "auto_backup": self.backup_chk.isChecked(),
            "backup_interval": self.backup_interval_spin.value(),
            "default_volume_enabled": self.default_vol_chk.isChecked(),
            "default_volume_level": self.default_vol_slider.value(),
            "default_volume_apps": self._default_volume_apps,
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


class ResizableScrollArea(QWidget):
    """ScrollArea avec un handle en bas pour redimensionner verticalement par drag."""

    def __init__(self, scroll_area: QScrollArea, min_h: int = 80, default_h: int = 150, parent=None):
        super().__init__(parent)
        self._scroll = scroll_area
        self._min_h = min_h
        self._current_h = default_h
        self._dragging = False
        self._drag_start_y = 0
        self._drag_start_h = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Retirer les contraintes de taille de la scroll area
        self._scroll.setMinimumHeight(0)
        self._scroll.setMaximumHeight(16777215)
        self._scroll.setFixedHeight(self._current_h)

        layout.addWidget(self._scroll)

        # Handle de drag
        self._handle = QWidget()
        self._handle.setFixedHeight(8)
        self._handle.setCursor(Qt.SizeVerCursor)
        self._handle.installEventFilter(self)
        layout.addWidget(self._handle)

        self._update_handle_style()

    def _update_handle_style(self):
        if is_dark_theme():
            self._handle.setStyleSheet(
                "background: #2a2a2a; border-bottom-left-radius: 4px; border-bottom-right-radius: 4px;"
            )
        else:
            self._handle.setStyleSheet(
                "background: #e0e0e0; border-bottom-left-radius: 4px; border-bottom-right-radius: 4px;"
            )

    def refresh_style(self):
        self._update_handle_style()

    def eventFilter(self, obj, event):
        if obj is self._handle:
            if event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
                self._dragging = True
                self._drag_start_y = event.globalPos().y()
                self._drag_start_h = self._current_h
                return True
            elif event.type() == event.MouseMove and self._dragging:
                delta = event.globalPos().y() - self._drag_start_y
                new_h = max(self._min_h, self._drag_start_h + delta)
                self._current_h = new_h
                self._scroll.setFixedHeight(new_h)
                return True
            elif event.type() == event.MouseButtonRelease and self._dragging:
                self._dragging = False
                return True
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        # Dessiner les traits de grip sur le handle
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        handle_rect = self._handle.geometry()
        cx = handle_rect.center().x()
        cy = handle_rect.center().y()
        color = QColor("#555") if is_dark_theme() else QColor("#bbb")
        painter.setPen(QPen(color, 1))
        for dx in [-8, 0, 8]:
            painter.drawLine(cx + dx - 2, cy, cx + dx + 2, cy)


class StatusIndicator(QWidget):
    """Rond coloré avec glow quand actif, pulse quand utilisé"""
    def __init__(self, active=False, parent=None):
        super().__init__(parent)
        self._active = active
        self._pulse = False
        self._pulse_timer = None
        self.setFixedSize(18, 18)

    def set_active(self, active: bool):
        self._active = active
        self.update()

    def pulse(self):
        """Déclenche un bref flash lumineux."""
        self._pulse = True
        self.update()
        if self._pulse_timer is None:
            self._pulse_timer = QTimer(self)
            self._pulse_timer.setSingleShot(True)
            self._pulse_timer.timeout.connect(self._end_pulse)
        self._pulse_timer.start(400)

    def _end_pulse(self):
        self._pulse = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self._active:
            # Glow effect (plus grand en pulse)
            glow = QRadialGradient(9, 9, 9)
            if self._pulse:
                glow.setColorAt(0, QColor(34, 197, 94, 200))
                glow.setColorAt(1, QColor(34, 197, 94, 0))
            else:
                glow.setColorAt(0, QColor(34, 197, 94, 120))
                glow.setColorAt(1, QColor(34, 197, 94, 0))
            painter.setBrush(glow)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 18, 18)
            # Core dot
            color = QColor("#4ade80") if self._pulse else QColor("#22c55e")
            painter.setBrush(color)
            painter.drawEllipse(4, 4, 10, 10)
        else:
            if is_dark_theme():
                painter.setBrush(QColor("#525252"))
            else:
                painter.setBrush(QColor("#d0d0d0"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(4, 4, 10, 10)


class ServiceItemWidget(QWidget):
    """Widget personnalisé pour afficher un service dans la liste"""
    clicked = pyqtSignal(int)
    doubleClicked = pyqtSignal(int)

    def __init__(self, index: int, name: str, hotkey: str, active: bool = False,
                 reduction: int = 75, mode: str = "hold", parent=None):
        super().__init__(parent)
        self.index = index
        self._selected = False
        self._active = active
        self._drag_start_pos = None
        self.setMinimumHeight(52)
        self.setCursor(Qt.PointingHandCursor)
        self.setAutoFillBackground(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 10, 8)
        layout.setSpacing(10)

        # Indicateur de statut
        self.indicator = StatusIndicator(active)
        layout.addWidget(self.indicator)

        # Infos du service
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        self.name_label = QLabel(name)
        hotkey_text = hotkey if hotkey else tr("no_hotkey")
        mode_text = mode
        self.hotkey_label = QLabel(f"{hotkey_text}  ·  {mode_text}")

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.hotkey_label)

        layout.addLayout(info_layout, 1)

        # Badge réduction
        self.reduction_label = QLabel(f"{reduction}%")
        self.reduction_label.setAlignment(Qt.AlignCenter)
        self.reduction_label.setFixedWidth(40)
        layout.addWidget(self.reduction_label)

        self._update_style()

    def set_active(self, active: bool):
        self._active = active
        self.indicator.set_active(active)
        self._update_style()

    def set_selected(self, selected: bool):
        self._selected = selected
        self._update_style()

    def _update_style(self):
        if is_dark_theme():
            if self._selected:
                self.setStyleSheet(
                    "ServiceItemWidget { background: #1e2d3d; border-left: 3px solid #5a9aad; border-radius: 10px; }"
                )
                self.name_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #e8e8e8; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #8ab4c8; background: transparent;")
                self.reduction_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #e0e0e0; background: #2a4a5a; border-radius: 4px; padding: 2px;")
            else:
                self.setStyleSheet(
                    "ServiceItemWidget { background: #242424; border-left: 3px solid transparent; border-radius: 10px; }"
                    " ServiceItemWidget:hover { background: #2c2c2c; }"
                )
                self.name_label.setStyleSheet("font-weight: 500; font-size: 13px; color: #d0d0d0; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #707070; background: transparent;")
                self.reduction_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #909090; background: #2a3a44; border-radius: 4px; padding: 2px;")
        else:
            if self._selected:
                self.setStyleSheet(
                    "ServiceItemWidget { background: #e8f0fe; border-left: 3px solid #2563eb; border-radius: 10px; }"
                )
                self.name_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #1a1a1a; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #3b72c4; background: transparent;")
                self.reduction_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #1e40af; background: #d0dff8; border-radius: 4px; padding: 2px;")
            else:
                self.setStyleSheet(
                    "ServiceItemWidget { background: #ffffff; border-left: 3px solid transparent; border-radius: 10px; border: 1px solid #e8e8e8; }"
                    " ServiceItemWidget:hover { background: #f5f5f5; }"
                )
                self.name_label.setStyleSheet("font-weight: 500; font-size: 13px; color: #333333; background: transparent;")
                self.hotkey_label.setStyleSheet("font-size: 11px; color: #888888; background: transparent;")
                self.reduction_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #555; background: #e8eff8; border-radius: 4px; padding: 2px;")

    def update_info(self, name: str, hotkey: str, reduction: int = None, mode: str = None):
        self.name_label.setText(name)
        hotkey_text = hotkey if hotkey else tr("no_hotkey")
        mode_text = mode or "hold"
        self.hotkey_label.setText(f"{hotkey_text}  ·  {mode_text}")
        if reduction is not None:
            self.reduction_label.setText(f"{reduction}%")

    def paintEvent(self, event):
        """Nécessaire pour que le background du stylesheet s'affiche sur un QWidget custom."""
        from PyQt5.QtWidgets import QStyleOption, QStyle
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
            self._drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_start_pos:
            if (event.pos() - self._drag_start_pos).manhattanLength() > 10:
                self._start_drag()
        super().mouseMoveEvent(event)

    def _start_drag(self):
        from PyQt5.QtCore import QMimeData
        from PyQt5.QtGui import QDrag

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.index))
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
        self._drag_start_pos = None

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit(self.index)
        super().mouseDoubleClickEvent(event)


class ServiceListWidget(QWidget):
    """Liste personnalisée de services avec support drag & drop"""
    selectionChanged = pyqtSignal(int)
    itemDoubleClicked = pyqtSignal(int)
    orderChanged = pyqtSignal(int, int)  # Signal émis quand l'ordre change (from_idx, to_idx)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: List[ServiceItemWidget] = []
        self._selected_index = -1
        self._drag_start_pos = None
        self._drag_item_index = -1

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(4)
        self.layout.addStretch()

        self.setAcceptDrops(True)

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

    def add_item(self, index: int, name: str, hotkey: str, active: bool = False,
                 reduction: int = 75, mode: str = "hold"):
        item = ServiceItemWidget(index, name, hotkey, active, reduction, mode)
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

    def pulse_item(self, index: int):
        """Déclenche un pulse sur l'indicateur d'un service."""
        if 0 <= index < len(self._items):
            self._items[index].indicator.pulse()

    def update_item(self, index: int, name: str, hotkey: str,
                    reduction: int = None, mode: str = None):
        if 0 <= index < len(self._items):
            self._items[index].update_info(name, hotkey, reduction, mode)

    def get_item_at(self, pos) -> int:
        """Retourne l'index de l'item à la position donnée, ou -1"""
        for item in self._items:
            if item.geometry().contains(pos):
                return item.index
        return -1

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            from_index = int(event.mimeData().text())
            to_index = self.get_item_at(event.pos())

            if to_index == -1:
                # Droppé en dehors d'un item, mettre à la fin
                to_index = len(self._items) - 1

            if from_index != to_index and from_index >= 0 and to_index >= 0:
                self.orderChanged.emit(from_index, to_index)

            event.acceptProposedAction()

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
        global _current_lang, _advanced_mode
        _current_lang = self.data.get("settings", {}).get("language", "fr")
        self._current_theme = self.data.get("settings", {}).get("theme", "dark")
        self._close_to_tray = self.data.get("settings", {}).get("close_to_tray", True)
        _advanced_mode = self.data.get("settings", {}).get("advanced_mode", False)
        self._advanced_mode = _advanced_mode
        self._startup_with_windows = self.data.get("settings", {}).get("startup_with_windows", False)
        self._auto_backup = self.data.get("settings", {}).get("auto_backup", False)
        self._backup_interval = self.data.get("settings", {}).get("backup_interval", 24)
        self._default_volume_enabled = self.data.get("settings", {}).get("default_volume_enabled", False)
        self._default_volume_level = self.data.get("settings", {}).get("default_volume_level", 100)
        self._default_volume_apps = self.data.get("settings", {}).get("default_volume_apps", [])
        self._force_quit = False  # Pour distinguer fermeture réelle de minimisation

        self.setWindowTitle(tr("app_title"))
        self.resize(900, 650)

        # Charger le thème
        self._apply_theme()
        self.services: List[Dict] = self.data.get("services", [])
        self.controllers: Dict[int, VolumeServiceController] = {}
        self._auto_started: set = set()  # Services démarrés automatiquement (schedule/jeux)
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

        # Appliquer le volume par défaut si activé
        if self._default_volume_enabled and self._default_volume_apps:
            QTimer.singleShot(1000, self._apply_default_volume)

        # Démarrer l'auto-activation si des services l'utilisent
        self._setup_auto_activation()

        # Démarrer la vérification de planification
        self._setup_schedule_check()

        # Appliquer le thème une seconde fois pour les éléments créés après
        self._apply_theme()

        # Initialiser le backup automatique si activé
        if self._auto_backup:
            self._setup_auto_backup()

        # Raccourcis clavier dans l'app
        self._setup_shortcuts()

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
                self.empty_state.setStyleSheet("background: #f5f5f5;")
                self.empty_title.setStyleSheet("font-size: 15px; font-weight: 600; color: #666; background: transparent;")
                self.empty_desc.setStyleSheet("font-size: 12px; color: #999; background: transparent;")
                self.targets_resizable.refresh_style()
                if hasattr(self, 'trigger_scroll'):
                    self.trigger_scroll.setStyleSheet("QScrollArea { border: 1px solid #d0d0d0; border-radius: 6px; background: #ffffff; }")
                    self.trigger_container.setStyleSheet("background: #ffffff;")
                    self.trigger_resizable.refresh_style()
            else:
                self.service_scroll.setStyleSheet("background: #1a1a1a;")
                self.list_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #7eb8c9; padding: 12px; background: #1a1a1a;")
                self.service_list.setStyleSheet("background: #1a1a1a;")
                self.targets_scroll.setStyleSheet("QScrollArea { border: 1px solid #2d2d2d; border-radius: 6px; background: #222222; }")
                self.targets_container.setStyleSheet("background: #222222;")
                self.empty_state.setStyleSheet("background: #1a1a1a;")
                self.empty_title.setStyleSheet("font-size: 15px; font-weight: 600; color: #606060; background: transparent;")
                self.empty_desc.setStyleSheet("font-size: 12px; color: #484848; background: transparent;")
                self.targets_resizable.refresh_style()
                if hasattr(self, 'trigger_scroll'):
                    self.trigger_scroll.setStyleSheet("QScrollArea { border: 1px solid #2d2d2d; border-radius: 6px; background: #222222; }")
                    self.trigger_container.setStyleSheet("background: #222222;")
                    self.trigger_resizable.refresh_style()

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

        # Champ de recherche pour filtrer les services
        self.search_services_edit = QLineEdit()
        self.search_services_edit.setPlaceholderText(tr("search_services"))
        self.search_services_edit.textChanged.connect(self._filter_services)
        self.search_services_edit.setStyleSheet("margin: 0 8px 8px 8px;")

        # Scroll area pour la liste
        scroll_list = QScrollArea()
        scroll_list.setWidgetResizable(True)
        scroll_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_list.setFrameShape(QFrame.NoFrame)
        self.service_scroll = scroll_list  # Garder référence pour le thème

        self.service_list = ServiceListWidget()
        self.service_list.selectionChanged.connect(self._on_service_selected)
        self.service_list.itemDoubleClicked.connect(self._toggle_service)
        self.service_list.orderChanged.connect(self._on_service_order_changed)
        self.service_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.service_list.customContextMenuRequested.connect(self._show_context_menu)

        scroll_list.setWidget(self.service_list)

        # Empty state
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_icon = QLabel("—")
        empty_icon.setStyleSheet("font-size: 28px; background: transparent; color: #555;")
        empty_icon.setAlignment(Qt.AlignCenter)
        self.empty_title = QLabel(tr("services"))
        self.empty_title.setAlignment(Qt.AlignCenter)
        self.empty_desc = QLabel(
            "Create your first service\nto control volume" if _current_lang == "en"
            else "Créez votre premier service\npour contrôler le volume"
        )
        self.empty_desc.setAlignment(Qt.AlignCenter)
        self.empty_desc.setWordWrap(True)
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(self.empty_title)
        empty_layout.addWidget(self.empty_desc)
        self.empty_state.setVisible(False)

        left_layout.addWidget(self.list_label)
        left_layout.addWidget(self.search_services_edit)
        left_layout.addWidget(scroll_list)
        left_layout.addWidget(self.empty_state)

        central.addWidget(left_widget)

        # === Panneau de droite avec scroll + actions sticky ===
        right_wrapper = QWidget()
        right_wrapper_layout = QVBoxLayout(right_wrapper)
        right_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        right_wrapper_layout.setSpacing(0)

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

        # === Groupe: Applications Cibles ===
        grp_targets = QGroupBox(tr("target_apps"))
        grp_targets_layout = QVBoxLayout(grp_targets)
        grp_targets_layout.setSpacing(8)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(tr("filter_apps"))
        self.filter_edit.setToolTip(tr("tooltip_filter_apps"))
        self.filter_edit.textChanged.connect(self._filter_apps)

        # Scroll area pour les checkboxes (redimensionnable)
        targets_scroll = QScrollArea()
        targets_scroll.setWidgetResizable(True)
        targets_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.targets_scroll = targets_scroll  # Garder référence pour le thème

        self.targets_container = QWidget()
        self.targets_layout = QVBoxLayout(self.targets_container)
        self.targets_layout.setContentsMargins(8, 8, 8, 8)
        self.targets_layout.setSpacing(4)
        self.targets_layout.addStretch()

        targets_scroll.setWidget(self.targets_container)
        self.targets_checkboxes: Dict[str, QCheckBox] = {}
        self.targets_resizable = ResizableScrollArea(targets_scroll, min_h=80, default_h=150)

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
        grp_targets_layout.addWidget(self.targets_resizable)
        grp_targets_layout.addLayout(add_app_row)
        grp_targets_layout.addLayout(targets_btn_row)

        rv.addWidget(grp_targets)

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
        self.reduct_slider.valueChanged.connect(self._on_reduction_changed)

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

        # === Groupe: Profils (mode avancé) ===
        self.grp_profiles = QGroupBox(tr("profiles"))
        grp_profiles_layout = QHBoxLayout(self.grp_profiles)

        self.save_profile_btn = QPushButton(tr("save_profile"))
        self.save_profile_btn.clicked.connect(self._save_profile)

        self.load_profile_btn = QPushButton(tr("load_profile"))
        self.load_profile_btn.clicked.connect(self._load_profile)

        grp_profiles_layout.addWidget(self.save_profile_btn)
        grp_profiles_layout.addWidget(self.load_profile_btn)

        rv.addWidget(self.grp_profiles)
        self.grp_profiles.setVisible(self._advanced_mode)

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

        # === Groupe: Statistiques (mode avancé) ===
        self.grp_stats = QGroupBox(tr("statistics"))
        grp_stats_layout = QVBoxLayout(self.grp_stats)
        grp_stats_layout.setSpacing(8)

        stats_row1 = QHBoxLayout()
        stats_row1.addWidget(QLabel(tr("usage_count") + ":"))
        self.usage_count_label = QLabel("0")
        self.usage_count_label.setStyleSheet("font-weight: bold;")
        stats_row1.addWidget(self.usage_count_label)
        stats_row1.addStretch()

        stats_row2 = QHBoxLayout()
        stats_row2.addWidget(QLabel(tr("last_used") + ":"))
        self.last_used_label = QLabel("-")
        stats_row2.addWidget(self.last_used_label)
        stats_row2.addStretch()

        grp_stats_layout.addLayout(stats_row1)
        grp_stats_layout.addLayout(stats_row2)

        # === Groupe: Planification (mode avancé) ===
        self.grp_schedule = QGroupBox(tr("schedule"))
        grp_schedule_layout = QVBoxLayout(self.grp_schedule)
        grp_schedule_layout.setSpacing(8)

        self.schedule_enabled_chk = QCheckBox(tr("schedule_enabled"))
        grp_schedule_layout.addWidget(self.schedule_enabled_chk)

        # Ligne heures
        time_row = QHBoxLayout()
        time_row.addWidget(QLabel(tr("schedule_start")))

        from PyQt5.QtWidgets import QTimeEdit
        from PyQt5.QtCore import QTime
        self.schedule_start_time = QTimeEdit()
        self.schedule_start_time.setDisplayFormat("HH:mm")
        self.schedule_start_time.setTime(QTime(9, 0))
        time_row.addWidget(self.schedule_start_time)

        time_row.addWidget(QLabel(tr("schedule_end")))
        self.schedule_end_time = QTimeEdit()
        self.schedule_end_time.setDisplayFormat("HH:mm")
        self.schedule_end_time.setTime(QTime(18, 0))
        time_row.addWidget(self.schedule_end_time)

        time_row.addStretch()
        grp_schedule_layout.addLayout(time_row)

        # Jours de la semaine
        days_row = QHBoxLayout()
        self.day_checkboxes = {}
        day_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_abbrevs = ["L", "M", "M", "J", "V", "S", "D"] if _current_lang == "fr" else ["M", "T", "W", "T", "F", "S", "S"]

        for i, (key, abbrev) in enumerate(zip(day_keys, day_abbrevs)):
            cb = QCheckBox(abbrev)
            cb.setToolTip(tr(key))
            cb.setChecked(i < 5)  # Lun-Ven cochés par défaut
            self.day_checkboxes[key] = cb
            days_row.addWidget(cb)

        days_row.addStretch()
        grp_schedule_layout.addLayout(days_row)

        rv.addWidget(self.grp_schedule)
        self.grp_schedule.setVisible(self._advanced_mode)

        # === Groupe: Auto-activation (mode avancé) ===
        self.grp_auto_activation = QGroupBox(tr("auto_activation"))
        grp_aa_layout = QVBoxLayout(self.grp_auto_activation)
        grp_aa_layout.setSpacing(8)

        self.auto_activation_chk = QCheckBox(tr("auto_activation_enabled"))
        self.auto_activation_chk.setToolTip(tr("auto_activation_desc"))
        self.auto_activation_chk.stateChanged.connect(self._on_auto_activation_toggled)
        grp_aa_layout.addWidget(self.auto_activation_chk)

        # Conteneur pour la liste d'apps (caché quand désactivé)
        self.trigger_apps_container = QWidget()
        trigger_apps_inner = QVBoxLayout(self.trigger_apps_container)
        trigger_apps_inner.setContentsMargins(0, 0, 0, 0)
        trigger_apps_inner.setSpacing(6)

        # Filtre
        self.trigger_filter_edit = QLineEdit()
        self.trigger_filter_edit.setPlaceholderText(tr("auto_activation_filter"))
        self.trigger_filter_edit.textChanged.connect(self._filter_trigger_apps)
        trigger_apps_inner.addWidget(self.trigger_filter_edit)

        # ScrollArea avec checkboxes (redimensionnable)
        trigger_scroll = QScrollArea()
        trigger_scroll.setWidgetResizable(True)
        trigger_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.trigger_scroll = trigger_scroll

        self.trigger_container = QWidget()
        self.trigger_layout = QVBoxLayout(self.trigger_container)
        self.trigger_layout.setContentsMargins(8, 8, 8, 8)
        self.trigger_layout.setSpacing(4)
        self.trigger_layout.addStretch()

        trigger_scroll.setWidget(self.trigger_container)
        self.trigger_checkboxes: Dict[str, QCheckBox] = {}
        self.trigger_resizable = ResizableScrollArea(trigger_scroll, min_h=60, default_h=120)
        trigger_apps_inner.addWidget(self.trigger_resizable)

        # Ajout manuel
        trigger_add_row = QHBoxLayout()
        self.trigger_add_edit = QLineEdit()
        self.trigger_add_edit.setPlaceholderText("app.exe")
        self.trigger_add_edit.returnPressed.connect(self._add_manual_trigger_app)
        self.trigger_add_btn = QPushButton("+")
        self.trigger_add_btn.setFixedWidth(36)
        self.trigger_add_btn.clicked.connect(self._add_manual_trigger_app)
        trigger_add_row.addWidget(self.trigger_add_edit, 1)
        trigger_add_row.addWidget(self.trigger_add_btn)
        trigger_apps_inner.addLayout(trigger_add_row)

        # Bouton actualiser
        self.trigger_refresh_btn = QPushButton(tr("refresh"))
        self.trigger_refresh_btn.clicked.connect(self._refresh_trigger_apps)
        trigger_apps_inner.addWidget(self.trigger_refresh_btn)

        grp_aa_layout.addWidget(self.trigger_apps_container)
        self.trigger_apps_container.setVisible(False)

        rv.addWidget(self.grp_auto_activation)
        self.grp_auto_activation.setVisible(self._advanced_mode)

        rv.addWidget(self.grp_stats)
        self.grp_stats.setVisible(self._advanced_mode)

        rv.addStretch(1)

        scroll.setWidget(right)
        right_wrapper_layout.addWidget(scroll, 1)
        right_wrapper_layout.addWidget(grp_actions)
        central.addWidget(right_wrapper)
        central.setSizes([280, 500])

        # Barre de statut
        self.setStatusBar(QStatusBar())

    # --- Liste des services ---
    def _load_list(self):
        self.service_list.clear()
        for idx, svc in enumerate(self.services):
            self._add_list_item(svc, idx)
        has_services = len(self.services) > 0
        self.empty_state.setVisible(not has_services)
        self.service_scroll.setVisible(has_services)

    def _add_list_item(self, svc: Dict, idx: int):
        is_active = idx in self.controllers
        name = svc.get("name", "Service sans nom")
        hotkey = svc.get("hotkey", "")
        reduction = svc.get("reduction", 75)
        mode = svc.get("mode", "hold")
        self.service_list.add_item(idx, name, hotkey, is_active, reduction, mode)

    def _update_status_indicators(self):
        for idx in range(len(self.services)):
            is_active = idx in self.controllers
            self.service_list.update_status(idx, is_active)

        # Mettre à jour l'icône et tooltip du tray selon l'état des services
        any_active = len(self.controllers) > 0
        self._update_tray_icon(any_active)
        self._update_tray_tooltip()

    def _update_tray_tooltip(self):
        """Met à jour le tooltip du tray avec le nombre de services actifs."""
        count = len(self.controllers)
        total = len(self.services)
        if count:
            tip = f"SoundLowerer Plus — {count}/{total} actif(s)" if _current_lang == "fr" else f"SoundLowerer Plus — {count}/{total} active"
        else:
            tip = "SoundLowerer Plus"
        self.tray.setToolTip(tip)

    def _update_tray_icon(self, active: bool):
        """Met à jour l'icône du tray selon l'état actif"""
        if active:
            icon_path = os.path.join(resource_path("icons"), "tray_active.svg")
        else:
            icon_path = os.path.join(resource_path("icons"), "tray.svg")

        if os.path.exists(icon_path):
            self.tray.setIcon(QIcon(icon_path))

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

        # Charger les statistiques (mode avancé)
        if self._advanced_mode and hasattr(self, 'usage_count_label'):
            self.usage_count_label.setText(str(svc.get("usage_count", 0)))
            last_used = svc.get("last_used", "")
            if last_used:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_used)
                    self.last_used_label.setText(dt.strftime("%d/%m/%Y %H:%M"))
                except:
                    self.last_used_label.setText("-")
            else:
                self.last_used_label.setText("-")

        # Charger la planification (mode avancé)
        if self._advanced_mode and hasattr(self, 'schedule_enabled_chk'):
            from PyQt5.QtCore import QTime
            self.schedule_enabled_chk.setChecked(svc.get("schedule_enabled", False))
            start_str = svc.get("schedule_start", "09:00")
            end_str = svc.get("schedule_end", "18:00")
            try:
                start_parts = start_str.split(":")
                self.schedule_start_time.setTime(QTime(int(start_parts[0]), int(start_parts[1])))
                end_parts = end_str.split(":")
                self.schedule_end_time.setTime(QTime(int(end_parts[0]), int(end_parts[1])))
            except:
                self.schedule_start_time.setTime(QTime(9, 0))
                self.schedule_end_time.setTime(QTime(18, 0))

            # Jours actifs
            schedule_days = svc.get("schedule_days", ["monday", "tuesday", "wednesday", "thursday", "friday"])
            for key, cb in self.day_checkboxes.items():
                cb.setChecked(key in schedule_days)

        # Charger l'auto-activation (mode avancé)
        if self._advanced_mode and hasattr(self, 'auto_activation_chk'):
            self.auto_activation_chk.setChecked(svc.get("auto_activation", False))
            trigger_apps = svc.get("trigger_apps", [])
            self._build_trigger_apps_checkboxes({app: True for app in trigger_apps})

    def _on_reduction_changed(self, value: int):
        self.reduct_label.setText(f"{value}%")
        self._update_slider_color(value)

    def _update_slider_color(self, value: int):
        """Met à jour la couleur du slider selon la valeur de réduction."""
        if value <= 30:
            color = "#22c55e"  # vert
            handle = "#16a34a"
        elif value <= 70:
            color = "#5a9aad"  # cyan
            handle = "#4a8a9d"
        else:
            color = "#f59e0b"  # orange
            handle = "#d97706"

        self.reduct_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{ height: 6px; background: {"#2a2a2a" if is_dark_theme() else "#d0d0d0"}; border-radius: 3px; }}
            QSlider::sub-page:horizontal {{ background: {color}; border-radius: 3px; }}
            QSlider::handle:horizontal {{ background: {handle}; width: 16px; height: 16px; margin: -5px 0; border-radius: 8px; }}
            QSlider::handle:horizontal:hover {{ background: {color}; }}
        """)

    def _toast(self, text: str, toast_type: str = "info", duration_ms: int = 3000):
        """Affiche un message dans la barre de statut."""
        self.statusBar().showMessage(text, duration_ms)

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
            stop_action = menu.addAction(tr("stop"))
            stop_action.triggered.connect(lambda: self._stop_at_index(idx))
        else:
            start_action = menu.addAction(tr("start"))
            start_action.triggered.connect(lambda: self._start_at_index(idx))

        menu.addSeparator()

        dup_action = menu.addAction(tr("duplicate"))
        dup_action.triggered.connect(lambda: self._duplicate_at_index(idx))

        del_action = menu.addAction(tr("delete"))
        del_action.triggered.connect(lambda: self._delete_at_index(idx))

        menu.exec_(self.service_list.mapToGlobal(pos))

    # --- Tray ---
    def _setup_tray(self):
        self.tray = QSystemTrayIcon(QIcon(os.path.join(resource_path("icons"), "tray.svg")), self)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray_menu = QMenu()
        self.toggle_all_act = self.tray_menu.addAction(tr("tray_toggle_all"))
        self.toggle_all_act.triggered.connect(self._toggle_all)
        self.stop_all_act = self.tray_menu.addAction(tr("tray_stop_all"))
        self.stop_all_act.triggered.connect(self._stop_all_services)
        self.tray_menu.addSeparator()
        self.open_act = self.tray_menu.addAction(tr("tray_open"))
        self.open_act.triggered.connect(self._show_from_tray)
        self.quit_act = self.tray_menu.addAction(tr("tray_quit"))
        self.quit_act.triggered.connect(self._quit_app)
        self.tray.setContextMenu(self.tray_menu)
        self._update_tray_tooltip()
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
        running = bool(self.controllers)
        if running:
            self._stop_all_services()
        else:
            for idx in range(len(self.services)):
                self._start_at_index(idx)
            self._toast(tr("all_started"), "success")
        self._update_tray_tooltip()

    def _stop_all_services(self):
        """Arrête tous les services actifs."""
        count = len(self.controllers)
        for idx, c in list(self.controllers.items()):
            c.stop()
            del self.controllers[idx]
        if count:
            self._toast(tr("stop_all_done").format(count), "info")
        self._update_tray_tooltip()

    # --- Persistance ---
    def _autosave(self):
        if self._dirty:
            self._dirty = False
            self.data["services"] = self.services
            save_config(self.data)
            self._toast(tr("config_saved"), "success")

    # --- Données audio ---
    def _add_manual_app(self):
        """Ajoute manuellement une application à la liste"""
        app_name = self.add_app_edit.text().strip()
        if not app_name:
            return
        # Assurer l'extension .exe si absente
        if not app_name.endswith(".exe"):
            app_name += ".exe"
        app_name = app_name.lower()

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

        self._toast(
            f"'{app_name}' added" if _current_lang == "en" else f"'{app_name}' ajouté",
            "success"
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
        svc = {
            "name": self.name_edit.text() or (targets[0] if targets else "Service"),
            "targets": targets,
            "hotkey": self.hk_edit.text().strip(),
            "reduction": int(self.reduct_slider.value()),
            "mode": self.mode_combo.currentText(),
            "fade_ms": int(self.fade_spin.value()),
            "curve": self.curve_combo.currentText(),
            "all_except": self.all_except_chk.isChecked()
        }

        # Ajouter les champs avancés si disponibles
        if hasattr(self, 'schedule_enabled_chk'):
            svc["schedule_enabled"] = self.schedule_enabled_chk.isChecked()
            svc["schedule_start"] = self.schedule_start_time.time().toString("HH:mm")
            svc["schedule_end"] = self.schedule_end_time.time().toString("HH:mm")
            svc["schedule_days"] = [key for key, cb in self.day_checkboxes.items() if cb.isChecked()]

        if hasattr(self, 'auto_activation_chk'):
            svc["auto_activation"] = self.auto_activation_chk.isChecked()
            svc["trigger_apps"] = [name for name, cb in self.trigger_checkboxes.items() if cb.isChecked()]

        return svc

    def _validate(self, svc: Dict, exclude_idx: int = -1) -> str:
        if not svc["hotkey"]:
            return tr("missing_hotkey")
        if not validate_hotkey(svc["hotkey"]):
            return tr("invalid_hotkey").format(svc['hotkey'])
        # Vérifier les noms dupliqués
        name = svc.get("name", "").strip()
        for i, existing in enumerate(self.services):
            if i == exclude_idx:
                continue
            if existing.get("name", "").strip().lower() == name.lower():
                return tr("duplicate_name").format(name)
        # Vérifier les horaires
        if svc.get("schedule_enabled"):
            start = svc.get("schedule_start", "00:00")
            end = svc.get("schedule_end", "23:59")
            if start >= end:
                return tr("schedule_invalid_time")
        return ""

    def _record_hotkey(self):
        original_text = self.hk_btn.text()
        self.hk_btn.setText(tr("press_keys"))
        self.hk_btn.setObjectName("recordingBtn")
        self.hk_btn.setStyle(self.hk_btn.style())
        self.hk_btn.setEnabled(False)
        self.hk_edit.setEnabled(False)

        # Animation pulsante sur le champ hotkey
        self._recording_pulse = True
        self._pulse_state = False
        accent = "#f59e0b"
        bg = "#3a2a10" if is_dark_theme() else "#fef3c7"
        self._pulse_styles = [
            f"QLineEdit {{ border: 2px solid {accent}; background: {bg}; }}",
            f"QLineEdit {{ border: 2px solid transparent; background: {bg}; }}",
        ]
        self._pulse_timer = QTimer()
        self._pulse_timer.timeout.connect(self._pulse_hotkey_field)
        self._pulse_timer.start(500)
        self.hk_edit.setStyleSheet(self._pulse_styles[0])

        QApplication.processEvents()

        hk = record_hotkey_once()

        # Arrêter l'animation
        self._recording_pulse = False
        self._pulse_timer.stop()
        self.hk_edit.setStyleSheet("")

        self.hk_btn.setText(original_text)
        self.hk_btn.setObjectName("")
        self.hk_btn.setStyle(self.hk_btn.style())
        self.hk_btn.setEnabled(True)
        self.hk_edit.setEnabled(True)

        if hk:
            self.hk_edit.setText(hk)
            # Vérifier les conflits en temps réel
            conflict = self._check_hotkey_conflict(hk)
            if conflict:
                self._toast(tr("hotkey_conflict").format(hk, conflict), "warning")
            else:
                self._toast(tr("hotkey_recorded").format(hk), "success")
        else:
            self._toast(tr("hotkey_cancelled"), "warning")

    def _check_hotkey_conflict(self, hotkey: str) -> str:
        """Vérifie si un raccourci est déjà utilisé. Retourne le nom du service en conflit ou ''."""
        for i, svc in enumerate(self.services):
            if i == self._selected_index:
                continue
            if svc.get("hotkey", "").strip().lower() == hotkey.strip().lower():
                return svc.get("name", "Service")
        return ""

    def _pulse_hotkey_field(self):
        """Alterne le style du champ hotkey pour créer un effet pulsant."""
        if not self._recording_pulse:
            return
        self._pulse_state = not self._pulse_state
        self.hk_edit.setStyleSheet(self._pulse_styles[1 if self._pulse_state else 0])

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
        self._toast(tr("preset_applied").format(preset_name), "info")

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

        # Mettre à jour les données en préservant les statistiques
        old_svc = self.services[self._selected_index]
        for key in ("usage_count", "last_used"):
            if key in old_svc and key not in svc:
                svc[key] = old_svc[key]
        self.services[self._selected_index] = svc
        self._dirty = True

        # Mettre à jour l'affichage dans la liste
        self.service_list.update_item(self._selected_index, svc['name'], svc['hotkey'],
                                      svc.get('reduction', 75), svc.get('mode', 'hold'))

        # Redémarrer si était actif
        if was_active:
            self._start_at_index(self._selected_index)

        # Relancer le timer d'auto-activation si les trigger_apps ont changé
        self._restart_auto_activation_if_needed()

        self._toast(tr("service_modified").format(svc['name']), "success")

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

        # Relancer le timer d'auto-activation si des trigger_apps sont configurées
        self._restart_auto_activation_if_needed()

        self._toast(tr("service_created").format(svc['name']), "success")

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

        self._toast(tr("service_deleted"), "info")

    def _duplicate_at_index(self, idx: int):
        import copy
        svc = copy.deepcopy(self.services[idx])
        svc["name"] = svc.get("name", "") + " (copie)"
        svc["hotkey"] = ""  # Vider le raccourci pour éviter les conflits
        # Réinitialiser les statistiques pour la copie
        svc.pop("usage_count", None)
        svc.pop("last_used", None)

        self.services.append(svc)
        new_idx = len(self.services) - 1
        self._add_list_item(svc, new_idx)
        self._dirty = True

        self.service_list.select(new_idx)
        self._toast(tr("service_duplicated"), "info")

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

        # Callback pour les statistiques et le pulse visuel
        service_idx = idx
        def on_use():
            if self._advanced_mode:
                self._record_service_usage(service_idx)
            # Pulse visuel via signal thread-safe
            QTimer.singleShot(0, lambda: self.service_list.pulse_item(service_idx))

        ctrl = VolumeServiceController(
            name=s.get("name", ""),
            targets=s.get("targets", []),
            hotkey=s.get("hotkey", ""),
            reduction_pct=int(s.get("reduction", 75)),
            mode=s.get("mode", "hold"),
            fade_ms=int(s.get("fade_ms", 300)),
            curve=s.get("curve", "linear"),
            all_except=bool(s.get("all_except", False)),
            on_use_callback=on_use
        )
        self.controllers[idx] = ctrl
        ctrl.start()
        self._toast(tr("service_started").format(s.get('name', '')), "success")

    def _stop_selected(self):
        if self._selected_index < 0:
            return
        self._stop_at_index(self._selected_index)

    def _stop_at_index(self, idx: int):
        if idx not in self.controllers:
            return
        self.controllers[idx].stop()
        del self.controllers[idx]
        self._auto_started.discard(idx)
        self._toast(tr("service_stopped").format(self.services[idx].get('name', '')), "info")

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
        self._toast(tr("test_applied"), "info")
        from threading import Timer
        Timer(0.8, c._restore).start()

    def changeEvent(self, e):
        """Pause les timers de polling quand la fenêtre est minimisée."""
        from PyQt5.QtCore import QEvent
        if e.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self._pause_polling()
            else:
                self._resume_polling()
        super().changeEvent(e)

    def hideEvent(self, e):
        """Pause les timers quand la fenêtre est cachée (tray)."""
        self._pause_polling()
        super().hideEvent(e)

    def showEvent(self, e):
        """Reprend les timers quand la fenêtre est affichée."""
        self._resume_polling()
        super().showEvent(e)

    def _pause_polling(self):
        """Arrête les timers de polling non-essentiels."""
        if hasattr(self, 'refresh_timer') and self.refresh_timer.isActive():
            self.refresh_timer.stop()
        if hasattr(self, 'status_timer') and self.status_timer.isActive():
            self.status_timer.stop()

    def _resume_polling(self):
        """Reprend les timers de polling."""
        if hasattr(self, 'refresh_timer') and not self.refresh_timer.isActive():
            self.refresh_timer.start()
            self._refresh_apps()  # Rafraîchir immédiatement
        if hasattr(self, 'status_timer') and not self.status_timer.isActive():
            self.status_timer.start()
            self._update_status_indicators()

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
            self._toast(tr("restored").format(len(active)), "success")

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
            self._toast(tr("export_success").format(os.path.basename(path)), "success")
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
            self._toast(tr("import_success").format(svc.get("name", "Service")), "success")

        except Exception as e:
            QMessageBox.warning(self, tr("import_btn"), tr("import_error") + f"\n{e}")

    # --- Paramètres ---
    def _open_settings(self):
        """Ouvre le dialogue des paramètres"""
        global _current_lang, _advanced_mode

        dialog = SettingsDialog(
            current_lang=_current_lang,
            current_theme=self._current_theme,
            close_to_tray=self._close_to_tray,
            advanced_mode=self._advanced_mode,
            startup_with_windows=self._startup_with_windows,
            auto_backup=self._auto_backup,
            backup_interval=self._backup_interval,
            default_volume_enabled=self._default_volume_enabled,
            default_volume_level=self._default_volume_level,
            default_volume_apps=self._default_volume_apps,
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

            # Appliquer mode avancé
            if settings["advanced_mode"] != self._advanced_mode:
                self._advanced_mode = settings["advanced_mode"]
                _advanced_mode = self._advanced_mode
                self.data.setdefault("settings", {})["advanced_mode"] = self._advanced_mode
                self._dirty = True
                self._update_advanced_ui()

            # Appliquer démarrage avec Windows
            if settings["startup_with_windows"] != self._startup_with_windows:
                self._startup_with_windows = settings["startup_with_windows"]
                self.data.setdefault("settings", {})["startup_with_windows"] = self._startup_with_windows
                self._apply_startup_with_windows()
                self._dirty = True

            # Appliquer backup auto
            if settings["auto_backup"] != self._auto_backup or settings["backup_interval"] != self._backup_interval:
                self._auto_backup = settings["auto_backup"]
                self._backup_interval = settings["backup_interval"]
                self.data.setdefault("settings", {})["auto_backup"] = self._auto_backup
                self.data.setdefault("settings", {})["backup_interval"] = self._backup_interval
                self._setup_auto_backup()
                self._dirty = True

            # Appliquer volume par défaut
            if (settings["default_volume_enabled"] != self._default_volume_enabled or
                settings["default_volume_level"] != self._default_volume_level or
                settings["default_volume_apps"] != self._default_volume_apps):
                self._default_volume_enabled = settings["default_volume_enabled"]
                self._default_volume_level = settings["default_volume_level"]
                self._default_volume_apps = settings["default_volume_apps"]
                self.data.setdefault("settings", {})["default_volume_enabled"] = self._default_volume_enabled
                self.data.setdefault("settings", {})["default_volume_level"] = self._default_volume_level
                self.data.setdefault("settings", {})["default_volume_apps"] = self._default_volume_apps
                self._dirty = True

            # Appliquer détection de jeux
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
        _title_keywords = {
            "service": ["service"],
            "target_apps": ["target", "cible"],
            "hotkey": ["hotkey", "raccourci", "keyboard"],
            "audio_params": ["audio", "paramètre"],
            "actions": ["action"],
            "auto_activation": ["auto-activation", "auto_activation"],
            "schedule": ["planification", "schedule"],
            "profiles": ["profil"],
            "statistics": ["statistique", "statistic"],
        }
        for group in self.findChildren(QGroupBox):
            title = group.title().lower()
            for key, keywords in _title_keywords.items():
                if any(kw in title for kw in keywords):
                    group.setTitle(tr(key))
                    break

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

        # État vide
        self.empty_title.setText(tr("services"))
        self.empty_desc.setText(
            "Create your first service\nto control volume" if _current_lang == "en"
            else "Créez votre premier service\npour contrôler le volume"
        )

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
            self.stop_all_act.setText(tr("tray_stop_all"))
            self.open_act.setText(tr("tray_open"))
            self.quit_act.setText(tr("tray_quit"))

        # Auto-activation
        if hasattr(self, 'auto_activation_chk'):
            self.auto_activation_chk.setText(tr("auto_activation_enabled"))
            self.auto_activation_chk.setToolTip(tr("auto_activation_desc"))
            self.trigger_filter_edit.setPlaceholderText(tr("auto_activation_filter"))
            self.trigger_refresh_btn.setText(tr("refresh"))

        # Champ de recherche
        if hasattr(self, 'search_services_edit'):
            self.search_services_edit.setPlaceholderText(tr("search_services"))

        # Rafraîchir la liste des services pour mettre à jour "Pas de raccourci"
        self._load_list()
        if self._selected_index >= 0:
            self.service_list.select(self._selected_index)

    # --- Drag & Drop ---
    def _on_service_order_changed(self, from_idx: int, to_idx: int):
        """Réorganise les services après un drag & drop"""
        if from_idx == to_idx:
            return

        # Arrêter les services actifs pour éviter les problèmes d'index
        active_services = set(self.controllers.keys())
        for idx in list(self.controllers.keys()):
            self.controllers[idx].stop()
        self.controllers.clear()

        # Réorganiser la liste
        service = self.services.pop(from_idx)
        self.services.insert(to_idx, service)

        # Recharger la liste
        self._load_list()
        self._dirty = True

        # Redémarrer les services qui étaient actifs (avec nouveaux index)
        for old_idx in active_services:
            if old_idx == from_idx:
                new_idx = to_idx
            elif old_idx > from_idx and old_idx <= to_idx:
                new_idx = old_idx - 1
            elif old_idx < from_idx and old_idx >= to_idx:
                new_idx = old_idx + 1
            else:
                new_idx = old_idx

            if new_idx < len(self.services):
                self._start_at_index(new_idx)

        # Sélectionner l'item déplacé
        self.service_list.select(to_idx)

    # --- Statistiques ---
    def _record_service_usage(self, idx: int):
        """Enregistre une utilisation du service"""
        if idx < 0 or idx >= len(self.services):
            return

        from datetime import datetime
        svc = self.services[idx]

        # Incrémenter le compteur
        svc["usage_count"] = svc.get("usage_count", 0) + 1

        # Enregistrer la dernière utilisation
        svc["last_used"] = datetime.now().isoformat()

        self._dirty = True

    # --- Recherche de services ---
    def _filter_services(self, text: str):
        """Filtre la liste des services selon le texte de recherche"""
        text = text.lower()
        self.service_list.clear()

        for idx, svc in enumerate(self.services):
            name = svc.get("name", "").lower()
            hotkey = svc.get("hotkey", "").lower()

            # Afficher si le texte est dans le nom ou le raccourci
            if not text or text in name or text in hotkey:
                is_active = idx in self.controllers
                self.service_list.add_item(idx, svc.get("name", "Service sans nom"),
                                          svc.get("hotkey", ""), is_active,
                                          svc.get("reduction", 75), svc.get("mode", "hold"))

    # --- Raccourcis clavier ---
    def _setup_shortcuts(self):
        """Configure les raccourcis clavier de l'application"""
        # Suppr pour supprimer le service sélectionné
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        delete_shortcut.activated.connect(self._on_delete_shortcut)

        # Entrée pour démarrer/arrêter le service sélectionné
        enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_shortcut.activated.connect(self._on_toggle_shortcut)

        # Espace aussi pour démarrer/arrêter
        space_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        space_shortcut.activated.connect(self._on_toggle_shortcut)

        # Ctrl+Enter pour démarrer/arrêter (fonctionne même si un champ texte a le focus)
        ctrl_enter_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        ctrl_enter_shortcut.activated.connect(self._toggle_selected_service)

    def _has_text_input_focus(self) -> bool:
        """Vérifie si un champ de saisie a le focus"""
        focused = QApplication.focusWidget()
        return isinstance(focused, (QLineEdit, QSpinBox, QComboBox))

    def _on_delete_shortcut(self):
        """Raccourci Suppr - ignore si un champ texte a le focus"""
        if not self._has_text_input_focus():
            self._delete_selected()

    def _on_toggle_shortcut(self):
        """Raccourci Entrée/Espace - ignore si un champ texte a le focus"""
        if not self._has_text_input_focus():
            self._toggle_selected_service()

    def _toggle_selected_service(self):
        """Démarre ou arrête le service sélectionné"""
        if self._selected_index >= 0:
            self._toggle_service(self._selected_index)

    def _on_auto_activation_toggled(self, state):
        """Affiche/cache la liste d'apps trigger quand le checkbox est coché/décoché"""
        self.trigger_apps_container.setVisible(state == Qt.Checked)
        if state == Qt.Checked and not self.trigger_checkboxes:
            self._refresh_trigger_apps()

    def _get_all_running_app_names(self) -> list:
        """Retourne la liste triée des noms de processus en cours"""
        import psutil
        names = set()
        for p in psutil.process_iter(['name']):
            try:
                name = p.info['name']
                if name:
                    names.add(name.lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        # Filtrer les processus système courants
        system_procs = {'system', 'system idle process', 'svchost.exe', 'csrss.exe',
                        'smss.exe', 'wininit.exe', 'services.exe', 'lsass.exe',
                        'winlogon.exe', 'dwm.exe', 'conhost.exe', 'registry',
                        'fontdrvhost.exe', 'dllhost.exe', 'sihost.exe',
                        'taskhostw.exe', 'ctfmon.exe', 'runtimebroker.exe'}
        return sorted(names - system_procs)

    def _build_trigger_apps_checkboxes(self, current_selections: Dict[str, bool] = None):
        """Construit la liste de checkboxes pour les applications déclencheurs"""
        if current_selections is None:
            current_selections = {}

        # Supprimer les anciennes checkboxes
        for cb in self.trigger_checkboxes.values():
            cb.deleteLater()
        self.trigger_checkboxes.clear()

        while self.trigger_layout.count():
            item = self.trigger_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        filter_text = self.trigger_filter_edit.text().lower() if hasattr(self, 'trigger_filter_edit') else ""
        apps = getattr(self, '_all_trigger_apps', None) or self._get_all_running_app_names()

        # Ajouter les apps manuelles trigger
        manual = getattr(self, '_manual_trigger_apps', set())
        for app in manual:
            if app not in apps:
                apps.append(app)

        # Ajouter les apps déjà sélectionnées (persistance)
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
            self.trigger_layout.addWidget(cb)
            self.trigger_checkboxes[name] = cb

        self.trigger_layout.addStretch()

    def _filter_trigger_apps(self, text: str):
        """Filtre la liste des apps trigger"""
        current = {name: cb.isChecked() for name, cb in self.trigger_checkboxes.items()}
        self._build_trigger_apps_checkboxes(current)

    def _add_manual_trigger_app(self):
        """Ajoute manuellement une app trigger"""
        app_name = self.trigger_add_edit.text().strip()
        if not app_name:
            return
        if not hasattr(self, '_manual_trigger_apps'):
            self._manual_trigger_apps = set()
        self._manual_trigger_apps.add(app_name)
        current = {name: cb.isChecked() for name, cb in self.trigger_checkboxes.items()}
        current[app_name] = True
        self._build_trigger_apps_checkboxes(current)
        self.trigger_add_edit.clear()

    def _refresh_trigger_apps(self):
        """Actualise la liste des apps trigger (tous les processus)"""
        self._all_trigger_apps = self._get_all_running_app_names()
        current = {name: cb.isChecked() for name, cb in self.trigger_checkboxes.items()}
        self._build_trigger_apps_checkboxes(current)

    # --- Mode avancé ---
    def _update_advanced_ui(self):
        """Met à jour l'interface selon le mode avancé"""
        # Afficher/cacher les groupes avancés
        if hasattr(self, 'grp_stats'):
            self.grp_stats.setVisible(self._advanced_mode)
        if hasattr(self, 'grp_profiles'):
            self.grp_profiles.setVisible(self._advanced_mode)
        if hasattr(self, 'grp_schedule'):
            self.grp_schedule.setVisible(self._advanced_mode)
        if hasattr(self, 'grp_auto_activation'):
            self.grp_auto_activation.setVisible(self._advanced_mode)

    # --- Profils ---
    def _get_profiles_dir(self):
        """Retourne le dossier des profils"""
        profiles_dir = os.path.join(os.path.dirname(resource_path(".")), "profiles")
        os.makedirs(profiles_dir, exist_ok=True)
        return profiles_dir

    def _save_profile(self):
        """Sauvegarde les services actuels dans un profil"""
        from PyQt5.QtWidgets import QInputDialog

        dialog = QInputDialog(self)
        dialog.setWindowTitle(tr("save_profile"))
        dialog.setLabelText(tr("profile_name") + ":")
        if is_dark_theme():
            dialog.setStyleSheet("""
                QInputDialog { background: #1e1e1e; }
                QLabel { color: #e0e0e0; }
                QLineEdit { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 6px; }
                QPushButton { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 6px 12px; }
                QPushButton:hover { background: #353535; }
            """)

        ok = dialog.exec_()
        name = dialog.textValue()
        if not ok or not name.strip():
            return

        name = name.strip()
        profiles_dir = self._get_profiles_dir()
        profile_path = os.path.join(profiles_dir, f"{name}.json")

        try:
            import json
            profile_data = {
                "name": name,
                "services": self.services
            }
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)

            self._toast(tr("profile_saved").format(name), "success")
        except Exception as e:
            QMessageBox.warning(self, tr("profiles"), f"Erreur: {e}")

    def _load_profile(self):
        """Charge un profil"""
        profiles_dir = self._get_profiles_dir()

        # Lister les profils existants
        profiles = [f[:-5] for f in os.listdir(profiles_dir) if f.endswith('.json')]

        if not profiles:
            QMessageBox.information(self, tr("profiles"),
                "Aucun profil" if _current_lang == "fr" else "No profiles")
            return

        from PyQt5.QtWidgets import QInputDialog
        dialog = QInputDialog(self)
        dialog.setWindowTitle(tr("load_profile"))
        dialog.setLabelText(tr("profile_name") + ":")
        dialog.setComboBoxItems(profiles)
        dialog.setComboBoxEditable(False)
        if is_dark_theme():
            dialog.setStyleSheet("""
                QInputDialog { background: #1e1e1e; }
                QLabel { color: #e0e0e0; }
                QComboBox { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 6px; }
                QComboBox QAbstractItemView { background: #2a2a2a; color: #e0e0e0; selection-background-color: #3d6a7a; }
                QPushButton { background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 6px 12px; }
                QPushButton:hover { background: #353535; }
            """)

        ok = dialog.exec_()
        name = dialog.textValue()
        if not ok:
            return

        profile_path = os.path.join(profiles_dir, f"{name}.json")

        try:
            import json
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)

            # Arrêter tous les services
            for idx in list(self.controllers.keys()):
                self.controllers[idx].stop()
            self.controllers.clear()

            # Charger les services
            self.services = profile_data.get("services", [])
            self._load_list()
            self._dirty = True

            self._toast(tr("profile_loaded").format(name), "success")
        except Exception as e:
            QMessageBox.warning(self, tr("profiles"), f"Erreur: {e}")

    def _apply_startup_with_windows(self):
        """Configure le démarrage automatique avec Windows"""
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "SoundLowerer"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

            if self._startup_with_windows:
                # Ajouter au démarrage
                if hasattr(sys, '_MEIPASS'):
                    # Mode exe
                    exe_path = sys.executable
                else:
                    # Mode développement
                    exe_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                # Supprimer du démarrage
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass

            winreg.CloseKey(key)
        except Exception as e:
            print(f"Erreur lors de la configuration du démarrage: {e}")

    def _setup_auto_backup(self):
        """Configure la sauvegarde automatique"""
        if hasattr(self, 'backup_timer'):
            self.backup_timer.stop()

        if self._auto_backup:
            self.backup_timer = QTimer(self)
            self.backup_timer.setInterval(self._backup_interval * 3600 * 1000)  # Heures en ms
            self.backup_timer.timeout.connect(self._do_backup)
            self.backup_timer.start()

    def _do_backup(self):
        """Effectue une sauvegarde de la configuration"""
        from datetime import datetime

        backup_dir = os.path.join(os.path.dirname(resource_path(".")), "backups")
        os.makedirs(backup_dir, exist_ok=True)

        # Nom du fichier de backup avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"config_backup_{timestamp}.json")

        try:
            # Sauvegarder la config actuelle
            import json
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

            # Garder seulement les 10 derniers backups
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith("config_backup_")])
            while len(backups) > 10:
                os.remove(os.path.join(backup_dir, backups.pop(0)))

        except Exception as e:
            print(f"Erreur lors du backup: {e}")

    # --- Volume par défaut ---
    def _apply_default_volume(self):
        """Applique le volume par défaut aux applications configurées"""
        if not self._default_volume_apps:
            return

        from audio_backend import set_volume_for_processes
        volume = self._default_volume_level / 100.0
        set_volume_for_processes(self._default_volume_apps, volume)
        self._toast(tr("default_vol_applied").format(len(self._default_volume_apps)), "info")

    # --- Auto-activation ---
    def _setup_auto_activation(self):
        """Configure le timer d'auto-activation si des services l'utilisent"""
        # Vérifier si au moins un service a l'auto-activation
        has_triggers = any(
            svc.get("auto_activation", False) and svc.get("trigger_apps", [])
            for svc in self.services
        )
        if has_triggers:
            self._auto_activation_timer = QTimer(self)
            self._auto_activation_timer.setInterval(5000)  # Vérifier toutes les 5 secondes
            self._auto_activation_timer.timeout.connect(self._check_trigger_apps)
            self._auto_activation_timer.start()
            self._previous_running_apps: set = set()

    def _get_running_processes(self) -> set:
        """Retourne l'ensemble des processus en cours d'exécution"""
        import psutil
        procs = set()
        for p in psutil.process_iter(['name']):
            try:
                name = p.info['name']
                if name:
                    procs.add(name.lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return procs

    def _check_trigger_apps(self):
        """Vérifie si les applications trigger sont en cours d'exécution"""
        current_apps = self._get_running_processes()

        for idx, svc in enumerate(self.services):
            if not svc.get("auto_activation", False):
                continue
            trigger_apps = svc.get("trigger_apps", [])
            if not trigger_apps:
                continue

            # Vérifier si au moins une trigger app est en cours
            any_running = any(app in current_apps for app in trigger_apps)

            if any_running and idx not in self.controllers:
                # Démarrer le service
                self._start_at_index(idx)
                self._auto_started.add(idx)
                # Trouver quelle app a déclenché
                detected = [app for app in trigger_apps if app in current_apps]
                self._toast(
                    tr("app_detected").format(detected[0]) + " - " +
                    tr("service_auto_started").format(svc.get("name", "")), "success")
            elif not any_running and idx in self._auto_started and idx in self.controllers:
                # Arrêter le service (seulement s'il a été auto-démarré)
                self._stop_at_index(idx)
                self._auto_started.discard(idx)
                self._toast(
                    tr("service_auto_stopped").format(svc.get("name", "")), "info")

    def _stop_auto_activation(self):
        """Arrête le timer d'auto-activation"""
        if hasattr(self, '_auto_activation_timer'):
            self._auto_activation_timer.stop()

    def _restart_auto_activation_if_needed(self):
        """Redémarre le timer d'auto-activation si nécessaire"""
        self._stop_auto_activation()
        self._setup_auto_activation()

    # --- Planification ---
    def _setup_schedule_check(self):
        """Configure la vérification périodique de la planification"""
        self.schedule_timer = QTimer(self)
        self.schedule_timer.setInterval(60000)  # Vérifier chaque minute
        self.schedule_timer.timeout.connect(self._check_schedules)
        self.schedule_timer.start()
        # Vérifier immédiatement au démarrage
        QTimer.singleShot(2000, self._check_schedules)

    def _check_schedules(self):
        """Vérifie si les services planifiés doivent être démarrés ou arrêtés"""
        if not self._advanced_mode:
            return

        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day_idx = now.weekday()  # 0 = Monday
        day_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        current_day = day_keys[current_day_idx]

        for idx, svc in enumerate(self.services):
            if not svc.get("schedule_enabled", False):
                continue

            schedule_days = svc.get("schedule_days", [])
            schedule_start = svc.get("schedule_start", "09:00")
            schedule_end = svc.get("schedule_end", "18:00")

            # Vérifier si c'est un jour actif
            if current_day not in schedule_days:
                # Arrêter le service seulement s'il a été démarré par le schedule
                if idx in self._auto_started and idx in self.controllers:
                    self._stop_at_index(idx)
                    self._auto_started.discard(idx)
                continue

            # Vérifier l'heure
            is_within_schedule = schedule_start <= current_time <= schedule_end

            if is_within_schedule:
                # Démarrer si pas déjà actif
                if idx not in self.controllers:
                    self._start_at_index(idx)
                    self._auto_started.add(idx)
                    self._toast(tr("schedule_active") + f" - {svc.get('name', '')}", "success")
            else:
                # Arrêter seulement si démarré par le schedule
                if idx in self._auto_started and idx in self.controllers:
                    self._stop_at_index(idx)
                    self._auto_started.discard(idx)
                    self._toast(tr("schedule_inactive") + f" - {svc.get('name', '')}", "info")
