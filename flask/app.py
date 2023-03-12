'''
Packages
'''
import time
from datetime import datetime
import requests
import json
import config as config
import os

'''
Environment Variables
'''
from dotenv import load_dotenv
load_dotenv()

'''
Selenium Imports
'''
from selenium import webdriver
from selenium.webdriver import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from flask import Flask, request, jsonify

from pybit import HTTP


########## Flask App ######################
app = Flask(__name__)
####################### Functions #######################

def selenium_home():
    pass
    return 

def selenium_trading(asset_name):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Remote(command_executor=f"{os.environ.get('VPS_HTTP')}:4444",options=chrome_options)
    
    driver.get(os.environ.get('TRADINGVIEW_SIGN_IN_HTTP'))
    wait=WebDriverWait(driver, timeout=10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='username']"))).send_keys(os.environ.get('TRADINGVIEW_EMAIL'))
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(f"{os.environ.get('TRADINGVIEW_PASSWORD')}" + Keys.RETURN)
    
    # Wait for TradingView
    time.sleep(5)

    trading_view_chart_page = False
    while not trading_view_chart_page :
        driver.get(os.environ.get('TRADINGVIEW_CHART_HTTP'))
        time.sleep(5)
        symbol_search = driver.find_element(By.XPATH, "//div[@title='Symbol Search' and @data-role='button']")    
        if symbol_search != []:
            trading_view_chart_page = True
            break

    symbol_search_visible = False 
    symbol_searched_for = False
    while not symbol_search_visible and not symbol_searched_for:
        symbol_search = driver.find_element(By.XPATH, "//div[@title='Symbol Search' and @data-role='button']")
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
            take_a_snapshot =  driver.find_elements(By.XPATH, "//div[@title='Take a snapshot']")    

            if take_a_snapshot != []:
                symbol_searched_for = True

    # Take a snapshot 
    new_tab_opened = False
    while not new_tab_opened:
        take_a_snapshot =  driver.find_elements(By.XPATH, "//div[@title='Take a snapshot']")
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

def airtable_api_request(api_url, data):
    '''API request'''
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.environ.get('AIRTABLE_API_KEY')}"
        }
    
    requests.patch(api_url, headers=headers, json=data)
    return True

####################### Flask Routes #######################

@app.route('/')
def hello():
    try:
        title = selenium_home()
        return f'Hello World! I have seen {title}.'

    except Exception as e:
        print(e.message)
        return f'{e.message}'

@app.route('/webhook_airtable', methods=['POST'])
def webhook_airtable():

    webhook_data = json.loads(request.data)
    if webhook_data['passphrase'] != os.environ.get('PASSPHRASE_WEBHOOK_AIRTABLE_TRADINGVIEW'):
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

    api_url = os.environ.get('AIRTABLE_SETUPS_TABLE_HTTP')

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

@app.route('/bybit_balance', methods=['POST'])
def bybit_balance():

    data = json.loads(request.data)
    if data['passphrase'] != os.environ.get('PASSPHRASE_WEBHOOK_AIRTABLE_BYBIT_DERIVS'):
        return {
            "code": "error",
            "message": "Invalid passphrase"
        }
    record_id = data['record_id']
    balance_field = data['request_type']
        
    #Get Wallet Balance
    session = HTTP(
        endpoint = 'https://api.bybit.com/',
        api_key = os.environ.get('BYBIT_API_KEY'),
        api_secret = os.environ.get('BYBIT_SECRET_KEY')
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
    
    api_url = os.environ.get('AIRTABLE_JOURNAL_TABLE_HTTP')
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

@app.route('/cache-me')
def cache():
	return "nginx will cache this response"

@app.route('/info')
def info():

	resp = {
		'connecting_ip': request.headers['X-Real-IP'],
		'proxy_ip': request.headers['X-Forwarded-For'],
		'host': request.headers['Host'],
		'user-agent': request.headers['User-Agent']
	}

	return jsonify(resp)

@app.route('/flask-health-check')
def flask_health_check():
	return "success"
