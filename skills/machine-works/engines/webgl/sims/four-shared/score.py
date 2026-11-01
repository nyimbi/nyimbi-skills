"""Score for the OHV four-stroke explorer: a quiet bed (Cmaj/Am chords, 78 bpm), a soft low thud at every spark (the
crank table crossing a firing TDC), a pale intake whoosh as each intake stroke begins, a breath of exhaust after each
power stroke, one air swell under the cutaway sweep and the throttle rise.

    python run_sfx.py sims/four-shared/score.py

Times and the crank model mirror four-shared/film.js: the rpm profile is the same string from the timeline, integrated
the same way (Euler, 1/240 s, playback 1/20), with theta0 set so t=7 lands on intake TDC.
"""

import math
import os

from sfx.score_kit import airy, bed, chords, hz, puff, thud
from sfx.synth import click

HERE = os.path.dirname(os.path.abspath(__file__))
import json

with open(os.path.join(HERE, "..", "four-film", "timeline.json"), encoding="utf8") as f:
    TL = json.load(f)
OUT = os.path.join(os.environ.get("TEARDOWN_OUT", os.path.join(HERE, "..", "..", "teardown-out")), "four-score.wav")
TARGET_LUFS = -14.0
SEED = 13

CHORDS = chords("Cmaj7:C3 E3 G3 B3/C2", "Am9:A2 E3 G3 B3 C4/A1", "Fmaj7:F2 C3 E3 A3/F1", "G6:G2 D3 E3 B3/G1")
MOTIF = [(0.5, hz("G4")), (1.5, hz("E4")), (2.5, hz("B4"))]


def smoother(x):
    u = min(1.0, max(0.0, x))
    return u * u * u * (u * (u * 6 - 15) + 10)


def rpm_at(t):
    keys = [[float(a), float(b)] for a, b in (p.split(":") for p in str(TL["rpm"]).split())]
    for i in range(1, len(keys)):
        t0, v0 = keys[i - 1]
        t1, v1 = keys[i]
        if t <= t1:
            return v0 + (v1 - v0) * smoother((t - t0) / (t1 - t0))
    return keys[-1][1]


PLAY = TL.get("playback", 20)
DT = 1 / 240
DUR = TL["duration"]


def theta_track():
    """The crank table, Euler left-sample, identical to film.js's build."""
    out, th = [], 0.0
    n = int((DUR + 1) / DT)
    for j in range(n):
        out.append(th)
        th += rpm_at(j * DT) / 60 * 360 * DT / PLAY
    return out, ((360 - out[1680] % 720) % 720 + 720) % 720


def crossings(track, th0, target):
    """Seconds where (theta0 + theta(t)) hits `target` degrees mod 720."""
    hits, prev = [], None
    for j, v in enumerate(track):
        cur = (th0 + v) % 720
        if prev is not None:
            # the crank only turns forward, so a wrap from near 720 to near 0
            spanned = cur < prev
            if (prev < target <= cur and not spanned) or (spanned and (target > prev or target <= cur)):
                k = 0 if not spanned else 0
                hits.append(j * DT)
        prev = cur
    return hits


def score(mix, tl):
    dur = tl["duration"]
    left, right, low, drums = bed(dur, 78, CHORDS, MOTIF, motif_voice="epiano", kicks=(0, 2.5), snares=(), hats=6, swing=0.0, keys_vel=0.65, keys_lp=3200)
    mix.put_stereo(0, left, right, 0.11)
    mix.put(0, low, 0.11)
    mix.put(0, drums, 0.03)
    track, th0 = theta_track()
    sparks = crossings(track, th0, 0.0)
    intakes = crossings(track, th0, 360.0)
    exhausts = [t for t in crossings(track, th0, 180.0) if t > 0.4]
    for t in sparks:
        if 0.2 < t < dur - 0.4:
            mix.put(t, thud(58, 0.09, 0.42), 0.16)
    for t in intakes:
        if 0.2 < t < dur - 0.5:
            mix.put(t, airy(1.3, 500, 1500, 0.5), 0.04)
    for t in exhausts:
        mix.put(t, puff(1.0), 0.05)
    # one air swell under the cutaway sweep, another under the throttle rise
    mix.put(3.1, airy(1.6, 700, 1600, 0.6), 0.028)
    mix.put(16.0, airy(1.9, 400, 1300, 0.7), 0.032)
    for t in (3.6, 7.4, 11.6, 16.7):
        mix.put(t, click(2400, 0.025), 0.05)