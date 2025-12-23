from __future__ import annotations

import re
import math
from pathlib import Path
from typing import Optional

import pandas as pd
from wordfreq import zipf_frequency


DATA_DIR = Path("data")
OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

# Rough numeric ordering for CEFR
CEFR_ORDER = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}

WORD_RE = re.compile(r"^[a-z]+$")  # keep it simple for Wordscapes-like gameplay


def normalize(w: str) -> str:
    w = w.strip().lower()
    # keep letters only (drop hyphens/apostrophes etc.)
    w = re.sub(r"[^a-z]", "", w)
    return w


def cefr_to_num(level: Optional[str]) -> float:
    if not level:
        return float("nan")
    level = level.strip().upper()
    return float(CEFR_ORDER.get(level, math.nan))


def compute_difficulty(zipf: float, cefr_num: float, length: int) -> float:
    """
    Higher difficulty = harder.
    Heuristic (tune later):
      - rarer words (lower zipf) are harder
      - higher CEFR is harder
      - longer words are a bit harder
    """
    # zipf is usually ~1..7 for English words
    rarity = max(0.0, 7.0 - zipf)  # 0 (very common) .. ~6 (very rare)
    cefr_component = 0.0 if math.isnan(cefr_num) else (cefr_num - 1.0)  # 0..5
    length_component = max(0.0, length - 3) * 0.35  # 3-letter baseline

    return (rarity * 1.2) + (cefr_component * 0.9) + length_component


def assign_level(difficulty: float) -> int:
    """
    Maps difficulty to level buckets 1..50.
    Replace with quantiles if you prefer perfectly-even level sizes.
    """
    # clamp-ish
    d = max(0.0, min(20.0, difficulty))
    # 0..20 -> 1..50
    return int(1 + round((d / 20.0) * 49))


def main():
    cefr_path = DATA_DIR / "cefr.csv"
    if not cefr_path.exists():
        raise FileNotFoundError(f"Missing {cefr_path}. Create it with columns: word,cefr")

    cefr_df = pd.read_csv(cefr_path)
    if not {"word", "cefr"}.issubset(set(c for c in cefr_df.columns)):
        raise ValueError("cefr.csv must have columns: word, cefr")

    # normalize + dedupe
    cefr_df["word"] = cefr_df["word"].astype(str).map(normalize)
    cefr_df = cefr_df.dropna(subset=["word"])
    cefr_df = cefr_df[cefr_df["word"].str.match(WORD_RE)]
    cefr_df = cefr_df.drop_duplicates(subset=["word"], keep="first")

    # compute frequency
    cefr_df["zipf"] = cefr_df["word"].map(lambda w: float(zipf_frequency(w, "en")))
    cefr_df["length"] = cefr_df["word"].str.len()

    # easy flag: CEFR A1/A2 or very common
    cefr_df["cefr_norm"] = cefr_df["cefr"].astype(str).str.upper().str.strip()
    cefr_df["cefr_num"] = cefr_df["cefr_norm"].map(lambda x: cefr_to_num(x))
    cefr_df["is_easy"] = (
        cefr_df["cefr_norm"].isin(["A1", "A2"])
        | (cefr_df["zipf"] >= 4.8)
    )

    # difficulty + level
    cefr_df["difficulty"] = cefr_df.apply(
        lambda r: compute_difficulty(r["zipf"], r["cefr_num"], int(r["length"])),
        axis=1
    )
    cefr_df["level"] = cefr_df["difficulty"].map(assign_level)

    # basic filters for Wordscapes-like play (tune)
    cefr_df = cefr_df[(cefr_df["length"] >= 3) & (cefr_df["length"] <= 9)]
    cefr_df = cefr_df.sort_values(["level", "difficulty", "zipf"], ascending=[True, True, False])

    out_csv = OUT_DIR / "words_ranked.csv"
    cefr_df[["word", "zipf", "cefr_norm", "is_easy", "length", "difficulty", "level"]].to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} ({len(cefr_df)} rows)")

    # Optional: SQLite for fast queries
    try:
        import sqlite3
        out_db = OUT_DIR / "words.db"
        with sqlite3.connect(out_db) as con:
            cefr_df.to_sql("words", con, if_exists="replace", index=False)
            con.execute("CREATE INDEX IF NOT EXISTS idx_words_level ON words(level);")
            con.execute("CREATE INDEX IF NOT EXISTS idx_words_word ON words(word);")
        print(f"Wrote {out_db}")
    except Exception as e:
        print(f"SQLite skipped: {e}")


if __name__ == "__main__":
    main()
