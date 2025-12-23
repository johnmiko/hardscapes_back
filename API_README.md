# Hardscapes API Documentation

FastAPI backend serving word data for the Hardscapes game.

## Base URL
- Local: `http://localhost:8000`
- Production: TBD

## Authentication
No authentication required for current endpoints.

---

## Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Hardscapes Word API"
}
```

---

### `GET /words`
Fetch words for a specific game level.

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `level` | int | 1 | 1-50 | Game level |
| `limit` | int | 50 | 1-500 | Maximum words to return |
| `min_len` | int | 3 | 3-12 | Minimum word length |
| `max_len` | int | 9 | 3-20 | Maximum word length |

**Example Request:**
```
GET /words?level=1&limit=100&min_len=3&max_len=7
```

**Response:**
```json
[
  {
    "word": "cat",
    "zipf": 5.234,
    "cefr": "A1",
    "is_easy": 1,
    "length": 3,
    "difficulty": 2.145,
    "level": 1
  },
  {
    "word": "dog",
    "zipf": 5.123,
    "cefr": "A1",
    "is_easy": 1,
    "length": 3,
    "difficulty": 2.234,
    "level": 1
  }
]
```

**Response Fields:**
- `word` (string): The English word
- `zipf` (float): Frequency score (higher = more common, typical range 1-7)
- `cefr` (string): Language level (A1, A2, B1, B2, C1, C2)
- `is_easy` (int): 1 if easy (A1/A2 or very common), 0 otherwise
- `length` (int): Number of letters
- `difficulty` (float): Computed difficulty score
- `level` (int): Game level (1-50)

---

### `GET /stats`
Get database statistics.

**Response:**
```json
{
  "total_words": 91,
  "words_by_level": [
    {
      "level": 1,
      "count": 15
    },
    {
      "level": 2,
      "count": 12
    }
  ]
}
```

**Response Fields:**
- `total_words` (int): Total number of words in database
- `words_by_level` (array): Count of words per level

---

## Difficulty Calculation

The difficulty score is computed using:
```python
rarity = max(0.0, 7.0 - zipf)  # 0 (very common) to ~6 (very rare)
cefr_component = 0.0 if unknown else (cefr_num - 1.0)  # 0 to 5
length_component = max(0.0, length - 3) * 0.35  # 3-letter baseline

difficulty = (rarity * 1.2) + (cefr_component * 0.9) + length_component
```

Where:
- Lower zipf = rarer word = harder
- Higher CEFR level = harder
- Longer words are slightly harder

## Level Assignment

Difficulty scores (0-20) are mapped to levels (1-50):
```python
level = 1 + round((difficulty / 20.0) * 49)
```

---

## CORS

The API allows cross-origin requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (alternative dev port)
- `*.vercel.app` (Vercel deployments)

---

## Interactive Documentation

FastAPI provides interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Error Handling

Standard HTTP status codes:
- `200 OK`: Successful request
- `422 Unprocessable Entity`: Invalid query parameters
- `500 Internal Server Error`: Database or server error

---

## Database Schema

SQLite database (`out/words.db`) with one table:

**words**
| Column | Type | Description |
|--------|------|-------------|
| word | TEXT | The word |
| zipf | REAL | Frequency score |
| cefr_norm | TEXT | CEFR level |
| is_easy | INTEGER | Easy flag (0/1) |
| length | INTEGER | Word length |
| difficulty | REAL | Difficulty score |
| level | INTEGER | Game level |

**Indexes:**
- `idx_words_level` on `level`
- `idx_words_word` on `word`
