"""
Module de gestion des hotkeys via l'API Windows RegisterHotKey.
Fonctionne même dans les jeux en plein écran.
"""
import ctypes
from ctypes import wintypes
import threading
import queue
from typing import Callable, Dict, Optional
import re

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Modificateurs
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
MOD_NOREPEAT = 0x4000

# Message Windows pour les hotkeys
WM_HOTKEY = 0x0312
WM_USER_REGISTER = 0x0400 + 1
WM_USER_UNREGISTER = 0x0400 + 2

# Mapping des noms de touches vers les virtual key codes
VK_CODES = {
    # Lettres
    **{chr(i): i for i in range(ord('A'), ord('Z') + 1)},
    **{chr(i).lower(): i for i in range(ord('A'), ord('Z') + 1)},
    # Chiffres
    **{str(i): 0x30 + i for i in range(10)},
    # Touches de fonction
    **{f'f{i}': 0x70 + i - 1 for i in range(1, 25)},
    # Touches spéciales
    'space': 0x20, 'spacebar': 0x20, ' ': 0x20,
    'enter': 0x0D, 'return': 0x0D,
    'tab': 0x09,
    'escape': 0x1B, 'esc': 0x1B,
    'backspace': 0x08, 'back': 0x08,
    'delete': 0x2E, 'del': 0x2E,
    'insert': 0x2D, 'ins': 0x2D,
    'home': 0x24,
    'end': 0x23,
    'pageup': 0x21, 'page up': 0x21,
    'pagedown': 0x22, 'page down': 0x22,
    'up': 0x26,
    'down': 0x28,
    'left': 0x25,
    'right': 0x27,
    'capslock': 0x14, 'caps lock': 0x14,
    'numlock': 0x90, 'num lock': 0x90,
    'scrolllock': 0x91, 'scroll lock': 0x91,
    'printscreen': 0x2C, 'print screen': 0x2C,
    'pause': 0x13,
    # Pavé numérique
    'num0': 0x60, 'numpad0': 0x60,
    'num1': 0x61, 'numpad1': 0x61,
    'num2': 0x62, 'numpad2': 0x62,
    'num3': 0x63, 'numpad3': 0x63,
    'num4': 0x64, 'numpad4': 0x64,
    'num5': 0x65, 'numpad5': 0x65,
    'num6': 0x66, 'numpad6': 0x66,
    'num7': 0x67, 'numpad7': 0x67,
    'num8': 0x68, 'numpad8': 0x68,
    'num9': 0x69, 'numpad9': 0x69,
    'multiply': 0x6A, '*': 0x6A,
    'add': 0x6B, 'plus': 0x6B,
    'subtract': 0x6D, 'minus': 0x6D,
    'decimal': 0x6E,
    'divide': 0x6F,
    # Autres
    ';': 0xBA, ':': 0xBA, '$': 0xBA,  # $ sur clavier français
    '/': 0xBF, '?': 0xBF,
    '`': 0xC0, '~': 0xC0,
    '[': 0xDB, '{': 0xDB,
    '\\': 0xDC, '|': 0xDC,
    ']': 0xDD, '}': 0xDD,
    "'": 0xDE, '"': 0xDE,
    ',': 0xBC, '<': 0xBC,
    '.': 0xBE, '>': 0xBE,
    '-': 0xBD, '_': 0xBD,
    '=': 0xBB, '+': 0xBB,
}

# Mapping des modificateurs
MODIFIER_KEYS = {
    'ctrl': MOD_CONTROL, 'control': MOD_CONTROL,
    'alt': MOD_ALT, 'menu': MOD_ALT,
    'shift': MOD_SHIFT,
    'win': MOD_WIN, 'windows': MOD_WIN, 'super': MOD_WIN,
}


# Caractères qui nécessitent Shift - mappés vers leur touche de base (claviers US)
SHIFT_CHARS = {
    '!': '1', '@': '2', '#': '3', '%': '5', '^': '6', '&': '7', '*': '8',
    '(': '9', ')': '0', '_': '-', '{': '[', '}': ']', '|': '\\',
    '"': "'", '<': ',', '>': '.', '?': '/', '~': '`',
}


def parse_hotkey(hotkey_str: str) -> tuple:
    """
    Parse une chaîne de hotkey (ex: "ctrl+alt+f1") et retourne (modifiers, vk_code).
    """
    parts = re.split(r'[+\s]+', hotkey_str.lower().strip())
    modifiers = 0
    vk_code = 0

    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part in MODIFIER_KEYS:
            modifiers |= MODIFIER_KEYS[part]
        elif part in VK_CODES:
            vk_code = VK_CODES[part]
        elif part in SHIFT_CHARS:
            # Caractère avec Shift implicite
            base_key = SHIFT_CHARS[part]
            if base_key in VK_CODES:
                vk_code = VK_CODES[base_key]
                modifiers |= MOD_SHIFT

    return modifiers, vk_code


