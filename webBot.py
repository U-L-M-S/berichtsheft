from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Read credentials from the JSON file
with open('credentials.json') as f:
    credentials = json.load(f)

# Extract username and password from credentials
username = credentials['username']
password = credentials['password']

# Initialize the WebDriver
driver = webdriver.Chrome()  # Chrome because some boxes does not content IDs in other browsers 

# Load the login page
login_url = 'https://lernplattform.gfn.de/login/index.php'
driver.get(login_url)

# Find the username and password input fields and submit button
# Wait for the username input box to be present
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'username'))
)
# Wait for the password input box to be present
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'password'))
)
# Wait for the login button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'loginbtn'))
)
# Fill in the login form
username_input.send_keys('username')
password_input.send_keys('password')

# Click on the submit button
login_button.click()

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(5)

# Print the content of the loaded page
print(driver.page_source)

# Close the WebDriver
driver.quit()
