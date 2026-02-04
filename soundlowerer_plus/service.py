import threading, time, math, ctypes
from typing import List, Dict, Optional
from audio_backend import get_current_volumes, set_volume_for_processes
from config import get_logger
from win_hotkeys import get_manager, parse_hotkey

# API Windows pour détecter l'état des touches
user32 = ctypes.windll.user32

def is_key_pressed(vk_code: int) -> bool:
    """Vérifie si une touche est actuellement pressée via GetAsyncKeyState."""
    return (user32.GetAsyncKeyState(vk_code) & 0x8000) != 0

def are_modifiers_pressed(modifiers: int) -> bool:
    """Vérifie si les modificateurs sont pressés."""
    from win_hotkeys import MOD_CONTROL, MOD_ALT, MOD_SHIFT, MOD_WIN
    VK_CONTROL = 0x11
    VK_MENU = 0x12  # Alt
    VK_SHIFT = 0x10
    VK_LWIN = 0x5B
    VK_RWIN = 0x5C

    if modifiers & MOD_CONTROL and not is_key_pressed(VK_CONTROL):
        return False
    if modifiers & MOD_ALT and not is_key_pressed(VK_MENU):
        return False
    if modifiers & MOD_SHIFT and not is_key_pressed(VK_SHIFT):
        return False
    if modifiers & MOD_WIN and not (is_key_pressed(VK_LWIN) or is_key_pressed(VK_RWIN)):
        return False
    return True


class VolumeServiceController:
    def __init__(self, name: str, targets: List[str], hotkey: str, reduction_pct: int,
                 mode: str = "hold", fade_ms: int = 300, curve: str = "linear",
                 all_except: bool = False, on_use_callback=None):
        self.name = name or (targets[0] if targets else "Service")
        self.targets = targets[:]  # list of process names
        self.hotkey = hotkey
        self.reduction_pct = max(0, min(100, reduction_pct))
        self.mode = mode  # "hold" or "toggle"
        self.fade_ms = max(0, fade_ms)
        self.curve = curve  # "linear" or "expo"
        self.all_except = all_except
        self.on_use_callback = on_use_callback  # Callback appelé à chaque utilisation
        self._running = False
        self._active = False
        self._hotkey_id: int = 0
        self._hold_thread: Optional[threading.Thread] = None
        self._original: Dict[str, float] = {}
        self._modifiers = 0
        self._vk_code = 0

    def start(self):
        if self._running:
            return
        self._running = True

        # Parser le hotkey pour obtenir les codes
        self._modifiers, self._vk_code = parse_hotkey(self.hotkey)
        get_logger().info(f"Service '{self.name}': parsing hotkey '{self.hotkey}' -> modifiers={self._modifiers}, vk={self._vk_code}")

        if self._vk_code == 0:
            get_logger().error(f"Service '{self.name}': hotkey invalide '{self.hotkey}'")
            return

        # Enregistrer le hotkey global
        manager = get_manager()
        self._hotkey_id = manager.register(
            self.hotkey,
            on_press=self._on_hotkey_press
        )
        get_logger().info(f"Service '{self.name}': register() returned id={self._hotkey_id}")

        if self._hotkey_id == 0:
            get_logger().error(f"Service '{self.name}': impossible d'enregistrer le hotkey")
            return

        get_logger().info(f"Service '{self.name}' démarré (hotkey: {self.hotkey})")

    def stop(self):
        self._running = False

        # Désenregistrer le hotkey
        if self._hotkey_id:
            get_manager().unregister(self._hotkey_id)
            self._hotkey_id = 0

        # Attendre la fin du thread hold si actif
        if self._hold_thread and self._hold_thread.is_alive():
            self._hold_thread.join(timeout=1.0)

        # Restaurer les volumes si le service était actif
        if self._active:
            self._restore()
        get_logger().info(f"Service '{self.name}' arrêté")

    def is_active(self) -> bool:
        return self._active

    def _on_hotkey_press(self):
        """Callback appelé quand le hotkey est pressé."""
        get_logger().info(f"Service '{self.name}': HOTKEY PRESSÉ!")

        if not self._running:
            return

        # Appeler le callback de statistiques si défini
        if self.on_use_callback:
            try:
                self.on_use_callback()
            except Exception as e:
                get_logger().error(f"Erreur dans on_use_callback: {e}")

        if self.mode == "toggle":
            # Mode toggle: alterner entre activé et désactivé
            if self._active:
                self._restore()
            else:
                self._apply_reduction()
        else:
            # Mode hold: activer et surveiller le relâchement
            if not self._active:
                self._apply_reduction()
                # Démarrer un thread pour surveiller le relâchement
                self._hold_thread = threading.Thread(target=self._hold_loop, daemon=True)
                self._hold_thread.start()

    def _hold_loop(self):
        """Boucle qui attend le relâchement de la touche en mode hold."""
        # Attendre un peu pour éviter la détection immédiate
        time.sleep(0.1)

        while self._running and self._active:
            # Vérifier si la touche principale est toujours pressée
            if not is_key_pressed(self._vk_code):
                # La touche a été relâchée
                self._restore()
                break
            time.sleep(0.02)

    def _calc_targets(self) -> List[str]:
        if not self.all_except:
            return self.targets[:]
        from audio_backend import unique_apps
        all_apps = unique_apps()
        return [a for a in all_apps if a not in set(self.targets)]

    def _apply_reduction(self):
        targets = self._calc_targets()
        if not targets:
            return
        self._original = get_current_volumes(targets)
        if not self._original:
            return
        target_level = max(0.0, min(1.0, 1.0 - self.reduction_pct / 100.0))
        steps = max(1, math.ceil(self.fade_ms / 15))
        for i in range(steps):
            if not self._running:
                break
            t = (i + 1) / steps
            if self.curve == "expo":
                t = t * t
            for proc, start in self._original.items():
                level = start + (target_level - start) * t
                set_volume_for_processes([proc], level)
            time.sleep(self.fade_ms / steps / 1000.0)
        self._active = True

    def _restore(self):
        if not self._original:
            self._active = False
            return
        steps = max(1, math.ceil(self.fade_ms / 15))
        for i in range(steps):
            t = (i + 1) / steps
            if self.curve == "expo":
                t = t * t
            for proc, start in self._original.items():
                level = (1 - t) * (1.0 - self.reduction_pct / 100.0) + t * start
                set_volume_for_processes([proc], level)
            time.sleep(self.fade_ms / steps / 1000.0)
        for proc, start in self._original.items():
            set_volume_for_processes([proc], start)
        self._original = {}
        self._active = False