class HotkeyManager:
    """
    Gestionnaire de hotkeys globaux utilisant l'API Windows RegisterHotKey.
    """

    def __init__(self):
        self._hotkeys: Dict[int, dict] = {}
        self._next_id = 1
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._thread_id = 0
        self._ready = threading.Event()
        self._pending_registrations = queue.Queue()

    def register(self, hotkey_str: str, on_press: Callable = None) -> int:
        """
        Enregistre un hotkey global.
        Retourne l'ID du hotkey ou 0 si échec.
        """
        modifiers, vk_code = parse_hotkey(hotkey_str)
        if vk_code == 0:
            print(f"[HotkeyManager] Hotkey invalide: {hotkey_str}")
            return 0

        hotkey_id = self._next_id
        self._next_id += 1

        self._hotkeys[hotkey_id] = {
            'hotkey': hotkey_str,
            'modifiers': modifiers,
            'vk_code': vk_code,
            'on_press': on_press,
            'registered': False
        }

        # Si le thread tourne, envoyer un message pour enregistrer
        if self._running and self._thread_id:
            self._pending_registrations.put(('register', hotkey_id))
            user32.PostThreadMessageW(self._thread_id, WM_USER_REGISTER, hotkey_id, 0)

        return hotkey_id

    def unregister(self, hotkey_id: int):
        """Désenregistre un hotkey."""
        if hotkey_id not in self._hotkeys:
            return

        hk_data = self._hotkeys.pop(hotkey_id, None)
        if hk_data and hk_data.get('registered'):
            if self._running and self._thread_id:
                # Envoyer un message pour désenregistrer dans le bon thread
                user32.PostThreadMessageW(self._thread_id, WM_USER_UNREGISTER, hotkey_id, 0)
            else:
                try:
                    user32.UnregisterHotKey(None, hotkey_id)
                except:
                    pass

    def start(self):
        """Démarre le thread de gestion des hotkeys."""
        if self._running:
            return
        self._running = True
        self._ready.clear()
        self._thread = threading.Thread(target=self._message_loop, daemon=True)
        self._thread.start()
        # Attendre que le thread soit prêt
        self._ready.wait(timeout=2.0)

    def stop(self):
        """Arrête le gestionnaire de hotkeys."""
        self._running = False
        if self._thread_id:
            user32.PostThreadMessageW(self._thread_id, 0x0012, 0, 0)  # WM_QUIT
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        # Désenregistrer tous les hotkeys
        for hk_id, hk_data in list(self._hotkeys.items()):
            if hk_data.get('registered'):
                try:
                    user32.UnregisterHotKey(None, hk_id)
                except:
                    pass

    def _do_register(self, hotkey_id: int):
        """Enregistre un hotkey (doit être appelé depuis le thread message loop)."""
        if hotkey_id not in self._hotkeys:
            return False
        hk_data = self._hotkeys[hotkey_id]
        if hk_data['registered']:
            return True

        success = user32.RegisterHotKey(
            None, hotkey_id,
            hk_data['modifiers'] | MOD_NOREPEAT,
            hk_data['vk_code']
        )
        hk_data['registered'] = bool(success)
        if success:
            print(f"[HotkeyManager] Hotkey enregistré: {hk_data['hotkey']} (id={hotkey_id})")
        else:
            error = kernel32.GetLastError()
            print(f"[HotkeyManager] Échec enregistrement {hk_data['hotkey']}: erreur {error}")
        return bool(success)

    def _message_loop(self):
        """Boucle de messages Windows pour recevoir les événements hotkey."""
        self._thread_id = kernel32.GetCurrentThreadId()

        # Créer une file de messages pour ce thread
        user32.PeekMessageW(ctypes.byref(wintypes.MSG()), None, 0, 0, 0)

        # Enregistrer tous les hotkeys en attente
        for hk_id in list(self._hotkeys.keys()):
            self._do_register(hk_id)

        # Signaler que le thread est prêt
        self._ready.set()

        msg = wintypes.MSG()
        while self._running:
            result = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if result <= 0:
                break

            if msg.message == WM_HOTKEY:
                hotkey_id = msg.wParam
                print(f"[HotkeyManager] WM_HOTKEY reçu! id={hotkey_id}")
                if hotkey_id in self._hotkeys:
                    hk_data = self._hotkeys[hotkey_id]
                    print(f"[HotkeyManager] Callback trouvé pour {hk_data['hotkey']}")
                    if hk_data.get('on_press'):
                        try:
                            # Exécuter le callback dans un thread séparé pour ne pas bloquer
                            threading.Thread(target=hk_data['on_press'], daemon=True).start()
                        except Exception as e:
                            print(f"[HotkeyManager] Erreur callback: {e}")
                else:
                    print(f"[HotkeyManager] Hotkey id={hotkey_id} non trouvé dans {list(self._hotkeys.keys())}")

            elif msg.message == WM_USER_REGISTER:
                hotkey_id = msg.wParam
                self._do_register(hotkey_id)

            elif msg.message == WM_USER_UNREGISTER:
                hotkey_id = msg.wParam
                # Le hotkey a déjà été retiré du dict, juste désenregistrer Windows
                try:
                    user32.UnregisterHotKey(None, hotkey_id)
                except:
                    pass

        self._thread_id = 0


# Instance globale
_manager: Optional[HotkeyManager] = None


def get_manager() -> HotkeyManager:
    """Retourne l'instance globale du gestionnaire de hotkeys."""
    global _manager
    if _manager is None:
        _manager = HotkeyManager()
        _manager.start()
    return _manager
