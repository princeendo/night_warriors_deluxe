"""EXP-0009: search a session recording for one sound-chip sample.

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0009/wavsearch.py \
        SESSION_WAV BIN_FILE OFFSET LENGTH RATE OUT_DIR [THRESHOLD]

Builds the sample's waveform from ``BIN_FILE`` (signed 8-bit PCM, LENGTH
samples from OFFSET, as the SCSP plays an 8-bit slot), at RATE Hz (from the
slot's OCT/FNS registers). ffmpeg resamples the session recording and the
sample to 16 kHz mono; ``afir`` with the reversed sample as impulse response
gives the cross-correlation. The normalized cross-correlation (divided by the
sample's norm and the recording's norm over the same window) is scanned for
peaks above THRESHOLD (default 0.5), at least one sample length apart. Prints
one line per peak: start time in seconds and the score. Work files go to
OUT_DIR (ignored).
"""

from __future__ import annotations

import array
import math
import subprocess
import sys
import wave
from itertools import accumulate
from pathlib import Path

SR = 16000


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args], check=True)


def read_f32(path: Path) -> array.array[float]:
    data = array.array("f")
    data.frombytes(path.read_bytes())
    return data


def peaks(score: list[float], threshold: float, gap: int) -> list[tuple[int, float]]:
    found: list[tuple[int, float]] = []
    i = 0
    while i < len(score):
        if score[i] >= threshold:
            j = max(range(i, min(i + gap, len(score))), key=score.__getitem__)
            found.append((j, score[j]))
            i = j + gap
        else:
            i += 1
    return found


def main(
    session: Path,
    bin_file: Path,
    offset: int,
    length: int,
    rate: int,
    out: Path,
    threshold: float,
) -> int:
    out.mkdir(parents=True, exist_ok=True)
    raw = bin_file.read_bytes()[offset : offset + length]
    pcm = array.array("h", ((b - 256 if b > 127 else b) * 256 for b in raw))
    tmpl = out / "template.wav"
    with wave.open(str(tmpl), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm.tobytes())
    ffmpeg(
        "-i", str(tmpl), "-ac", "1", "-ar", str(SR), "-f", "f32le", str(out / "t.f32")
    )
    ffmpeg(
        "-i",
        str(tmpl),
        "-af",
        "areverse",
        "-ac",
        "1",
        "-ar",
        str(SR),
        str(out / "trev.wav"),
    )
    sig_path = out / "s.f32"
    if not sig_path.exists():
        ffmpeg(
            "-i", str(session), "-ac", "1", "-ar", str(SR), "-f", "f32le", str(sig_path)
        )
    ffmpeg(
        "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(sig_path),
        "-i", str(out / "trev.wav"),
        "-lavfi", "[0][1]afir=irnorm=-1:gtype=-1:dry=1:wet=1:length=1",
        "-f", "f32le", "-ac", "1", str(out / "c.f32"),
    )  # fmt: skip
    t = read_f32(out / "t.f32")
    s = read_f32(sig_path)
    c = read_f32(out / "c.f32")
    n = len(t)
    t_norm = math.sqrt(sum(x * x for x in t))
    energy = [0.0, *accumulate(x * x for x in s)]
    score: list[float] = []
    for end in range(len(c)):
        lo = max(0, end - n + 1)
        e = energy[min(end + 1, len(s))] - energy[lo]
        score.append(c[end] / (t_norm * math.sqrt(e)) if e > 1e-9 else 0.0)
    for end, value in peaks(score, threshold, n):
        print(f"{(end - n + 1) / SR:9.3f} s  score {value:.3f}")
    return 0


if __name__ == "__main__":
    assert peaks([0, 0.6, 0.9, 0.2, 0, 0.7], 0.5, 3) == [(2, 0.9), (5, 0.7)]
    a = sys.argv
    raise SystemExit(
        main(
            Path(a[1]),
            Path(a[2]),
            int(a[3], 0),
            int(a[4], 0),
            int(a[5]),
            Path(a[6]),
            float(a[7]) if len(a) > 7 else 0.5,
        )
    )
