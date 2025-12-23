import sqlite3
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Hardscapes Word API", version="1.0.0")

# Configure CORS for local development and deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "https://*.vercel.app",   # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "out/words.db"


# Pydantic models for type-safe responses
class WordRow(BaseModel):
    word: str
    zipf: float
    cefr: str
    is_easy: int
    length: int
    difficulty: float
    level: int


class PuzzleResponse(BaseModel):
    letters: List[str]
    words: List[WordRow]
    level: int


def q(sql: str, params=()):
    """Execute SQL query and return results as list of dicts."""
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        return [dict(r) for r in con.execute(sql, params).fetchall()]


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Hardscapes Word API"}


@app.get("/words")
def get_words(
    level: int = Query(1, ge=1, le=50),
    limit: int = Query(50, ge=1, le=500),
    min_len: int = Query(3, ge=3, le=12),
    max_len: int = Query(9, ge=3, le=20),
):
    """
    Fetch words for a specific level with optional filters.
    
    Args:
        level: Game level (1-50)
        limit: Maximum number of words to return
        min_len: Minimum word length
        max_len: Maximum word length
    """
    return q(
        """
        SELECT word, zipf, cefr_norm as cefr, is_easy, length, difficulty, level
        FROM words
        WHERE level = ? AND length BETWEEN ? AND ?
        ORDER BY difficulty ASC, zipf DESC
        LIMIT ?
        """,
        (level, min_len, max_len, limit),
    )


@app.get("/stats")
def get_stats():
    """Get database statistics."""
    try:
        total_words = q("SELECT COUNT(*) as count FROM words")[0]["count"]
        words_by_level = q("""
            SELECT level, COUNT(*) as count
            FROM words
            GROUP BY level
            ORDER BY level
        """)
        return {
            "total_words": total_words,
            "words_by_level": words_by_level
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/puzzle/{level}", response_model=PuzzleResponse)
def get_puzzle(level: int):
    """
    Get a puzzle for a specific level.
    
    Returns puzzle data including words and unique letters.
    
    Args:
        level: Game level (1-50)
    
    Returns:
        PuzzleResponse with letters, words, and level
    """
    if level < 1 or level > 50:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 50")
    
    # Fetch words for this level
    words_data = q(
        """
        SELECT word, zipf, cefr_norm as cefr, is_easy, length, difficulty, level
        FROM words
        WHERE level = ?
        ORDER BY difficulty ASC, zipf DESC
        LIMIT 100
        """,
        (level,),
    )
    
    if not words_data:
        raise HTTPException(status_code=404, detail=f"No words found for level {level}")
    
    # Extract unique letters from all words (sorted, uppercase)
    all_letters = set()
    for word_row in words_data:
        all_letters.update(word_row["word"].upper())
    
    letters = sorted(list(all_letters))
    
    # Convert to WordRow objects
    words = [WordRow(**word) for word in words_data]
    
    return PuzzleResponse(letters=letters, words=words, level=level)