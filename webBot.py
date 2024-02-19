from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
#Own Imports
import module

if(__name__ == "__main__"):
    # Description: This script logs into the GFN Lernplattform and prints the content of the loaded page.
    # Read credentials from the JSON file
    with open('./credentials.json') as f:
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
        sys.exit()

    #Moodle Lookup.
    userid, modules = module.searchModuleIDsAndUserID(driver) 
    module.setUpMoodleClass(driver,userid,modules)
    #modules ist eine Liste von verfügbaren Modulen z.B. modules[1]
    #diese gehen dann in eine Klasse mit diversen variabeln:
    #modules[i].self.id = int modulID
    #modules[i].name = STR modulName
    #modules[i].moodleLink = STR Link zum Modul selber
    #modules[i].moodleGradeLink = STR Link zum Bewertung vom Modul
    #modules[i].classbookLink = STR Link zum Klassenbuch vom Modul
    #modules[i].ClassBookEntry = [] ARRAY mit Tag,Inhalt.
    print(module.printToJson(modules))
    input("Enter-to-exit!")

# Close the WebDriver
#driver.quit()
