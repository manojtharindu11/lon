# lon – Dialogflow Webhook + Menu UI

This repository contains:

- A **FastAPI** webhook for a **Dialogflow** agent (order tracking / add / remove / complete).
- A simple static menu page in `static webpage/`.

## Prerequisites

- Python 3.x
- MySQL (with the tables/data used by the bot)
- `ngrok` (included as `ngrok.exe` in this repo)

## Setup

1. Create/activate a virtual environment (optional but recommended).

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables.

Copy `.env.example` to `.env` and set your MySQL credentials:

```env
HOST=localhost
USER=root
PASSWORD=your_password
DATABASE=ape_kama_db
```

## Run the API (uvicorn)

Start the FastAPI app with:

```bash
uvicorn run:app --reload
```

By default this runs on `http://127.0.0.1:8000/`.

Routes:

- `GET /` – simple health check
- `POST /` – Dialogflow webhook endpoint (expects a Dialogflow webhook request body)

## Expose HTTPS with ngrok (for Dialogflow)

Dialogflow typically requires a public HTTPS webhook URL. Run ngrok to expose your local uvicorn port:

```bash
.\ngrok.exe http 8000
```

Then:

1. Copy the **Forwarding** HTTPS URL printed by ngrok (example: `https://xxxx.ngrok-free.app`).
2. In Dialogflow, set the webhook/fulfillment URL to:

```
https://xxxx.ngrok-free.app/
```

Keep both `uvicorn` and `ngrok` running while testing the bot.

## Static menu page

Open the menu UI at:

- `static webpage/index.html`

(You can open it directly in a browser, or serve it with any static server.)

## Notes

- `requirements.txt` in this repo is UTF-16 encoded. If `pip install -r requirements.txt` fails on your machine, convert it to UTF-8 and retry.
