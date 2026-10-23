"""Sound: three built-in synthesized presets, plus audio files dropped into sounds/."""
import ctypes
import io
import itertools
import math
import os
import struct
import subprocess
import threading
import time
import wave
import winsound
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "sounds"
EXTS = {".wav", ".mp3", ".mp4", ".m4a", ".wma", ".aac"}
RATE, MAX_FILE_SECONDS = 22050, 12
# name: (notes as (Hz, start second), length s, fade-in s, decay rate, overtone level)
PRESETS = {
    "Soft Bell": ([(523.25, 0), (659.25, .35), (783.99, .7)], 3.0, .08, 2.2, .25),
    "Marimba": ([(392.0, 0), (493.88, .25), (587.33, .5), (783.99, .75)], 2.5, .01, 4.5, .5),
    "Rising Tone": ([(392.0, 0), (523.25, .6), (659.25, 1.2)], 4.0, .35, 1.3, .1),
}
DEFAULT = "Soft Bell"
_cache, _ids = {}, itertools.count()


def names():
    files = sorted(p.name for p in DIR.glob("*") if p.suffix.lower() in EXTS) if DIR.is_dir() else []
    return list(PRESETS) + files


def synth(name, volume):
    """Sine notes with a smooth fade-in and exponential fade-out, as 16-bit mono WAV bytes."""
    notes, length, attack, decay, over = PRESETS[name]
    n = int(RATE * length)
    buf = [0.0] * n
    for freq, start in notes:
        for i in range(int(start * RATE), n):
            t = i / RATE - start
            env = math.sin(min(t / attack, 1) * math.pi / 2) ** 2 * math.exp(-decay * t)
            buf[i] += env * (math.sin(2 * math.pi * freq * t) + over * math.sin(4 * math.pi * freq * t))
    peak = max(map(abs, buf)) or 1
    fade = int(RATE * 0.2)  # guarantee silence at the very end
    pcm = b"".join(struct.pack("<h", int(32767 * volume * s / peak * min(1, (n - i) / fade)))
                   for i, s in enumerate(buf))
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm)
    return out.getvalue()


def _mci(cmd):
    buf = ctypes.create_unicode_buffer(255)
    return ctypes.windll.winmm.mciSendStringW(cmd, buf, 255, 0), buf.value


def _mci_play(path, volume):
    """Play via MCI (wav/mp3/wma...) with a fade in/out. False if it can't play."""
    a = f"rem{next(_ids)}"
    if _mci(f'open "{path}" type mpegvideo alias {a}')[0]:
        return False
    try:
        ms = min(int(_mci(f"status {a} length")[1] or 0), MAX_FILE_SECONDS * 1000)
        if ms <= 0 or _mci(f"play {a}")[0]:
            return False
        t0 = time.time()
        while (pos := (time.time() - t0) * 1000) < ms:
            env = min(1, pos / 600, (ms - pos) / 1000)
            _mci(f"setaudio {a} volume to {int(1000 * volume * env)}")
            time.sleep(.05)
        return True
    finally:
        _mci(f"close {a}")


# Windows' WPF MediaPlayer (via PowerShell) handles containers MCI can't, such as mp4/m4a.
_WPF = r"""
Add-Type -AssemblyName PresentationCore
$p = New-Object System.Windows.Media.MediaPlayer
$p.Open([uri]$env:REM_FILE); $p.Volume = 0
for ($i = 0; $i -lt 50 -and -not $p.NaturalDuration.HasTimeSpan; $i++) { Start-Sleep -m 100 }
if (-not $p.NaturalDuration.HasTimeSpan) { exit 1 }
$ms = [Math]::Min($p.NaturalDuration.TimeSpan.TotalMilliseconds, [double]$env:REM_MS)
$vol = [double]$env:REM_VOL
$p.Play(); $sw = [Diagnostics.Stopwatch]::StartNew()
while ($sw.ElapsedMilliseconds -lt $ms) {
    $t = $sw.ElapsedMilliseconds
    $p.Volume = $vol * [Math]::Min(1, [Math]::Min($t / 600, ($ms - $t) / 1000)); Start-Sleep -m 50
}
$p.Close()
"""


def _wpf_play(path, volume):
    env = {**os.environ, "REM_FILE": str(path), "REM_VOL": str(volume), "REM_MS": str(MAX_FILE_SECONDS * 1000)}
    r = subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", _WPF],
                       env=env, creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
    return r.returncode == 0


def play_file(path, volume):
    return _mci_play(path, volume) or _wpf_play(path, volume)


def _play(name, volume):
    f = DIR / name
    if name not in PRESETS and f.is_file() and play_file(f, volume):
        return
    name = name if name in PRESETS else DEFAULT
    data = _cache.setdefault((name, volume), synth(name, volume))
    winsound.PlaySound(data, winsound.SND_MEMORY)


def play(name, volume):
    threading.Thread(target=_play, args=(name, volume), daemon=True).start()
