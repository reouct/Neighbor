# Multi-Vehicle Search Take-Home Challenge

## Prerequisites

- Python 3.11+ (developed & tested with CPython 3.13)
- `pip` available on PATH

## 1. Clone & enter the project directory

```bash
git clone https://github.com/reouct/Neighbor
cd Neighbor
```

## 2. Create & activate a virtual environment (recommended)

Windows (bash / Git Bash / WSL style):

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## 3. Install dependencies

Note: the dependency file is intentionally named `requirement.txt` (singular).

```bash
pip install -r requirement.txt
```

## 4. Run the server

```bash
python app.py
```

Environment variables you can optionally set:

- `PORT` - Port to bind (default 5000)
- `LISTINGS_FILE` - Path to an alternate `listings.json` (defaults to bundled file)

With debug mode enabled (default in `app.py`), code changes auto-reload.

## 5. Call the endpoint

```bash
curl -X POST "http://localhost:5000/search" \
    -H "Content-Type: application/json" \
    -d '[{"length":10,"quantity":1}]'
```

Expected example response:

```json
[
  {
    "location_id": "...",
    "listing_ids": ["..."],
    "total_price_in_cents": 1005
  }
]
```

---

## Hosted Endpoint

A live instance is available at:

`https://reouct.pythonanywhere.com/search`

### Make a request

POST a JSON array of vehicle objects (same shape as local usage):

```bash
curl -X POST "https://reouct.pythonanywhere.com/search" \
  -H "Content-Type: application/json" \
  -d '[{"length":10, "quantity":1}]'
```

Example response:

```json
[
  {
    "location_id": "...",
    "listing_ids": ["..."],
    "total_price_in_cents": 1005
  }
]
---
