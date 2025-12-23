import sqlite3
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

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
