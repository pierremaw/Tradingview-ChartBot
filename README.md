# TradingView Chart Automation

[https://github.com/user-attachments/assets/6538c9c2-16e4-433c-b9ef-e02d0ad08e13](https://github.com/user-attachments/assets/6538c9c2-16e4-433c-b9ef-e02d0ad08e13)

**TradingView Chart Automation** is a streamlined Python microservice that automates the capture of TradingView chart snapshots and delivers them directly into Airtable records via webhooks. This system leverages Flask for API handling, Selenium for browser automation, and Docker for remote deployment. Designed for real-time use, the service makes it easy to visualize and archive financial chart data in a structured and centralized workspace.

This project served as a practical deep dive into full-stack Python development. It provided hands-on experience with secure environment configuration, authenticated web automation, and API-driven workflows. The microservice is compact, single-file, and containerized for ease of deployment and maintenance on remote servers.

## Overview

When triggered by an incoming webhook, the service performs a sequence of actions:

* Launches a Selenium browser session using a remote Selenium Grid (headless-compatible).
* Authenticates with TradingView using securely stored credentials.
* Opens a specified asset chart and captures a PNG snapshot.
* Extracts the image and page URLs of the snapshot.
* Sends the image and metadata to Airtable, updating the specified record.

The Flask server exposes a public webhook endpoint that accepts chart generation requests and orchestrates all these steps automatically.

## Features

### TradingView Chart Automation

This service automates the full lifecycle of chart capture, including symbol lookup, visual rendering, and image extraction from TradingView. It retrieves both the direct PNG file and the corresponding chart page URL using Selenium WebDriver.

### Webhook-Based API

The `/webhook_airtable` endpoint listens for JSON payloads containing fields such as `asset`, `record_id`, and `request_type`. This enables seamless integration with Airtable automations or third-party systems that need on-demand chart generation.

### Airtable Integration

After capturing the chart snapshot, the service PATCHes the target record in Airtable using the Airtable API. It attaches the chart image and inserts a link back to TradingView, keeping your Airtable database visually enriched and up to date.

### Lightweight Flask Server

The service is built on Flask and includes several endpoints for diagnostics and system health:

* `/webhook_airtable`: Accepts chart generation requests.
* `/info`: Provides request metadata for debugging.
* `/flask-health-check`: Simple liveness probe for monitoring.
* `/cache-me`: Used to test Nginx or browser caching layers.
* `/`: Root endpoint.

## Environment Configuration

To run the service, create a `.env` file in the project root with your credentials and configuration:

```env
TRADING_VIEW_EMAIL=your_tradingview_email
TRADING_VIEW_PASSWORD=your_tradingview_password

AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_API_URL=https://api.airtable.com/v0/YOUR_BASE_ID/YOUR_TABLE_NAME

WEBHOOK_PASSPHRASE=your_webhook_passphrase
CHART_WEBHOOK_PASSPHRASE=your_chart_webhook_passphrase

REMOTE_ADDRESS=http://your-selenium-grid-address
```

These environment variables manage authentication and connectivity. Use `dotenv` to load them securely during execution.

## Core Logic

### `selenium_chart(asset_name)`

This function initiates a Selenium browser session, logs into TradingView, opens the chart for the specified `asset_name`, captures a snapshot, and returns both the page URL and the image URL. It supports Selenium Grid and randomizes the user agent for robustness.

### `airtable_api_request(api_url, data)`

This function sends a PATCH request to the Airtable API, updating the designated record with the chart image and its metadata.

### Flask Endpoints

```python
@app.route('/')
def root():
    return 'Service is running.'

@app.route('/webhook_airtable', methods=['POST'])
def webhook_airtable():
    # Main webhook logic here
    pass

@app.route('/cache-me')
def cache_me():
    return 'Cache test successful.'

@app.route('/info')
def info():
    return request.headers

@app.route('/flask-health-check')
def health_check():
    return 'OK'
```

These routes define the main entry point and diagnostic endpoints for the Flask server.

## Dependencies

Install the required Python libraries using:

```bash
pip install -r requirements.txt
```

The core dependencies include:

* `selenium`: For browser automation
* `flask`: For building the API server
* `python-dotenv`: For loading environment variables
* `fake-useragent`: To spoof browser fingerprints
* `requests`: For API communication with Airtable

## Example Webhook Payload

Here’s a sample JSON body for a webhook request:

```json
{
  "passphrase": "your_chart_webhook_passphrase",
  "record_id": "recXXXXXXXXXX",
  "asset": "AAPL",
  "request_type": "Daily Chart",
  "timeframe": "1D",
  "pattern": "Flag"
}
```

The service will use this payload to navigate to the specified asset’s chart, take a snapshot, and update the corresponding Airtable record with the new image and chart link.
