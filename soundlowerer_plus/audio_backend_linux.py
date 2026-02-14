import os
import time
from typing import List, Dict
from config import get_logger

try:
    import pulsectl
except ImportError:
    pulsectl = None
    get_logger().error("pulsectl non installé. Installer avec: pip install pulsectl")

# Cache pour unique_apps avec TTL
_apps_cache = {"data": [], "timestamp": 0}
CACHE_TTL = 3.0  # secondes


def _detect_pulse_server():
    """Détecte le serveur PulseAudio, y compris quand lancé via sudo."""
    # Si PULSE_SERVER est déjà défini, l'utiliser
    if os.environ.get('PULSE_SERVER'):
        return os.environ['PULSE_SERVER']

    # Si lancé via sudo, on tourne en root mais PulseAudio tourne en user
    sudo_uid = os.environ.get('SUDO_UID')
    if sudo_uid and os.getuid() == 0:
        # Essayer le socket PulseAudio de l'utilisateur original
        pulse_socket = f"/run/user/{sudo_uid}/pulse/native"
        if os.path.exists(pulse_socket):
            server = f"unix:{pulse_socket}"
            get_logger().info(f"Sudo détecté: connexion PulseAudio via {server}")
            return server

        # Essayer le socket PipeWire-Pulse
        pipewire_socket = f"/run/user/{sudo_uid}/pipewire-0"
        if os.path.exists(pipewire_socket):
            server = f"unix:{pipewire_socket}"
            get_logger().info(f"Sudo détecté: connexion PipeWire via {server}")
            return server

    return None


_pulse_server = _detect_pulse_server()


def _get_pulse():
    """Crée une connexion PulseAudio/PipeWire."""
    if pulsectl is None:
        return None
    try:
        return pulsectl.Pulse('soundlowerer-plus', server=_pulse_server)
    except Exception as e:
        get_logger().warning(f"Impossible de se connecter à PulseAudio/PipeWire: {e}")
        return None


def _get_app_name(sink_input) -> str:
    """Extrait le nom de processus d'un sink_input PulseAudio."""
    # Priorité: application.process.binary > application.name
    props = sink_input.proplist
    name = props.get('application.process.binary', '') or props.get('application.name', '') or sink_input.name or ''
    return name.lower()


def list_sessions() -> List[Dict]:
    pulse = _get_pulse()
    if pulse is None:
        return []
    try:
        with pulse:
            out = []
            for si in pulse.sink_input_list():
                proc = _get_app_name(si)
                out.append({
                    "process": proc if proc else None,
                    "sink_input_index": si.index,
                    "volume": si.volume,
                })
            return out
    except Exception as e:
        get_logger().warning(f"Erreur list_sessions: {e}")
        return []


def unique_apps(force_refresh: bool = False) -> List[str]:
    """Retourne la liste des applications audio uniques, avec cache TTL"""
    global _apps_cache
    now = time.time()
    if not force_refresh and (now - _apps_cache["timestamp"]) < CACHE_TTL and _apps_cache["data"]:
        return _apps_cache["data"]

    names = set()
    pulse = _get_pulse()
    if pulse is not None:
        try:
            with pulse:
                for si in pulse.sink_input_list():
                    name = _get_app_name(si)
                    if name:
                        names.add(name)
        except Exception as e:
            get_logger().warning(f"Erreur unique_apps: {e}")

    result = sorted(names)
    _apps_cache = {"data": result, "timestamp": now}
    return result


def set_volume_for_processes(process_names: List[str], volume: float):
    volume = max(0.0, min(1.0, volume))
    pulse = _get_pulse()
    if pulse is None:
        return
    try:
        with pulse:
            for si in pulse.sink_input_list():
                name = _get_app_name(si)
                if name and name in process_names:
                    try:
                        pulse.volume_set_all_chans(si, volume)
                    except Exception as e:
                        get_logger().warning(f"Erreur volume pour {name}: {e}")
    except Exception as e:
        get_logger().warning(f"Erreur set_volume_for_processes: {e}")


def get_current_volumes(process_names: List[str]) -> Dict[str, float]:
    res = {}
    pulse = _get_pulse()
    if pulse is None:
        return res
    try:
        with pulse:
            for si in pulse.sink_input_list():
                name = _get_app_name(si)
                if name and name in process_names:
                    try:
                        # Prendre la moyenne des canaux
                        values = si.volume.values
                        res[name] = sum(values) / len(values) if values else 1.0
                    except Exception:
                        pass
    except Exception as e:
        get_logger().warning(f"Erreur get_current_volumes: {e}")
    return res
