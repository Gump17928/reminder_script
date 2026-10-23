"""Detect a locked Windows session (no admin needed)."""
import ctypes

_u = ctypes.windll.user32
_u.OpenInputDesktop.restype = ctypes.c_void_p
_u.SwitchDesktop.argtypes = _u.CloseDesktop.argtypes = [ctypes.c_void_p]


def locked():
    # While locked, the input desktop is the secure one and can't be opened/switched to.
    h = _u.OpenInputDesktop(0, False, 0x100)  # DESKTOP_SWITCHDESKTOP
    if not h:
        return True
    ok = _u.SwitchDesktop(h)
    _u.CloseDesktop(h)
    return not ok


if __name__ == "__main__":  # python -m rem.lock, then lock the PC to check detection
    import time
    for _ in range(30):
        print("locked" if locked() else "unlocked", flush=True)
        time.sleep(1)
