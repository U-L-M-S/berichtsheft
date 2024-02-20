from Addons import webBot,module,UserInterface,docWriter

def main():
    #Moodle Lookup.
    userid, modules = module.searchModuleIDsAndUserID(webBot.driver) 
    module.setUpMoodleClass(webBot.driver,userid,modules)
    #modules ist eine Liste von verfügbaren Modulen z.B. modules[1]
    #diese gehen dann in eine Klasse mit diversen variabeln:
    #modules[i].self.id = int modulID
    #modules[i].name = STR modulName
    #modules[i].moodleLink = STR Link zum Modul selber
    #modules[i].moodleGradeLink = STR Link zum Bewertung vom Modul
    #modules[i].classbookLink = STR Link zum Klassenbuch vom Modul
    #modules[i].ClassBookEntry = [] ARRAY mit Tag,Inhalt.
    print(module.printToJson(modules))
    docWriter.createMDFromModul("Wochentest",modules[4])
    return

def finishWebBot(): # Wird von webBot gecalled wenn er fertig ist mit dem Browser und man eingeloggt ist.
    main()
    return



