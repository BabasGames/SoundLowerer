"""
Module de gestion des hotkeys globaux sur Linux via la bibliothèque keyboard.
Nécessite les droits root ou l'appartenance au groupe 'input'.
"""
import threading
import time
from typing import Callable, Dict, Optional
import re

try:
    import keyboard
except ImportError:
    keyboard = None

from config import get_logger


# Mapping des modificateurs (compatibilité avec le format win_hotkeys)
MODIFIER_NAMES = {'ctrl', 'control', 'alt', 'shift', 'win', 'windows', 'super', 'menu'}


def parse_hotkey(hotkey_str: str) -> tuple:
    """
    Parse une chaîne de hotkey (ex: "ctrl+alt+f1").
    Retourne (modifiers_set, key_name) pour compatibilité avec l'interface Windows.
    Sur Linux, modifiers est un frozenset de noms et key_name est une string.
    """
    parts = re.split(r'[+]', hotkey_str.lower().strip())
    modifiers = set()
    key_name = ""

    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part in MODIFIER_NAMES:
            # Normaliser
            if part in ('control',):
                part = 'ctrl'
            if part in ('windows', 'super'):
                part = 'win'
            if part == 'menu':
                part = 'alt'
            modifiers.add(part)
        else:
            key_name = part

    return frozenset(modifiers), key_name


class HotkeyManager:
    """
    Gestionnaire de hotkeys globaux utilisant la bibliothèque keyboard sur Linux.
    Simule MOD_NOREPEAT de Windows en ignorant les répétitions de touches.
    """

    def __init__(self):
        self._hotkeys: Dict[int, dict] = {}
        self._next_id = 1
        self._running = False

    def _make_callback(self, hotkey_id: int, on_press: Callable):
        """Crée un callback qui ne tire qu'une fois par appui (simule MOD_NOREPEAT)."""
        def norepeat_callback():
            hk_data = self._hotkeys.get(hotkey_id)
            if not hk_data or hk_data.get('fired'):
                return
            hk_data['fired'] = True

            # Thread qui attend le relâchement pour réinitialiser le flag
            def wait_for_release():
                key = hk_data['key_name']
                time.sleep(0.1)
                try:
                    while keyboard and keyboard.is_pressed(key):
                        time.sleep(0.02)
                except Exception:
                    pass
                hk_data['fired'] = False
            threading.Thread(target=wait_for_release, daemon=True).start()

            if on_press:
                threading.Thread(target=on_press, daemon=True).start()
        return norepeat_callback

    def register(self, hotkey_str: str, on_press: Callable = None) -> int:
        """
        Enregistre un hotkey global.
        Retourne l'ID du hotkey ou 0 si échec.
        """
        if keyboard is None:
            get_logger().error("La bibliothèque 'keyboard' n'est pas installée")
            return 0

        modifiers, key_name = parse_hotkey(hotkey_str)
        if not key_name:
            get_logger().error(f"Hotkey invalide: {hotkey_str}")
            return 0

        hotkey_id = self._next_id
        self._next_id += 1

        # Pré-créer l'entrée pour que le callback puisse y accéder
        self._hotkeys[hotkey_id] = {
            'hotkey': hotkey_str,
            'kb_hotkey_str': '',
            'hook': None,
            'on_press': on_press,
            'modifiers': modifiers,
            'key_name': key_name,
            'fired': False,
        }

        try:
            # Construire la chaîne hotkey pour la lib keyboard
            parts = sorted(modifiers) + [key_name]
            kb_hotkey_str = '+'.join(parts)

            callback = self._make_callback(hotkey_id, on_press)
            hook = keyboard.add_hotkey(
                kb_hotkey_str,
                callback,
                suppress=False
            )

            self._hotkeys[hotkey_id]['kb_hotkey_str'] = kb_hotkey_str
            self._hotkeys[hotkey_id]['hook'] = hook

            get_logger().info(f"[HotkeyManager Linux] Hotkey enregistré: {hotkey_str} (id={hotkey_id})")
            return hotkey_id

        except Exception as e:
            self._hotkeys.pop(hotkey_id, None)
            get_logger().error(f"[HotkeyManager Linux] Échec enregistrement {hotkey_str}: {e}")
            return 0

    def unregister(self, hotkey_id: int):
        """Désenregistre un hotkey."""
        if hotkey_id not in self._hotkeys:
            return

        hk_data = self._hotkeys.pop(hotkey_id, None)
        if hk_data and hk_data.get('hook') is not None and keyboard is not None:
            try:
                keyboard.remove_hotkey(hk_data['hook'])
                get_logger().info(f"[HotkeyManager Linux] Hotkey désenregistré: {hk_data['hotkey']}")
            except Exception as e:
                get_logger().warning(f"[HotkeyManager Linux] Erreur désenregistrement: {e}")

    def start(self):
        """Démarre le gestionnaire (no-op sur Linux, keyboard gère son propre thread)."""
        self._running = True
        get_logger().info("[HotkeyManager Linux] Démarré")

    def stop(self):
        """Arrête le gestionnaire et désenregistre tous les hotkeys."""
        self._running = False
        for hk_id in list(self._hotkeys.keys()):
            self.unregister(hk_id)
        get_logger().info("[HotkeyManager Linux] Arrêté")


# Instance globale
_manager: Optional[HotkeyManager] = None


def get_manager() -> HotkeyManager:
    """Retourne l'instance globale du gestionnaire de hotkeys."""
    global _manager
    if _manager is None:
        _manager = HotkeyManager()
        _manager.start()
    return _manager
