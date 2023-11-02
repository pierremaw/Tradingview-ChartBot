## TradingView Chart Automation

https://github.com/pierremaw/Tradingview-Chart-Automation/assets/99075249/91d60aae-25ed-4c99-be22-1e917539c521

This automation bot:
1. Uses selenium to navigate to TradingView.
2. Accesses the chart for the asset specified via the parameter.
3. Takes a chart image snapshot.
4. Returns the chart image url and image source url.

This automation bot provides helper functions for a custom Airtable automation. The bot is hosted on a VPS and listens for webhooks from Airtable. Once a webhook is received, the bot parses the data, uses Selenium to navigate to TradingView, takes a snapshot, and then uploads the snapshot to Airtable via its API.

### Features
- **TradingView Automation**: Using Selenium to access, search, and capture snapshots of charts.
- **Airtable Integration**: After capturing the snapshot, the image and its URL will be saved into an Airtable base using the Airtable API.
- **Flask Application**: A simple Flask application is integrated to serve as an API endpoint for triggering the automation, among other utility routes.

### Prerequisites
- Python (>=3.6)
- An account on TradingView
- An Airtable base setup
- A `.env` file containing all necessary environment variables
- Selenium Grid
- VPS
- Docker
- Flask

### Environment Variables
Here's what you need in your `.env` file:

```env
TRADING_VIEW_EMAIL=your_tradingview_email
TRADING_VIEW_PASSWORD=your_tradingview_password
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_API_URL=your_airtable_api_url
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_NAME=your_airtable_table_name
WEBHOOK_PASSPHRASE=your_webhook_passphrase
CHART_WEBHOOK_PASSPHRASE=your_chart_webhook_passphrase
```

### Code Overview
#### **Selenium Chart Function (`selenium_chart`)**
- This function takes in an `asset_name` and returns a TradingView chart's snapshot and image URL.
- It signs into TradingView, navigates to the chart, searches for the asset, and takes a snapshot.
  
#### **Airtable API Request Function (`airtable_api_request`)**
- This function interacts with the Airtable API to update a specific record with the TradingView chart's snapshot and URL.
  
#### **Flask Application**
The Flask app serves a couple of routes for different purposes:
  - **`/`**: A basic home route.
  - **`/webhook_airtable`**: The main route that triggers the automation when received a POST request.
  - **`/cache-me`**: A testing route for Nginx caching.
  - **`/info`**: Returns details about the incoming request, like IPs and user-agents.
  - **`/flask-health-check`**: A health check route.

### Tip
To trigger the automation:

1. Send a POST request to `/webhook_airtable` with the required data.
2. The Flask app will process the request, capture the TradingView snapshot, and update the Airtable record.
