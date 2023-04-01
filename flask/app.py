'''
IMPORTS
'''
import time
from datetime import datetime
import requests
import json
import config as config

'''
SELENIUM
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from fake_useragent import UserAgent

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
FLASK
'''
from flask import Flask, request, jsonify

'''
BYBIT
'''
from pybit import HTTP
bybit_api_key = "nkWOnzfGIJBpjwOKiX"
bybit_secret_key = "W7sMJ0LRwEwGl3JNOj0aqo2UG7tdasRPgY16"

'''
TRADINGVIEW
'''
trading_view_email = "pierre.maw@gmail.com"
trading_view_password = "aKoZgT9UTN9mRiZ2xpiM"

airtable_api_key = 'pat48T3AqL1nq9OK0.8916dff7d59b8e2b2db3bdaf26cf9a88f3ee94e7bf02de7231d1e3f48c6d11ad'
airtable_base_id = 'appkfyJCQlrzAluvw'
airtable_table_name = 'tbl6MlOcqL99B445n'

'''
VPS ADDRESS
'''
remote_address = 'http://5.161.52.144'

'''
FLASK APP
'''
app = Flask(__name__)


'''
AIRTABLE -> VPS -> TRADINGVIEW
'''
def selenium_trading(asset_name):

    '''CHROME OPTIONS'''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    
    '''USER AGENT'''
    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument(f'user-agent={userAgent}')
    
    '''SETUP DRIVER'''
    driver = webdriver.Remote(command_executor=f'{remote_address}:4444',options=chrome_options)
    
    '''ACCESS TRADINGVIEW'''
    driver.get('https://www.tradingview.com/#signin')
    time.sleep(1)
    wait=WebDriverWait(driver, timeout=10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='username']"))).send_keys(trading_view_email)
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(f"{trading_view_password}" + Keys.RETURN)
    # Wait for TradingView
    time.sleep(5)

    '''ACCESS TRADINGVIEW CHART AND WAIT FOR SYMBOL SEARCH'''
    trading_view_chart_page = False
    while not trading_view_chart_page :
        driver.get("https://www.tradingview.com/chart/6l6q6Oh0")
        time.sleep(5)
        symbol_search = driver.find_element(By.XPATH, "//*[@id='header-toolbar-symbol-search']")
        if symbol_search != []:
            trading_view_chart_page = True
            break
    
    '''SEARCH FOR SYMBOL'''
    symbol_search_visible = False 
    symbol_searched_for = False
    while not symbol_search_visible and not symbol_searched_for:
        symbol_search = driver.find_element(By.XPATH, "//*[@id='header-toolbar-symbol-search']")
        driver.execute_script("arguments[0].click();", symbol_search)
        time.sleep(3)
        search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        if search_bar != []:
            symbol_search_visible = True
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
            search_bar.clear()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))).send_keys(asset_name)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))).send_keys(Keys.ENTER)
            time.sleep(5)
            take_a_snapshot = driver.find_elements(By.XPATH, "//button[@type='button'][@data-tooltip='Take a snapshot'][@aria-label='Take a snapshot']")

            if take_a_snapshot != []:
                symbol_searched_for = True

    '''TAKE A SNAPSHOT AND OPEN IMAGE IN NEW TAB'''
    new_tab_opened = False
    while not new_tab_opened:
        take_a_snapshot = driver.find_elements(By.XPATH, "//button[@type='button'][@data-tooltip='Take a snapshot'][@aria-label='Take a snapshot']")
        open_image_in_new_tab = driver.find_elements(By.XPATH, "//span[text()='Open image in new tab']")
        
        for element in take_a_snapshot:

            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            open_image_in_new_tab = driver.find_element(By.XPATH, "//span[text()='Open image in new tab']")
            if open_image_in_new_tab != []:
                open_image_in_new_tab = driver.find_element(By.XPATH, "//span[text()='Open image in new tab']")
                driver.execute_script("arguments[0].click();", open_image_in_new_tab)
                new_tab_opened = True
                break
 
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    trading_view_chart_image_url = driver.current_url
    image_source_url = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='TradingView Chart']"))).get_attribute("src")
    
    driver.close()
    driver.quit()

    return trading_view_chart_image_url, image_source_url

