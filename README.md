# TradingView ChartBot: Personal Project for Automating Market Visuals with Airtable Integration

# TradingView ChartBot: Automated Market Chart Snapshots with Airtable Integration

TradingView ChartBot is a Python-based microservice that automatically captures real-time chart snapshots from TradingView and updates them to Airtable using webhooks. Built with Selenium and Flask, it runs on a remote server, listens for asset data, and delivers high-resolution images of live charts directly into structured Airtable records.

I created this project to explore automated financial data visualization, practice full-stack Python development, and demonstrate how to bridge dynamic websites with no-code platforms. It reflects my experience in browser automation, API integration, and building scalable backend services with secure environment management.




**TradingView ChartBot** is a Flask-based microservice that automatically generates chart snapshots from TradingView and updates them in Airtable through webhook triggers. I built this tool to explore automated market monitoring, deepen my experience with Selenium, and demonstrate how Python scripts can bridge dynamic web interfaces with no-code platforms like Airtable.

By combining real-time chart capture with structured record updates, this bot acts as a lightweight charting engine that can plug into personal dashboards, market research tools, or workflow automations. The service is deployed on a VPS and operates entirely from webhook input—no manual interaction required after setup.

This project reflects my proficiency in:

- Using Selenium to control browser behavior for authenticated sites
- Creating and managing Flask APIs
- Handling secure credential storage with dotenv
- Structuring modular Python code for automation
- Integrating with external APIs (in this case, Airtable)
- Deploying code to a remote environment using Docker and environment variables

The rest of this README details how the system works, how to run it locally or on a VPS, and how it can be extended or integrated with other platforms.

## How It Works

When triggered by a webhook, the bot executes the following steps:

1. Launches a browser session through Selenium Grid.
2. Logs into TradingView using secure credentials stored in the environment.
3. Opens the chart for a specified asset and takes a snapshot.
4. Captures the URL and image source of the chart snapshot.
5. Updates an Airtable record using the Airtable API, attaching the image and reference URL.

The Flask server manages the webhook input and coordinates the entire process.

## Features

### Automated TradingView Charting

This tool automates the end-to-end process of navigating TradingView, searching for an asset, and capturing a chart snapshot using Selenium WebDriver. The snapshot is accessed via a newly opened tab and returned as both a URL and image source.

### Webhook-Driven API

The Flask application exposes a `/webhook_airtable` POST route that accepts JSON payloads with details like `asset`, `record_id`, and `request_type`. This allows other services, such as Airtable automations or third-party systems, to trigger chart captures on demand.

### Airtable Integration

After capturing the chart image, the bot sends a PATCH request to Airtable, updating the record with the image file and a reference link. This setup allows the bot to act as a bridge between TradingView visual data and your Airtable workspace.

### Flask API Server

The project is built around a Flask server that listens for incoming webhooks and also offers diagnostic endpoints for debugging and health monitoring.

## Environment Configuration

Create a `.env` file in your project root with the following variables:

```env
TRADING_VIEW_EMAIL=your_tradingview_email
TRADING_VIEW_PASSWORD=your_tradingview_password

AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_API_URL=your_airtable_api_url
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_NAME=your_airtable_table_name

WEBHOOK_PASSPHRASE=your_webhook_passphrase
CHART_WEBHOOK_PASSPHRASE=your_chart_webhook_passphrase
REMOTE_ADDRESS=http://your-selenium-grid-address
````

These environment variables are loaded at runtime and are critical for authentication and routing.

## Code Overview

### `selenium_chart(asset_name)`

Logs into TradingView, navigates to the chart for the given asset, takes a snapshot, and returns both the image URL and the image source. This function uses a randomized user agent and supports Selenium Grid execution.

### `airtable_api_request(api_url, data)`

Wraps a PATCH request to update a record in Airtable with the provided JSON `data`. The headers are configured using your Airtable API key.

### Flask Endpoints

* `/`: Basic root endpoint returning `"W!"`.
* `/webhook_airtable`: Accepts a POST request and triggers the full chart capture and Airtable update.
* `/cache-me`: Dummy route for testing Nginx cache behavior.
* `/info`: Shows request metadata such as headers, host, and IP.
* `/flask-health-check`: Health check endpoint returning a simple success string.

## Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

Key dependencies include:

* selenium
* flask
* python-dotenv
* fake\_useragent
* requests

Ensure you also have a Selenium Grid setup and Chrome WebDriver accessible through the address specified in `REMOTE_ADDRESS`.

## Example Webhook Payload

To trigger the automation, send a POST request to `/webhook_airtable` with the following JSON structure:

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

The record in Airtable will be updated with a file upload and a URL in the field named by `request_type`.

## Deployment

You can run the application on any VPS with Python 3.6 or newer. Docker support is recommended for production use. Ensure your Selenium Grid is also running in the environment, either locally or remotely.
