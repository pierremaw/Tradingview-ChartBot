## TradingView to Airtable Automation

This repository contains a Python-based automation tool designed to provide helper functions for automation processes in Airtable, specifically when there are alerts from TradingView.

### Process Overview:

1. **TradingView Alert**: When an alert is triggered in TradingView, the information is transmitted directly to an Airtable base.
2. **Airtable Storage**: The transmitted information from TradingView is stored in the Airtable base named "Trading View Setups". Each TradingView alert translates to a unique record in this base.
3. **Airtable Automation**: After storing the alert information, Airtable runs a set of automation scripts. One of these scripts is responsible for sending a JSON-formatted webhook to a Virtual Private Server (VPS).
4. **VPS Reception**: The VPS, which runs the server-side script from this repository, listens for and processes the webhook transmitted by Airtable.

### Features:

- **TradingView Automation**: Using Selenium to access, search, and capture snapshots of charts.
- **Airtable Integration**: After capturing the snapshot, the image and its URL will be saved into an Airtable base using the Airtable API.
- **Flask Application**: A simple Flask application is integrated to serve as an API endpoint for triggering the automation, among other utility routes.

### Prerequisites:

1. Python (>=3.6)
2. An account on TradingView.
3. An Airtable base setup.
4. A `.env` file containing all necessary environment variables.

### Environment Variables:

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

### Code Overview:

- **Selenium Trading Function (`selenium_trading`)**:
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

### Setup & Run:

1. Clone this repository.
2. Navigate to the cloned directory.
3. Install the required packages: `pip install -r requirements.txt`
4. Ensure you've set up the `.env` file correctly.
5. Run the Flask app: `python filename.py`
6. Now, the application will be running and waiting for incoming requests.

### Usage:

To trigger the automation:

1. Send a POST request to `/webhook_airtable` with the required data.
2. The Flask app will process the request, capture the TradingView snapshot, and update the Airtable record.

### Tip:

Ensure that your environment can handle multiple instances of the web driver if there will be concurrent requests to this tool. You may need to set up a grid or use a cloud-based Selenium solution for better scalability.
