"""
Routeur de plateforme pour la gestion des hotkeys globaux.
Importe automatiquement le bon backend selon l'OS.
"""
import sys

if sys.platform == "win32":
    from hotkeys_windows import get_manager, parse_hotkey, HotkeyManager
else:
    from hotkeys_linux import get_manager, parse_hotkey, HotkeyManager

__all__ = ['get_manager', 'parse_hotkey', 'HotkeyManager']
