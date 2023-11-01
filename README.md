## TradingView Chart Automation

https://github.com/pierremaw/Tradingview-Chart-Automation/assets/99075249/91d60aae-25ed-4c99-be22-1e917539c521

This Python bot provides helper functions for Airtable automation. The bot is hosted on a VPS and listens for webhooks from Airtable. Once a webhook is received, the bot parses the data, uses Selenium Grid to navigate to TradingView, takes a snapshot, and then uploads the snapshot to Airtable via its API.


### Process Overview
1. Alert to Airtable: Alerts from TradingView are sent and stored in the Airtable base "TradingView Setups".
2. Automation and Webhook: Post storage, Airtable automation scripts send a JSON webhook to a VPS.
3. VPS Processing: VPS listens for the webhook and processes it using the bot from this repository.

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
- Docker

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
- **Selenium Chart Function (`selenium_chart`)**:
  - This function takes in an `asset_name` and returns a TradingView chart's snapshot and image URL.
  - It signs into TradingView, navigates to the chart, searches for the asset, and takes a snapshot.
  
- **Airtable API Request Function (`airtable_api_request`)**:
  - This function interacts with the Airtable API to update a specific record with the TradingView chart's snapshot and URL.
  
- **Flask Application**:
  - The Flask app serves a couple of routes for different purposes:
    - **`/`**: A basic home route.
    - **`/webhook_airtable`**: The main route that triggers the automation when received a POST request.
    - **`/cache-me`**: A testing route for Nginx caching.
    - **`/info`**: Returns details about the incoming request, like IPs and user-agents.
    - **`/flask-health-check`**: A health check route.

### Setup & Run
1. Clone this repository.
2. Navigate to the cloned directory.
3. Install the required packages: `pip install -r requirements.txt`.
4. Ensure you've set up the `.env` file correctly.
5. Run the Flask app: `python app.py`.
6. Now, the application will be running and waiting for incoming requests.

### Usage
To trigger the automation:

1. Send a POST request to `/webhook_airtable` with the required data.
2. The Flask app will process the request, capture the TradingView snapshot, and update the Airtable record.

### Tip
This repo incorporates Docker for consistent environment deployment and Selenium Grid for parallel browser interactions. Docker ensures smooth deployment across platforms, while Selenium Grid enhances efficiency by handling multiple sessions simultaneously.

