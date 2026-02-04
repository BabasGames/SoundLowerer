import keyboard
from typing import Optional, Set
import time

def record_hotkey_once(prompt="Press your shortcut (finish by releasing)...") -> Optional[str]:
    """
    Capture les touches pressées et retourne une chaîne de hotkey normalisée.
    """
    try:
        pressed_keys: Set[str] = set()
        recording = True
        last_event_time = time.time()

        def on_key(event):
            nonlocal pressed_keys, recording, last_event_time
            if not recording:
                return

            key_name = event.name.lower() if event.name else ""
            if not key_name:
                return

            last_event_time = time.time()

            if event.event_type == 'down':
                pressed_keys.add(key_name)

        # Installer le hook
        keyboard.hook(on_key)

        # Attendre que l'utilisateur appuie sur des touches puis relâche
        time.sleep(0.1)  # Petit délai initial

        start = time.time()
        while recording and (time.time() - start) < 10:
            time.sleep(0.05)
            # Si des touches ont été pressées et qu'il n'y a pas eu d'activité depuis 0.3s
            if pressed_keys and (time.time() - last_event_time) > 0.3:
                recording = False

        # Retirer le hook
        keyboard.unhook(on_key)

        if not pressed_keys:
            return None

        # Trier les touches : modificateurs d'abord, puis la touche principale
        modifiers_set = {'ctrl', 'control', 'alt', 'shift', 'win', 'windows',
                         'cmd', 'command', 'left ctrl', 'right ctrl',
                         'left alt', 'right alt', 'left shift', 'right shift',
                         'left windows', 'right windows'}

        mod_keys = []
        other_keys = []

        for k in pressed_keys:
            if k in modifiers_set or 'ctrl' in k or 'alt' in k or 'shift' in k or 'windows' in k:
                mod_keys.append(k)
            else:
                other_keys.append(k)

        # Normaliser les modificateurs
        normalized_mods = []
        has_ctrl = any('ctrl' in m or 'control' in m for m in mod_keys)
        has_alt = any('alt' in m for m in mod_keys)
        has_shift = any('shift' in m for m in mod_keys)
        has_win = any('windows' in m or 'win' in m for m in mod_keys)

        if has_ctrl:
            normalized_mods.append('ctrl')
        if has_alt:
            normalized_mods.append('alt')
        if has_shift:
            normalized_mods.append('shift')
        if has_win:
            normalized_mods.append('win')

        # Construire le hotkey
        all_keys = normalized_mods + other_keys
        result = '+'.join(all_keys) if all_keys else None

        print(f"[Hotkey] Enregistré: {result} (touches brutes: {pressed_keys})")
        return result

    except KeyboardInterrupt:
        return None
    except Exception as e:
        print(f"Erreur enregistrement hotkey: {e}")
        return None


def validate_hotkey(hotkey: str) -> bool:
    """Vérifie si un hotkey est valide pour notre système"""
    if not hotkey or not hotkey.strip():
        return False

    try:
        from win_hotkeys import parse_hotkey
        modifiers, vk_code = parse_hotkey(hotkey)
        return vk_code != 0
    except Exception:
        return False
