"""
Routeur de plateforme pour le backend audio.
Importe automatiquement le bon backend selon l'OS.
"""
import sys

if sys.platform == "win32":
    from audio_backend_windows import list_sessions, unique_apps, set_volume_for_processes, get_current_volumes
else:
    from audio_backend_linux import list_sessions, unique_apps, set_volume_for_processes, get_current_volumes

__all__ = ['list_sessions', 'unique_apps', 'set_volume_for_processes', 'get_current_volumes']
