from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import os
import argparse
import pyotp

parser = argparse.ArgumentParser(description='Selenium Website Monitor')
parser.add_argument("-f", "--findme", default="", help="text to find on page")
parser.add_argument("-u", "--user", default="", help="specify a username to log in with")
parser.add_argument("-l", "--url", default="", help="specify a url to log in with")
parser.add_argument("-p", "--passw", default="", help="specify a password for the username")
parser.add_argument("-o", "--otp", default="", help="Please supply your otp hash")
args = parser.parse_args()

# populate our variables
url = args.url
findme = args.findme
user_name = args.user
pass_word = args.passw
exceptioncount = 0
web_timeout = 30
totp = pyotp.TOTP(args.otp)

# modify otp URL
otp_url = url + "/otp"

# set the chrome driver options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x1400")
chrome_options.add_argument("--no-sandbox")
chrome_driver = os.path.join(os.getcwd(), "chromedriver.exe")

# load the chrome driver
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.set_page_load_timeout(web_timeout)

try:
    driver.get(url)
    time.sleep(5)
except TimeoutException:
    exceptioncount = exceptioncount + 1
    print("2")

if exceptioncount > 0:
    driver.quit()
    exit(1)
else:
    try:
        driver.find_element_by_id("Email").send_keys(user_name)
        driver.find_element_by_id("Password").send_keys(pass_word)
        driver.find_element_by_class_name("submit-button").click()

        # MFA Verification
        driver.get(otp_url)
        driver.find_element_by_id("Code").send_keys(totp.now())
        driver.find_element_by_class_name("submit-button").click()
    except:
        exceptioncount = exceptioncount + 1
        print("5")

try:
    driver.get('https://'+ url + '/gobeyond/landing/page')
except TimeoutException:
    exceptioncount = exceptioncount + 1
    # print(TimeoutException)
    print("3")

# Wait seconds for page to load
if exceptioncount > 0:
    driver.quit()
    exit(2)
else:
    time.sleep(5)
    name = driver.page_source
    if findme in name:
        print("0")
    else:
        print("4")

driver.quit()