# TradingView Chart Capture Automation

A streamlined automation service that captures live TradingView chart snapshots and syncs them with Airtable. Powered by Selenium, Flask, and Docker, this bot listens for webhooks and delivers high-resolution chart images directly to your Airtable base.

## Overview

This automation bot performs end-to-end chart image generation and Airtable integration. Once it receives a webhook, it:

1. Logs into TradingView using Selenium.
2. Navigates to the specified asset's chart.
3. Captures a snapshot of the chart.
4. Uploads the image and its URL to a designated Airtable record.

Hosted on a VPS and wrapped in a Flask app, this service enables chart-driven workflows and custom data pipelines.

## Key Features

### 🔍 TradingView Automation
Automates login, chart navigation, and snapshot generation on TradingView using Selenium. Ideal for generating visual reports or monitoring market movements.

### 📦 Airtable Integration
Automatically uploads chart images and links to your Airtable base using the Airtable API. Supports dynamic record updates based on webhook payloads.

### 🌐 Flask API Service
A lightweight Flask server handles incoming webhooks, manages requests, and routes various utility functions.

## Prerequisites

To deploy and run the automation, ensure the following:

- Python ≥ 3.6
- A TradingView account
- Airtable account with a base and API access
- A VPS (virtual private server)
- Docker and Docker Compose
- Selenium Grid (or a compatible WebDriver setup)
- A `.env` file with required environment variables

## Environment Variables

Your `.env` file should include:

```env
TRADING_VIEW_EMAIL=your_tradingview_email
TRADING_VIEW_PASSWORD=your_tradingview_password
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_API_URL=your_airtable_api_url
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_NAME=your_airtable_table_name
WEBHOOK_PASSPHRASE=your_webhook_passphrase
CHART_WEBHOOK_PASSPHRASE=your_chart_webhook_passphrase
````

## Code Architecture

### `selenium_chart(asset_name)`

Logs into TradingView, searches for the specified asset, captures a chart snapshot, and returns both the image URL and the image source.

### `airtable_api_request(image_url, image_src)`

Sends a PATCH request to Airtable to update a record with the chart image and metadata.

### Flask Routes

* `/`: Root route for health confirmation.
* `/webhook_airtable`: Receives POST requests from Airtable and triggers the automation workflow.
* `/cache-me`: A test endpoint for validating Nginx or proxy caching.
* `/info`: Debug endpoint showing request metadata.
* `/flask-health-check`: Health check route used for monitoring.

## Triggering the Automation

To initiate a snapshot and Airtable update:

1. Send a `POST` request to `/webhook_airtable` with the required JSON payload.
2. The bot authenticates with TradingView, captures the chart image, and updates your Airtable record.

## License

MIT License

