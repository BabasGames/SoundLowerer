import time
from typing import List, Dict
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from config import get_logger

# Cache pour unique_apps avec TTL
_apps_cache = {"data": [], "timestamp": 0}
CACHE_TTL = 3.0  # secondes

def list_sessions() -> List[Dict]:
    sessions = AudioUtilities.GetAllSessions()
    out = []
    for s in sessions:
        try:
            proc = s.Process.name().lower() if s.Process else None
        except Exception:
            proc = None
        out.append({
            "process": proc,
            "session": s
        })
    return out

def unique_apps(force_refresh: bool = False) -> List[str]:
    """Retourne la liste des applications audio uniques, avec cache TTL"""
    global _apps_cache
    now = time.time()
    if not force_refresh and (now - _apps_cache["timestamp"]) < CACHE_TTL and _apps_cache["data"]:
        return _apps_cache["data"]

    names = set()
    for s in list_sessions():
        if s["process"]:
            names.add(s["process"])
    result = sorted(names)
    _apps_cache = {"data": result, "timestamp": now}
    return result

def set_volume_for_processes(process_names: List[str], volume: float):
    volume = max(0.0, min(1.0, volume))
    for s in list_sessions():
        if s["process"] and s["process"] in process_names:
            try:
                vol = s["session"]._ctl.QueryInterface(ISimpleAudioVolume)
                vol.SetMasterVolume(volume, None)
            except Exception as e:
                get_logger().warning(f"Erreur volume pour {s['process']}: {e}")

def get_current_volumes(process_names: List[str]) -> Dict[str, float]:
    res = {}
    for s in list_sessions():
        if s["process"] and s["process"] in process_names:
            try:
                vol = s["session"]._ctl.QueryInterface(ISimpleAudioVolume)
                res[s["process"]] = vol.GetMasterVolume()
            except Exception:
                pass
    return res
