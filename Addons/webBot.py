from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def createWebBrowserOptions(headless=False):
    options = webdriver.ChromeOptions()
    if(headless == True):
        options.add_argument("--headless") # Runs Chrome in headless mode. (No UI)
    return options

def webBrowserInit(options = None):
    # Setup the browser and wait for it to be ready
    if (options is not None):
            driver = webdriver.Chrome(options=options)  # Chrome because some boxes does not content IDs in other browsers
    else:
        driver = webdriver.Chrome()  # Chrome because some boxes does not content IDs in other browsers
    return driver

def loadLoginInfo():
    global username,password
    # Description: This script logs into the GFN Lernplattform and prints the content of the loaded page.
    # Read credentials from the JSON file
    with open('./credentials.json') as f:
        credentials = json.load(f)

    # Extract username and password from credentials
    username = credentials['username']
    password = credentials['password']

def logInGFN(driver): # Returns True wenn eingeloggt, False wenn nicht.
    # Load the login page
    login_url = 'https://lernplattform.gfn.de/login/index.php'
    driver.get(login_url)

    # Find the username and password input fields and submit button
    # Wait for the username input box to be present
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    ).send_keys(username)
    # Wait for the password input box to be present
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    ).send_keys(password)
    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'loginbtn'))
    ).click()

    driver.get("https://lernplattform.gfn.de/grade/report/overview/index.php")
    # Wait for the page to load (you may need to adjust the wait time)
    driver.implicitly_wait(30)

    if(driver.current_url == "https://lernplattform.gfn.de/login/index.php"):
        print("Falsche Logindaten!")
        return False
    return True


def requestHTML(driver,URL,timeout = 10):
    driver.get(URL)
    driver.implicitly_wait(timeout)
    return driver.page_source

def closeBrowser(driver):
    if driver is not None:
        try:
            driver.quit()
        except Exception as e:
            pass

    # Close the WebDriver
    #driver.quit()
