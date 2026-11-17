#!/usr/bin/env python3
import math, random, struct, wave
from pathlib import Path

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "sounds"
OUT.mkdir(exist_ok=True)
random.seed(4242)

def envelope(n, attack=0.004, release=0.035):
    a = max(1, int(attack * SR))
    r = max(1, int(release * SR))
    out = []
    for i in range(n):
        if i < a:
            v = i / a
        elif i > n - r:
            v = max(0.0, (n - i) / r)
        else:
            v = 1.0
        out.append(v)
    return out

def tone(f0, f1, dur, kind="square", amp=0.35, bit=8, noise=0.0, release=0.035):
    n = max(1, int(dur * SR))
    env = envelope(n, release=release)
    phase = 0.0
    data = []
    levels = 2 ** (bit - 1)
    for i in range(n):
        t = i / n
        f = f0 + (f1 - f0) * t
        phase += 2 * math.pi * f / SR
        if kind == "square":
            s = 1.0 if math.sin(phase) >= 0 else -1.0
        elif kind == "saw":
            s = 2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0
        elif kind == "tri":
            s = 2.0 * abs(2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0) - 1.0
        else:
            s = math.sin(phase)
        s = round(s * levels) / levels
        if noise:
            s += (random.random() * 2 - 1) * noise
        data.append(max(-1.0, min(1.0, s * amp * env[i])))
    return data

def silence(dur):
    return [0.0] * max(0, int(dur * SR))

def mix(*tracks):
    size = max(len(track) for track in tracks)
    out = [0.0] * size
    for track in tracks:
        for i, value in enumerate(track):
            out[i] += value
    return out

def sequence(*parts):
    out = []
    for part in parts:
        out.extend(part)
    return out

def normalize(data, peak=0.72):
    top = max(abs(x) for x in data) or 1.0
    return [x / top * peak for x in data]

def save(name, data):
    data = normalize(data)
    path = OUT / name
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        frames = b"".join(struct.pack("<h", int(x * 32767)) for x in data)
        wav.writeframes(frames)
    print(f"{name:24} {path.stat().st_size:6} bytes")

save("boot.wav", mix(tone(120, 980, 0.34, "saw", 0.28, noise=0.035, release=0.12), tone(60, 120, 0.22, "sine", 0.18)))
save("hover.wav", mix(tone(1650, 2100, 0.025, "square", 0.18, release=0.012), tone(90, 90, 0.018, "sine", 0.12, release=0.01)))
save("select.wav", mix(tone(880, 660, 0.075, "square", 0.26), tone(1760, 1320, 0.04, "sine", 0.12)))
save("back.wav", mix(tone(520, 260, 0.085, "square", 0.24), tone(130, 110, 0.04, "sine", 0.14)))
save("send.wav", mix(tone(1400, 920, 0.035, "square", 0.18, release=0.02), tone(120, 80, 0.04, "sine", 0.2, release=0.03), tone(0, 0, 0.006, "square", 0.12, noise=0.3, release=0.004)))
save("receive.wav", mix(tone(520, 780, 0.085, "tri", 0.24), tone(1040, 1560, 0.045, "sine", 0.1)))
save("reply.wav", sequence(tone(660, 880, 0.05, "square", 0.2), tone(880, 660, 0.07, "square", 0.2)))
save("mention.wav", sequence(tone(880, 880, 0.05, "square", 0.24), silence(0.025), tone(1320, 1320, 0.05, "square", 0.2), silence(0.02), tone(1760, 1760, 0.08, "square", 0.16)))
save("mute.wav", mix(tone(420, 200, 0.1, "square", 0.24), tone(100, 80, 0.06, "sine", 0.16)))
save("unmute.wav", mix(tone(200, 420, 0.1, "square", 0.24), tone(80, 120, 0.06, "sine", 0.16)))
save("deafen.wav", mix(tone(320, 150, 0.13, "saw", 0.22, noise=0.03), tone(90, 60, 0.08, "sine", 0.18)))
save("undeafen.wav", mix(tone(150, 320, 0.13, "saw", 0.22), tone(60, 90, 0.08, "sine", 0.18)))
save("join.wav", mix(tone(280, 880, 0.2, "tri", 0.22, noise=0.025), tone(560, 1760, 0.1, "sine", 0.09)))
save("leave.wav", mix(tone(820, 190, 0.2, "tri", 0.22), tone(410, 90, 0.12, "sine", 0.1)))
save("disconnect.wav", mix(tone(520, 90, 0.24, "saw", 0.22, noise=0.06, release=0.1), tone(80, 50, 0.16, "sine", 0.12)))
save("reconnect.wav", mix(tone(180, 760, 0.22, "tri", 0.22), tone(90, 380, 0.1, "sine", 0.1)))
save("ring.wav", sequence(tone(440, 440, 0.14, "tri", 0.2), silence(0.04), tone(480, 480, 0.14, "tri", 0.18), silence(0.04), tone(440, 440, 0.14, "tri", 0.15)))
save("success.wav", sequence(tone(660, 660, 0.09, "tri", 0.22), tone(990, 990, 0.17, "tri", 0.2, release=0.1)))
save("error.wav", mix(tone(130, 95, 0.22, "square", 0.26, noise=0.035, release=0.08), tone(65, 55, 0.14, "sine", 0.14)))
save("stream-on.wav", mix(tone(380, 1100, 0.16, "saw", 0.2, noise=0.02), tone(760, 2200, 0.08, "sine", 0.08)))
save("stream-off.wav", mix(tone(1100, 260, 0.16, "saw", 0.2), tone(550, 130, 0.08, "sine", 0.08)))
save("ptt-on.wav", mix(tone(900, 900, 0.04, "square", 0.18), tone(180, 180, 0.03, "sine", 0.1)))
save("ptt-off.wav", mix(tone(500, 500, 0.04, "square", 0.16), tone(100, 100, 0.03, "sine", 0.09)))
