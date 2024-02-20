from Addons import webBot,module,UserInterface,docWriter

def main():
    #Starte Browser
    webBot.webBrowserInit()
    #LoginUser
    loginRetry = 3 #Versuche bis abbruch
    while(loginRetry != 0):
        webBot.loadLoginInfo()
        if(webBot.logInGFN()):
            loginRetry = 0
        else:
            loginRetry -=1

    #Start Moodle Lookup:
    
    #Moodle Lookup.
    userid, modules = module.searchModuleIDsAndUserID() 
    module.setUpMoodleClass(userid,modules)
    #modules ist eine Liste von verfügbaren Modulen z.B. modules[1]
    #diese gehen dann in eine Klasse mit diversen variabeln:
    #modules[i].self.id = int modulID
    #modules[i].name = STR modulName
    #modules[i].moodleLink = STR Link zum Modul selber
    #modules[i].moodleGradeLink = STR Link zum Bewertung vom Modul
    #modules[i].classbookLink = STR Link zum Klassenbuch vom Modul
    #modules[i].ClassBookEntry = [] ARRAY mit Tag,Inhalt.
    print(module.printToJson(modules))
    #docWriter.createMDFromModul("Wochentest",modules[4]) #Erstellt eine MD Datei DEBUG
    return

if(__name__ == "__main__"):
    main()



