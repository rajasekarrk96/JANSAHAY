"""Generate a placeholder narration track (Windows SAPI) aligned to the cue timeline,
plus an SRT for dubbing a human voice over the silent master."""
import os, sys, subprocess, wave, json
import numpy as np

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from timeline import TOTAL, build_cues

VOICE = "Microsoft Zira Desktop"
SR = 44100
TTS_DIR = os.path.join(SP, "tts")
os.makedirs(TTS_DIR, exist_ok=True)
OUT_WAV = os.path.join(SP, "narration.wav")
OUT_SRT = os.path.join(SP, "narration.srt")

CUES = build_cues()

PS = r'''
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {{ $s.SelectVoice("{voice}") }} catch {{ }}
$s.Rate = {rate}
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo({sr}, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
$s.SetOutputToWaveFile("{path}", $fmt)
$s.Speak(@'
{text}
'@)
$s.SetOutputToNull()
$s.Dispose()
'''


def synth(text, path, rate):
    script = PS.format(voice=VOICE, rate=rate, sr=SR, path=path.replace("\\", "/"), text=text)
    r = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "ignore")[:400])
    with wave.open(path, "rb") as w:
        return w.getnframes() / w.getframerate()


def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getsampwidth() == 2 and w.getnchannels() == 1
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        return data, w.getframerate()


def srt_ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main():
    track = np.zeros(int(TOTAL * SR) + SR, dtype=np.float32)
    report = []

    for i, (cs, ce, text) in enumerate(CUES):
        slot = ce - cs
        path = os.path.join(TTS_DIR, f"cue{i:02d}.wav")
        rate, dur = 0, None
        for attempt in range(5):
            dur = synth(text, path, rate)
            if dur <= slot - 0.15:
                break
            rate += 1                      # nudge the voice faster until it fits
        data, sr = read_wav(path)
        assert sr == SR, sr
        start = int(cs * SR)
        seg = data.astype(np.float32) / 32768.0
        end = min(start + len(seg), len(track))
        track[start:end] += seg[:end - start]
        report.append({"cue": i, "start": cs, "slot": round(slot, 2),
                       "spoken": round(dur, 2), "rate": rate, "text": text})
        print(f"  {i:02d} slot={slot:5.2f}s spoken={dur:5.2f}s rate={rate}  {text[:52]}")

    track = track[:int(TOTAL * SR)]
    peak = float(np.max(np.abs(track))) or 1.0
    track = np.clip(track / peak * 0.85, -1.0, 1.0)
    pcm = (track * 32767).astype(np.int16)
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", OUT_WAV, os.path.getsize(OUT_WAV) // 1024, "KB")

    with open(OUT_SRT, "w", encoding="utf-8") as f:
        for i, (cs, ce, text) in enumerate(CUES, 1):
            f.write(f"{i}\n{srt_ts(cs)} --> {srt_ts(ce)}\n{text}\n\n")
    print("wrote", OUT_SRT)

    json.dump(report, open(os.path.join(SP, "narration_report.json"), "w"), indent=2)
    over = [r for r in report if r["spoken"] > r["slot"]]
    print("cues that still overflow their slot:", len(over))
    for r in over:
        print("   ", r["cue"], r["slot"], r["spoken"], r["text"][:40])


if __name__ == "__main__":
    main()
