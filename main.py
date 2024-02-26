from Addons import webBot,module,docWriter
import os

def main():

    #Starte Browser
    options = webBot.createWebBrowserOptions(headless=False)
    driver = webBot.webBrowserInit(options=options)
    #WebDriver = webBot.driver #So bekommt man den webDriver
    #LoginUser
    loginRetry = 3 #Versuche bis abbruch
    while(loginRetry != 0):
        webBot.loadLoginInfo()
        if(webBot.logInGFN(driver)):
            loginRetry = 0
        else:
            loginRetry -=1

    #Moodle Lookup.
    userid, modules = module.searchModuleIDsAndUserID(driver) 
    module.setUpMoodleClass(driver,userid,modules)
    webBot.closeBrowser(driver)
    #modules ist eine Liste von verfügbaren Modulen z.B. modules[1]
    #diese gehen dann in eine Klasse mit diversen variabeln:
    #modules[i].self.id = int modulID
    #modules[i].name = STR modulName
    #modules[i].moodleLink = STR Link zum Modul selber
    #modules[i].moodleGradeLink = STR Link zum Bewertung vom Modul
    #modules[i].classbookLink = STR Link zum Klassenbuch vom Modul
    #modules[i].ClassBookEntry = [] ARRAY mit Tag,Inhalt.

    module.saveAndUpdateJsonData(modules)
    #print(module.printToJson(modules))
    #docWriter.createMDFromModul("Wochentest",modules[4]) #Erstellt eine MD Datei DEBUG
    #input("Enter to exit.")
    return

if(__name__ == "__main__"):
    main()



