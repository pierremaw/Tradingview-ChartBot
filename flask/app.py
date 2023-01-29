
import time
from datetime import datetime
import requests
import pyperclip
import json
import config as config

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
# from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from flask import Flask, request, jsonify

####################### Environment Variables #######################
airtable_api_key = 'pat48T3AqL1nq9OK0.8916dff7d59b8e2b2db3bdaf26cf9a88f3ee94e7bf02de7231d1e3f48c6d11ad'
trading_view_email = "pierre.maw@gmail.com"
trading_view_password = "aKoZgT9UTN9mRiZ2xpiM"

airtable_base_id = 'appkfyJCQlrzAluvw'
airtable_table_name = 'tbl6MlOcqL99B445n'

remote_address = 'http://5.161.52.144'

########## Flask App ######################
app = Flask(__name__)

####################### Functions #######################

def selenium_home():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Remote(command_executor=f'{remote_address}:4444',options=chrome_options)
    
    driver.get('https://www.google.com')
    driver.get('https://www.python.org')
    title = driver.title
    driver.close()
    driver.quit()
    return title

def selenium_trading(asset_name):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--start-fullscreen')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Remote(command_executor=f'{remote_address}:4444',options=chrome_options)
    
    try:
        driver.get('https://www.tradingview.com/#signin')
        wait=WebDriverWait(driver, timeout=10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='username']"))).send_keys(trading_view_email)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(f"{trading_view_password}" + Keys.RETURN)
        # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='password']"))).send_keys(trading_view_password)
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(., 'Sign in')]]"))).click()
        
        #wait for tradingview homepage to load
        time.sleep(5)
        # navigate to the tradingview chart page
        driver.get("https://www.tradingview.com/chart/6l6q6Oh0")
        time.sleep(5)
        # We need to ensure that we are on the correct page for a given asset
        # We can do this by inputing the asset name using key strokes. 

        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        actions.send_keys("@")
        actions.send_keys(Keys.BACKSPACE)
        actions.send_keys(asset_name)
        actions.perform()
        time.sleep(2)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(8)
        # Take a snapshot 
        wait = WebDriverWait(driver, 40)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='header-toolbar-screenshot' and @data-role='button']")))
        ######################################################################### seems to be working
        actions.key_down(Keys.ALT).key_down('s').key_up(Keys.ALT).key_up('s').perform()
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Take a snapshot' and @data-role='button']"))).click()
        time.sleep(5)
        
        # time.sleep(1)
        driver.execute_script("window.open('');")

        trading_view_chart_image_url = 'https://www.tradingview.com/x/iUcOPe96/'
        
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.get(trading_view_chart_image_url)
        image_source_url = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='TradingView Chart']"))).get_attribute("src")
        
        trading_view_chart_image_url = driver.current_url()

        driver.close()
        driver.quit()

        return trading_view_chart_image_url, image_source_url

    except Exception as e:
        print (e)


    driver.close()
    driver.quit()
    return trading_view_chart_image_url, image_source_url

def add_data(data, record_id):
    """Add scores to the Airtable."""
    
    api_url = 'https://api.airtable.com/v0/appkfyJCQlrzAluvw/tbl6MlOcqL99B445n/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {airtable_api_key}'
        }
    
    response = requests.patch(api_url, headers=headers, json=data)
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

    data = json.loads(request.data)
    if data['passphrase'] != config.CHART_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Invalid passphrase"
        }
    record_id = data['record_id']
    asset_name = data['asset']
    time_stamp = datetime.today().strftime('%Y-%m-%d')

    # call the take_screenshot function
    screenshot = selenium_trading(asset_name)
    
    print(screenshot)

    data = {"records": 
    [
        {"id": record_id,
            "fields": {
            "Chart Link": f"{screenshot}", #screenshot[0]
            "Chart": [{
                "url": "test", #screenshot[1]
                "filename": f'[{time_stamp}] {asset_name}.png'
                }]
            }
        },
    ]
    }
    # data = {"records": 
    # [
    #     {"id": record_id,
    #         "fields": {
    #         "Chart Link": screenshot[0],
    #         "Chart": [{
    #             "url": screenshot[1],
    #             "filename": f'[{time_stamp}] {asset_name}.png'
    #             }]
    #         }
    #     },
    # ]
    # }
    airtable_response = add_data(data, record_id)

    if airtable_response:
        return {
            "code": "success",
            "message": "Airtable record updated successfully"
        }
    else:
        return {
            "code": "error",
            "message": "Airtable record update failed",
            "airtable response": f'{airtable_response}'
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
