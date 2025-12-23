# Hardscapes Backend

FastAPI backend for the Hardscapes word game. Builds a ranked word database using CEFR levels and word frequency data, then serves it via REST API.

## Architecture
- **Word Builder**: `build_words.py` - processes CEFR data and creates ranked word database
- **API**: `api.py` - FastAPI app exposing word data endpoints
- **Data**: `data/cefr.csv` - CEFR word list (word, level pairs)
- **Output**: `out/words.db` (SQLite) and `out/words_ranked.csv`

## Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build the word database:
```bash
python build_words.py
```

This creates:
- `out/words_ranked.csv` - CSV with ranked words
- `out/words.db` - SQLite database with indexed words

4. Run the API server:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### `GET /`
Health check endpoint.

### `GET /words`
Fetch words for a specific level.

Query parameters:
- `level` (1-50, default: 1) - Game level
- `limit` (1-500, default: 50) - Max words to return
- `min_len` (3-12, default: 3) - Minimum word length
- `max_len` (3-20, default: 9) - Maximum word length

Response:
```json
[
  {
    "word": "cat",
    "zipf": 5.2,
    "cefr": "A1",
    "is_easy": 1,
    "length": 3,
    "difficulty": 2.1,
    "level": 1
  }
]
```

### `GET /stats`
Get database statistics including total words and words per level.

## Word Ranking System

- **Zipf**: Frequency score from `wordfreq` library (higher = more common)
- **CEFR**: Language level (A1-C2) from input data
- **Difficulty**: Computed from rarity (7 - zipf), CEFR level, and length
- **Level**: Difficulty mapped to game levels 1-50
- **is_easy**: Flag for A1/A2 words or very common words (zipf >= 4.8)

## Development

The API uses CORS middleware to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (alternative dev port)
- Vercel deployments (`*.vercel.app`)

## Deployment

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions on deploying to Railway.

Quick steps:
1. Push code to GitHub
2. Connect repository to Railway
3. Railway will auto-detect Python and use the build configuration
4. Add your Railway domain to CORS in `api.py`

## Data Source

Add your CEFR word list to `data/cefr.csv` with columns:
```
word,cefr
cat,A1
garden,A2
```

The sample data includes ~110 words across all CEFR levels (A1-C2).