'''
AIRTABLE API REQUEST
'''
def airtable_api_request(api_url, data):
    """API request."""
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {airtable_api_key}'
        }
    
    requests.patch(api_url, headers=headers, json=data)
    return True



'''
FLASK APP ROUTES
'''

'''
HOME PAGE
'''
@app.route('/')
def hello():
    
    return 'W!'

'''
WEBHOOK AIRTABLE
'''
@app.route('/webhook_airtable', methods=['POST'])
def webhook_airtable():

    webhook_data = json.loads(request.data)
    if webhook_data['passphrase'] != config.CHART_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Invalid passphrase"
        }
    record_id = webhook_data['record_id']
    asset_name = webhook_data['asset']
    chart_request_type = webhook_data['request_type']
    time_stamp = datetime.today().strftime('%Y-%m-%d')

    # call the selenium webdriver function
    tradingview_chart_data = selenium_trading(asset_name)

    data = {"records": 
    [
        {"id": record_id,
            "fields": {
            f"{chart_request_type} Reference": tradingview_chart_data[0],
            f"{chart_request_type}": [{
                "url": tradingview_chart_data[1],
                "filename": f"[{time_stamp}] {asset_name} {chart_request_type}.png"
                }]
            }
        },
    ]
    }

    airtable_table = 'tbl6MlOcqL99B445n' # Trading Viw Setups Table
    api_url = f'https://api.airtable.com/v0/appkfyJCQlrzAluvw/{airtable_table}/'
    api_response = airtable_api_request(api_url, data)

    if api_response:
        return {
            "code": "success",
            "message": "Airtable record updated successfully"
        }
    else:
        return {
            "code": "error",
            "message": "Airtable record update failed",
            "airtable response": f'{api_response}'
        }

'''
BYBIT BALANCE
'''
@app.route('/bybit_balance', methods=['POST'])
def bybit_balance():

    data = json.loads(request.data)
    if data['passphrase'] != config.CHART_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Invalid passphrase"
        }
    record_id = data['record_id']
    balance_field = data['request_type']
        
    #Get Wallet Balance
    session = HTTP(
        endpoint = 'https://api.bybit.com/',
        api_key = bybit_api_key,
        api_secret = bybit_secret_key
    )

    balance_request = session.get_wallet_balance(coin="USDT")
    balance = balance_request["result"]["USDT"]["wallet_balance"]

    data = {"records": 
    [
        {"id": record_id,
            "fields": {
            f"{balance_field}": balance,
            }
        },
    ]
    }
    
    airtable_table = 'tblsdUW4vxAB7molM' # Trading Journal Table
    api_url = f'https://api.airtable.com/v0/appkfyJCQlrzAluvw/{airtable_table}/'
    api_response = airtable_api_request(api_url, data)

    if api_response:
        return {
            "code": "success",
            "message": "Airtable record updated successfully"
        }
    else:
        return {
            "code": "error",
            "message": "Airtable record update failed",
            "airtable response": f'{api_response}'
        }

'''
NGINX CACHE'''
@app.route('/cache-me')
def cache():
	return "nginx will cache this response"

'''
FLASK INFO
'''
@app.route('/info')
def info():

	resp = {
		'connecting_ip': request.headers['X-Real-IP'],
		'proxy_ip': request.headers['X-Forwarded-For'],
		'host': request.headers['Host'],
		'user-agent': request.headers['User-Agent']
	}

	return jsonify(resp)

'''
FLASK HEALTH CHECK
'''
@app.route('/flask-health-check')
def flask_health_check():
	return "success"
