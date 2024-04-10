from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
@app.route('/api', methods=['POST', 'OPTIONS'])
def print_name():
    print(request)
    if request.is_json:
        data = request.json
        
        if 'name' in data:
            name = data['name']
            print(name)
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                # service = Service(executable_path="chromedriver.exe")
                # driver = webdriver.Chrome(service=service)
                driver.get("https://www.rayware.co.uk/")
                element = WebDriverWait(driver, 0).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/header/div[2]/div[3]/div/form/div/label/span"))
                )
                # element = driver.find_element(By.XPATH, "/html/body/div[4]/header/div[2]/div[3]/div/form/div/label/span")
                element.click()
                input_element = driver.find_element(By.XPATH, "/html/body/div[4]/header/div[2]/div[3]/div/form/div/div/input")
                input_element.send_keys(name, Keys.ENTER)
                time.sleep(5)
                cookie_banner = driver.find_elements(By.CLASS_NAME, 'cc-window')
                if cookie_banner:
                    driver.execute_script("arguments[0].style.display = 'none';", cookie_banner[0])

                new = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'product-item-link')))
                new.click()
                description = driver.find_element(By.XPATH,"/html/body/div[5]/main/div[2]/div/div[3]/div/div[2]/div/div")
                print(description.text)
                time.sleep(10)
                print("Element found")
                return jsonify({'message': description.text})
            except Exception as e:
                print("Error:", e)
            print("Received name:", name)
        else:
            print("No name field found in JSON data")
            return jsonify({'error': 'No name field found in JSON data'}), 400
    else:
        print("Request must contain JSON data")
        return jsonify({'error': 'Request must contain JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
