import os
from datetime import datetime as dt
from datetime import timedelta
from time import sleep
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

_ = load_dotenv("/.env")


class SeleniumTest():
    def __init__(self, site):

        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values.automatic_downloads': 1,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
        }
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--lang=en")

        print('>         CONNECTING...')
        
        self.site = site
        self.browser = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=chrome_options
        )
        
        print('<         CONNECTED')
        
        self.browser.maximize_window()
        self.browser.get(self.site)
        
    def get_driver(self):
        return self.browser

    def find_by_id(self, id):
        return self.browser.find_element(by=By.ID, value=id)

    def find_by_name(self, name):
        return self.browser.find_element(by=By.NAME, value=name)
    
    def find_by_class(self, name):
        return self.browser.find_element(by=By.CLASS_NAME, value=name)
    
    def find_mult_by_class(self, name):
        items = self.browser.find_elements(by=By.CLASS_NAME, value=name)
        return items
    
    def find_by_xpath(self, xpath):
        return self.browser.find_elements(by=By.XPATH, value=xpath)
                
    def login(self, username, password):
        try:
            inputElement = self.find_by_name("user")
            inputElement.send_keys(username)

            inputElement = self.find_by_name('password')
            inputElement.send_keys(password)
            
            inputElement.send_keys(Keys.ENTER)
            
        except Exception as e:
            raise Exception({'method': 'login', 'error': e})

        
if __name__ == '__main__':
    site = "https://www.asigbo.org/"
    user = "diego.morales.aquino@gmail.com"
    password = "12345678"
    download = SeleniumTest(site)
    sleep(10)
    
    try:
        download.login(user, password)
    except Exception as e:
        print(e)
        
    sleep(10)
