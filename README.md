# Stocker

Simple Flask dashboard that surfaces the top 10 Indian stocks with quick analytics.

## Stack
- Python 3.x, Flask
- yfinance for data fetch
- Matplotlib for charts (rendered to base64)
- Frontend: vanilla HTML + CSS (see `app/static/styles.css`)

## Getting started
1) Create and activate a virtual env (recommended).
2) Install deps:
```bash
pip install -r requirements.txt
```
3) Run the app:
```bash
python app.py
```
4) Open `http://127.0.0.1:5000/`.

## Project structure
- `app/routes.py` — Flask routes (leave intact as requested)
- `app/templates/` — HTML templates for dashboard and analytics
- `app/static/styles.css` — UI styling
- `stocks.csv` — data file (if needed elsewhere)

## Notes
- UI was refreshed; backend logic remains untouched.
- Charts are generated at request time; keep an eye on rate limits when developing.
