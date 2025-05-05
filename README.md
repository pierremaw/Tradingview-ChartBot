# TradingView Chart Automation

[https://github.com/user-attachments/assets/f266d143-5bb5-4d9f-87a1-150726d078a8](https://github.com/user-attachments/assets/f266d143-5bb5-4d9f-87a1-150726d078a8)

**TradingView Chart Automation** is a Python‑based micro‑service that automatically captures real‑time chart snapshots from TradingView and updates them to Airtable via webhooks.  
Built with Selenium and Flask, it runs on a remote server, listens for asset data, and delivers TradingView snapshot images directly into structured Airtable records.

I created this project to explore automated financial data visualisation and sharpen my full‑stack Python skills.

This project reflects my proficiency in:

- Using Selenium to control browser behaviour for authenticated sites
- Creating and managing Flask APIs
- Handling secure credential storage with `dotenv`
- Building a **concise single‑file micro‑service** for automation
- Integrating with external APIs (in this case, Airtable)
- Optionally containerising and running code on a VPS with Docker + env‑vars

## How It Works

When triggered by a webhook, the bot executes the following steps:

1. Launches a browser session through Selenium Grid (headless‑ready).
2. Logs into TradingView using secure credentials stored in the environment.
3. Opens the chart for a specified asset and takes a snapshot.
4. Captures the URL and image source of that snapshot.
5. Updates an Airtable record with the image and reference link through the Airtable API.

The Flask server manages the webhook input and coordinates the entire process.

## Features

### Automated TradingView Charting
End‑to‑end navigation of TradingView, symbol search, snapshot capture, and retrieval of both the PNG URL and the page URL via Selenium WebDriver.

### Webhook‑Driven API
`/webhook_airtable` accepts JSON payloads—`asset`, `record_id`, `request_type`, &c.—so Airtable automations or third‑party services can request charts on demand.

### Airtable Integration
After capturing the chart image, the bot PATCHes the target record, attaching the file and its source URL—bridging TradingView visual data into your Airtable workspace.

### Flask Micro‑Server
Lightweight Flask app exposes the webhook plus diagnostics (`/info`, `/flask-health-check`, `/cache-me`).

## Environment Configuration

Create a `.env` file in your project root with:

```env
TRADING_VIEW_EMAIL=your_tradingview_email
TRADING_VIEW_PASSWORD=your_tradingview_password

AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_API_URL=https://api.airtable.com/v0/YOUR_BASE_ID/YOUR_TABLE_NAME   # combine base & table here

WEBHOOK_PASSPHRASE=your_webhook_passphrase
CHART_WEBHOOK_PASSPHRASE=your_chart_webhook_passphrase

REMOTE_ADDRESS=http://your-selenium-grid-address    # e.g. http://localhost
````

> **Note:** `AIRTABLE_BASE_ID` and `AIRTABLE_TABLE_NAME` were folded into the full `AIRTABLE_API_URL` for simplicity.
> If you prefer separate vars, update `airtable_api_request()` accordingly.

## Code Overview

### `selenium_chart(asset_name)`

Logs into TradingView, navigates to the chart for `asset_name`, takes a snapshot, and returns the page URL plus the PNG URL. Supports Selenium Grid and randomises the user‑agent.

### `airtable_api_request(api_url, data)`

PATCHes Airtable with the provided payload.

### Flask Endpoints

* `/` — root (“W!”)
* `/webhook_airtable` — main webhook
* `/cache-me` — Nginx cache test
* `/info` — request metadata
* `/flask-health-check` — simple health probe

## Dependencies

```bash
pip install -r requirements.txt
```

Core libs:

* selenium
* flask
* python‑dotenv
* fake‑useragent
* requests

You’ll also need a Selenium Grid (or local `chromedriver`) reachable at `REMOTE_ADDRESS`.

## Example Webhook Payload

```json
{
  "passphrase": "your_chart_webhook_passphrase",
  "record_id": "recXXXXXXXXXX",
  "asset": "AAPL",
  "request_type": "Daily Chart",
  "timeframe": "1D",
  "pattern": "Breakout"
}
```

The specified Airtable record will receive a new file attachment and a reference URL under the field named by `request_type`.
