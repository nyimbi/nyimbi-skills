#!/usr/bin/env python3
"""storycheck — diagnostic checks for a Fountain screenplay.

This is a defect finder, not a quality verdict. It measures structural facts a
reader can verify and flags the usual failure patterns. It cannot judge taste,
surprise, or whether the film is worth making.

    python3 storycheck.py screenplay.fountain
    python3 storycheck.py screenplay.fountain --cards scene-cards.csv
    python3 storycheck.py screenplay.fountain --ledger setup-payoff.csv
    python3 storycheck.py screenplay.fountain --out ../01_story/quality-report.md

Exit code is 0 for a completed diagnostic, 2 for a missing or unreadable input.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCENE_RE = re.compile(r"^(INT\.|EXT\.|EST\.|INT\./EXT\.|I/E\.)", re.I)
TRANSITION_RE = re.compile(r"(TO:|FADE OUT\.|FADE IN:|CUT TO:)\s*$", re.I)
UNFILMABLE_RE = re.compile(
    r"\b(remembers?|thinks?|feels?|realizes?|understands?|knows?|wants?|hopes?|"
    r"regrets?|loves?|hates?|decides?)\b",
    re.I,
)
ON_THE_NOSE_RE = re.compile(
    r"\b(I feel|I'm (angry|sad|afraid|scared|happy|furious)|I love you|I hate you|"
    r"the truth is|the point is|you don't understand|I need you)\b",
    re.I,
)
PASSIVE_RE = re.compile(r"\b(was|were|is|are|been|being)\s+\w+(ed|en)\b", re.I)
WORD_RE = re.compile(r"[A-Za-z']+")

STOPWORDS = set(
    "a an the and or but if then than that this these those i you he she it we they "
    "me him her us them my your his its our their to of in on at for from with by as "
    "is are was were be been being do does did not no yes so just very really about "
    "what who whom which when where why how there here have has had will would can "
    "could should may might must shall".split()
)


def parse_fountain(text: str):
    lines = text.splitlines()
    scenes = []          # (index, heading, start_line, words, action_lines, dialogue_lines)
    actions = []         # (line_no, scene_idx, text)
    dialogue = []        # (line_no, scene_idx, character, text)
    characters = Counter()
    current_scene = -1
    i = 0

    # skip a Fountain title page: key: value lines at the top
    while i < len(lines):
        s = lines[i].strip()
        if not s or re.match(r"^(title|credit|author|draft date|contact|source)\s*:", s, re.I):
            i += 1
            if scenes:
                break
            continue
        break

    in_boneyard = False
    in_note = False
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        line_no = i + 1

        if "/*" in s:
            in_boneyard = True
        if in_boneyard:
            if "*/" in s:
                in_boneyard = False
            i += 1
            continue
        if s.startswith("[[") or in_note:
            in_note = not s.endswith("]]")
            i += 1
            continue
        if not s or s.startswith(("#", "=", ">", "~")):
            i += 1
            continue

        if SCENE_RE.match(s):
            current_scene += 1
            scenes.append({
                "index": current_scene + 1,
                "heading": s,
                "start_line": line_no,
                "words": 0,
                "action_lines": 0,
                "dialogue_lines": 0,
            })
            i += 1
            continue

        if current_scene < 0:
            i += 1
            continue

        # character cue: uppercase line followed by non-empty dialogue
        cue = s
        m = re.match(r"^(?P<name>@?[A-Z][A-Z0-9 .'\-]*(?:\s*\([^)]*\))?)\s*\^?\s*$", cue)
        nxt = ""
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            nxt = lines[j].strip()
        is_cue = bool(m) and nxt and not SCENE_RE.match(nxt) and not nxt.startswith("[[")

        if is_cue and m is not None and not TRANSITION_RE.search(s):
            name = re.sub(r"\s*\([^)]*\)", "", m.group("name")).replace("@", "").strip().upper()
            characters[name] += 1
            scenes[current_scene]["dialogue_lines"] += 1
            k = j
            said = []
            while k < len(lines):
                d = lines[k].strip()
                if not d:
                    break
                if SCENE_RE.match(d) or d.startswith("[[") or TRANSITION_RE.search(d):
                    break
                if re.match(r"^@?[A-Z][A-Z0-9 .'\-]*(?:\s*\([^)]*\))?\s*\^?\s*$", d):
                    break
                if not (d.startswith("(") and d.endswith(")")):
                    said.append(d)
                k += 1
            text = " ".join(said)
            if text:
                dialogue.append((line_no, current_scene, name, text))
                words = len(WORD_RE.findall(text))
                scenes[current_scene]["words"] += words
            i = k
            continue

        if not TRANSITION_RE.search(s):
            actions.append((line_no, current_scene, s))
            scenes[current_scene]["action_lines"] += 1
            scenes[current_scene]["words"] += len(WORD_RE.findall(s))
        i += 1

    return scenes, actions, dialogue, characters


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def voice_profiles(dialogue, top: int = 8):
    by_char = defaultdict(list)
    for _, _, name, text in dialogue:
        by_char[name].extend(w.lower() for w in WORD_RE.findall(text) if w.lower() not in STOPWORDS)
    profiles = []
    for name, words in sorted(by_char.items(), key=lambda kv: -len(kv[1]))[:top]:
        if len(words) < 15:
            continue
        profiles.append((name, set(words), len(words)))
    return profiles


def ngrams(dialogue, n: int = 4, min_count: int = 3):
    counts = Counter()
    for _, _, _, text in dialogue:
        toks = [w.lower() for w in WORD_RE.findall(text)]
        for k in range(len(toks) - n + 1):
            counts[tuple(toks[k:k + n])] += 1
    return [(g, c) for g, c in counts.most_common(20) if c >= min_count][:5]


def read_cards(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return [], ["cards file has no rows"]
    headers = {h.lower().strip() for h in rows[0].keys()}
    required = {"scene", "goal", "conflict", "turn", "outcome"}
    missing = sorted(required - headers)
    problems = []
    if missing:
        problems.append("cards missing columns: " + ", ".join(missing))
    empty = []
    for idx, row in enumerate(rows, start=2):
        for key in required & headers:
            if not (row.get(key) or "").strip():
                empty.append(f"row {idx}: empty {key}")
    turns = [(row.get("turn") or "").strip().lower() for row in rows]
    dup = sorted({t for t in turns if t and turns.count(t) > 1})
    if dup:
        problems.append("duplicate turns: " + "; ".join(dup))
    problems.extend(empty)
    return rows, problems


def read_ledger(path: Path, scenes):
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    headings = [s["heading"].lower() for s in scenes]
    problems = []
    matched = 0

    def exists(value: str) -> bool:
        v = value.strip()
        if not v:
            return False
        if v.isdigit() and 1 <= int(v) <= len(scenes):
            return True
        return any(v.lower() in h for h in headings)

    for idx, row in enumerate(rows, start=2):
        setup = (row.get("setup_scene") or row.get("setup") or "").strip()
        payoff = (row.get("payoff_scene") or row.get("payoff") or "").strip()
        if not setup or not payoff:
            problems.append(f"row {idx}: setup and payoff are required")
            continue
        if not exists(setup):
            problems.append(f"row {idx}: setup scene not found: {setup}")
        if not exists(payoff):
            problems.append(f"row {idx}: payoff scene not found: {payoff}")
        if exists(setup) and exists(payoff):
            matched += 1
    return len(rows), matched, problems


def main() -> None:
    ap = argparse.ArgumentParser(prog="storycheck")
    ap.add_argument("screenplay")
    ap.add_argument("--cards")
    ap.add_argument("--ledger")
    ap.add_argument("--out")
    args = ap.parse_args()

    path = Path(args.screenplay).expanduser()
    if not path.is_file():
        print(f"storycheck: not found: {path}", file=sys.stderr)
        raise SystemExit(2)

    text = path.read_text(encoding="utf-8", errors="replace")
    scenes, actions, dialogue, characters = parse_fountain(text)
    if not scenes:
        print("storycheck: no scene headings found", file=sys.stderr)
        raise SystemExit(2)

    total_words = sum(s["words"] for s in scenes)
    dialogue_words = sum(len(WORD_RE.findall(t)) for _, _, _, t in dialogue)
    action_words = sum(len(WORD_RE.findall(a)) for _, _, a in actions)

    out = []
    add = out.append
    add(f"# Story Check — {path.name}\n")
    add("> Diagnostic only. A clean run does not mean the script is good; it means the "
        "mechanical defects below were not found.\n")

    add("## Summary\n")
    add(f"- Scenes: **{len(scenes)}**")
    add(f"- Words: **{total_words}** "
        f"({dialogue_words} dialogue, {action_words} action)")
    add(f"- Estimated runtime: **{total_words/150:.1f} min** at 150 wpm; "
        f"**{total_words/130:.1f} min** at 130 wpm")
    add(f"- Dialogue/action word ratio: **{dialogue_words/max(action_words,1):.2f}**")
    add(f"- Characters with dialogue: **{len(characters)}**")
    add("")

    add("## Scene lengths\n")
    lengths = sorted(scenes, key=lambda s: s["words"], reverse=True)
    add(f"- Average: **{total_words/len(scenes):.0f} words/scene**")
    add(f"- Longest: **{lengths[0]['words']} words** — {lengths[0]['heading']}")
    add(f"- Shortest: **{lengths[-1]['words']} words** — {lengths[-1]['heading']}")
    short = [s for s in scenes if s["words"] < 40]
    if short:
        add(f"- Under 40 words: {len(short)} scenes "
            f"(first: {short[0]['heading']}) — check they are not fragments")
    add("")

    add("## Dialogue share\n")
    add("| Character | Lines | Words |")
    add("|---|---:|---:|")
    by_char = defaultdict(lambda: [0, 0])
    for _, _, name, txt in dialogue:
        by_char[name][0] += 1
        by_char[name][1] += len(WORD_RE.findall(txt))
    for name, (lines, words) in sorted(by_char.items(), key=lambda kv: -kv[1][1])[:12]:
        add(f"| {name} | {lines} | {words} |")
    add("")

    profiles = voice_profiles(dialogue)
    add("## Voice distinctiveness\n")
    add("Jaccard similarity of stopword-filtered vocabulary. Above 0.55 suggests two "
        "characters are speaking with one voice.\n")
    flagged = []
    for i in range(len(profiles)):
        for j in range(i + 1, len(profiles)):
            a, b = profiles[i], profiles[j]
            sim = jaccard(a[1], b[1])
            if sim > 0.55:
                flagged.append((a[0], b[0], sim))
    if flagged:
        for a, b, sim in flagged:
            add(f"- **{a} / {b}: {sim:.2f}** — differentiate vocabulary, syntax or evasion")
    else:
        add("- No pair above 0.55 in the measured cast.")
    add("")

    add("## Agency proxy\n")
    add("Scenes where the character appears in action lines or speaks. A lead below ~25% "
        "of scenes may be reacting rather than driving.\n")
    add("| Character | Scenes present | Share |")
    add("|---|---:|---:|")
    for name, _ in sorted(by_char.items(), key=lambda kv: -kv[1][1])[:8]:
        present = len({s for (_, s, n, _) in dialogue if n == name} |
                      {s for (_, s, a) in actions
                       if re.search(rf"\b{re.escape(name)}\b", a, re.I)})
        share = present / len(scenes)
        flag = " ⚠" if share < 0.25 else ""
        add(f"| {name} | {present} | {share:.0%}{flag} |")
    add("")

    add("## Flags\n")
    unfilm = [(ln, a) for ln, _, a in actions if UNFILMABLE_RE.search(a)]
    add(f"### Unfilmable interior states in action: **{len(unfilm)}**")
    for ln, a in unfilm[:8]:
        add(f"- L{ln}: {a[:140]}")
    add("")

    onnose = [(ln, name, txt) for ln, _, name, txt in dialogue if ON_THE_NOSE_RE.search(txt)]
    add(f"### On-the-nose dialogue: **{len(onnose)}**")
    for ln, name, txt in onnose[:8]:
        add(f"- L{ln} {name}: {txt[:140]}")
    add("")

    passive = [a for _, _, a in actions if PASSIVE_RE.search(a)]
    add(f"### Passive constructions in action: **{len(passive)}**")
    add("")

    repeats = ngrams(dialogue)
    add("### Repeated 4-grams in dialogue")
    if repeats:
        for gram, count in repeats:
            add(f"- \"{' '.join(gram)}\" ×{count}")
    else:
        add("- None at ≥3 occurrences.")
    add("")

    add("## Cards\n")
    if args.cards:
        rows, problems = read_cards(Path(args.cards).expanduser())
        add(f"- Rows: {len(rows)}")
        if problems:
            for p in problems[:12]:
                add(f"- ⚠ {p}")
        else:
            add("- All required fields present; no duplicate turns.")
    else:
        add("- No cards file supplied. Every scene needs goal, conflict, turn, outcome.")
    add("")

    add("## Setup / payoff ledger\n")
    if args.ledger:
        total, matched, problems = read_ledger(Path(args.ledger).expanduser(), scenes)
        add(f"- Rows: {total}; matched: {matched}")
        for p in problems[:12]:
            add(f"- ⚠ {p}")
    else:
        add("- No ledger supplied. Every setup needs a payoff; every payoff needs a setup.")
    add("")

    add("## Manual rubric\n")
    add("Score 0–4. Target average ≥ 3.0, no dimension ≤ 2, plus the hard checks and a "
        "human sign-off. Evidence is required for anything below 3.\n")
    add("| Dimension | Score | Evidence | Fix |")
    add("|---|---:|---|---|")
    for d in ["Premise", "Structure", "Character", "Agency", "Scene craft",
              "Dialogue", "Theme / emotion", "Originality / feasibility"]:
        add(f"| {d} | | | |")
    add("| **Average** | | | |")
    add("")

    report = "\n".join(out) + "\n"
    if args.out:
        Path(args.out).expanduser().write_text(report, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
