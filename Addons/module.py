import json,bs4,pathlib,os
from bs4 import BeautifulSoup
import urllib,requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from Addons import webBot

class Moodlemodule():
    def __init__(self, modulID, modulName):
        self.id = modulID # MoodleID
        self.name = modulName # Name des Moduls
        self.moodleLink = "" #Link zum Modul
        self.moodleGradeLink = ""# Link zur Modul Bewertungs seite
        self.classbookLink = "" # Link zum Klassenbuch
        self.ClassBookEntry = [] # Einträge ins klassenbuch
                                #Jeder Eintrag ist ein Array aus [Datum,[Array Eintrag Lines]]
        self.schoolmaterialLink = ""# Link zu den Schulungsmaterialien.
        self.schoolmaterials = [] #Array der Materialien [Dateiname,Downloadlink]
        self.Trainers = [] # Speichert Liste der Trainer
                           # Jeder Eintrag ist ein Array aus [Name,ImgLink,ImgName(Name+.jpeg)]  
    def setMoodleLinks(self, MoodleLink, Gradelink):
        self.moodleLink = MoodleLink
        self.moodleGradeLink = Gradelink
    def setContentLinks(self,schoolmeteriallink):
        self.schoolmaterialLink = schoolmeteriallink
    def setClassBookLink(self, link):
        self.classbookLink = link  
    def setClassBookEntry(self, day , content):
        self.ClassBookEntry.append([day,content])
    def getClassBookEntryItem(self,ItemID):
        return self.ClassBookEntry[ItemID]
    
'''
Beispiel als JSON ansicht:
{
  "id": "12074",
  "name": "LF01V2 Das Unternehmen und die eigene Rolle im Betrieb  05.02.2024-09.02.2024",
  "moodleLink": "https://lernplattform.gfn.de/course/view.php?id=12074",
  "moodleGradeLink": "https://lernplattform.gfn.de/course/user.php?mode=grade&amp;id=12074&amp;user=_USER_ID_",
  "classbookLink": "https://lernplattform.gfn.de/mod/attendance/view.php?id=359254&view=4",
  "ClassBookEntry": [
    [
      "Mon, 5.02.24 08:30 - 16:30",
      [
        "Tag 1",
        "Einstieg ins Lernfeld",
        "1.1 Die IT-Ausbildungsberufe",
        "1.2 Die eigene Rlle im Betrieb",
        "Rechte und Pflichten",
        "Ausbildungsvertrag",
        "K\u00fcndigung",
        "Methdik:\nPr\u00e4sentatinen durch\nden Dzenten \nEigen-Recherche\nPr\u00e4sentatinen durch die TN\nFragen und Antwrten\nDiskussin"
      ]
    ],
    [
      "Tue, 6.02.24 08:30 - 16:30",
      [
        "Tag 2",
        "Mitbestimmung im Unternehmen",
        "1.3 Der Ausbildungsbetrieb",
        "\u00b7\nBetrieb und\nUnternehmen",
        "Gliederung der betriebswirtschaftlichen Ans\u00e4tze",
        "Stakehlder",
        "\u00b7\nZiele vn\nBetrieben und Unternehmen (I)",
        "Benennung: Knzern, Unternehmen, Betrieb, Firma",
        "Zielsysteme, Umweltschutz und Nachhaltigkeit",
        "Methdik:\nPr\u00e4sentatinen durch\nden Dzenten \nEigen-Recherche\nDiskussin"
      ]
    ]]
}

'''

#Vars
baseIndexURL = "https://lernplattform.gfn.de"

baseMoodleURL = "https://lernplattform.gfn.de/course/view.php?"
#               https://lernplattform.gfn.de/course/view.php?id=11923

baseMoodleGradeURL = "https://lernplattform.gfn.de/course/user.php?mode=grade&amp;"
#               "https://lernplattform.gfn.de/course/user.php?mode=grade&amp;id=5989&amp;user=18704"

baseClassbookURL = "https://lernplattform.gfn.de/mod/attendance/view.php?"
#                   https://lernplattform.gfn.de/mod/attendance/view.php?id=359254

baseSchoolMaterialURL = "https://lernplattform.gfn.de/course/view.php?id="
baseSchoolMaterialSection = "&section=3"
#                       https://lernplattform.gfn.de/course/view.php?id=11923&section=3


#Debug

def printToJson(List_Of_Modules):
    newJson = json.dumps(List_Of_Modules, default= lambda x: x.__dict__,indent=2) #Erstellt für jedes Modul eine json und verbindet sie später miteinander
    return newJson# return verbundenen JSON

#SaveAndCompareJson

def __compareGetNewJson(Modul):
    newJson = json.dumps(Modul, default= lambda x: x.__dict__,indent=2) #Erstellt für jedes Modul eine json und verbindet sie später miteinander
    return newJson# return verbundenen JSON

def __UpdateTrainers(modul,formated_name):
    trainersFolderContent = os.listdir('./module_data/' + formated_name + "/Trainers")
    for trainers in modul.Trainers:
        #print(str(trainers)+ " | " + str(trainersFolderContent))
        #Checks if Trainer is already in the Trainers Folder Content
        if trainers[2] not in trainersFolderContent :
            #Adds the Trainer to the Trainers Folder
            url = trainers[1]
            response = requests.get(url)
            if response.status_code == 200:
                with open('./module_data/' + formated_name + "/Trainers/"+trainers[2], 'wb') as f:
                    f.write(response.content)
                    f.close()
    return

def __UpdateClassBook(modul,formated_name):
    ClassBookEntrys = os.listdir('./module_data/' + formated_name + "/Classbook")
    #print(ClassBookEntrys)
    #print(modul.ClassBookEntry)
    for entrys in modul.ClassBookEntry:
        entry_format = entrys[0].replace(',','').replace('08:30','').replace('.','-').replace(" ","-").split("---")[0]+'.txt'
        if entry_format not in ClassBookEntrys:
            #print(entry_format)
            with open('./module_data/' + formated_name +"/Classbook/"+entry_format,'w') as file:
                [file.write(x+"\n") for x in entrys[1]]
                file.close()
    return

def __UpdateSchoolMaterials(driver,modul,formated_name):
    SchoolMaterialsList = os.listdir('./module_data/' + formated_name + "/SchoolMaterials")
    #print(ClassBookEntrys)
    #print(modul.ClassBookEntry)
    if modul.schoolmaterials != [] :

        for entrys in modul.schoolmaterials:
            format_entry = entrys[0].replace(" Tag","_Tag").replace(" Kap.","_Kap.")+".pdf"
            if format_entry not in SchoolMaterialsList:
                url = entrys[1]
                driver.get(url)
                webBot.WebDriverWait(driver,10)
    return

def saveAndUpdateJsonData(List_Of_Modules,Full_Update = True):
    #Does a For loop  through all Moduls in the List of Modules and calls the compare function for each one
    #If there are changes they will be saved to the Json file
    pathlib.Path("./module_data").mkdir(parents=True, exist_ok=True)
    for modul in  List_Of_Modules:
        formated_name = modul.name.replace('  ','-').replace(' ','_')
        #check if folder with the name from modul.name exists in ./module_data if not make one
        pathlib.Path("./module_data/" + formated_name).mkdir(parents=True, exist_ok=True)
        try:#try to open the old json data
            oldJson = json.load(open('./module_data/' + formated_name + '/' + 'Data.json', 'r'))
            if oldJson  != __compareGetNewJson(modul):
                #save the new Data into the File
                json.dump(__compareGetNewJson(modul), open('./module_data/' + formated_name + '/' + 'Data.json', 'w'), indent=2)
                print("Updated Module: ", formated_name )
        except :#if it fails just write the new Data into the File
            json.dump(__compareGetNewJson(modul), open('./module_data/' + formated_name + '/' + 'Data.json', 'w'), indent=2)
            print("Module not found created: ", formated_name )
        
        if Full_Update == True:
            #check if folder for Trainer exists
            pathlib.Path("./module_data/" + formated_name + '/Trainers').mkdir(parents=True, exist_ok=True)
            #Get and Update Trainers
            __UpdateTrainers(modul,formated_name)

            #Check if folder for classbook exists
            pathlib.Path("./module_data/" + formated_name + '/Classbook').mkdir(parents=True, exist_ok=True)
            #Get and Update ClassBook
            __UpdateClassBook(modul,formated_name)

            #Check if folder for SchoolMaterials exists
            pathlib.Path("./module_data/" + formated_name + '/SchoolMaterials').mkdir(parents=True, exist_ok=True)
            if modul.schoolmaterials != [] :
                options = webBot.createWebBrowserOptions(headless=True)
                options.add_experimental_option('prefs', {
                "download.default_directory": os.getcwd()+'\\module_data\\' + formated_name + "\\SchoolMaterials", #Change default directory for downloads
                "download.prompt_for_download": False, #To auto download the file
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
                })
                driver = webBot.webBrowserInit(options=options)
                webBot.loadLoginInfo()
                webBot.logInGFN(driver)
                #Get and Update SchoolMaterials
                __UpdateSchoolMaterials(driver, modul,formated_name)
                waiting = True
                while waiting:
                    still_waiting = False
                    for x in os.listdir('./module_data/' + formated_name + "/SchoolMaterials"):
                        if ".crdownload" in x:
                            still_waiting = True
                            break
                    waiting = still_waiting
                counting = 0
                temp = modul.schoolmaterials
                modul.schoolmaterials = []
                for x in os.listdir('./module_data/' + formated_name + "/SchoolMaterials"):
                    modul.schoolmaterials.append([x.replace(".pdf",""),temp[counting][1]])
                driver.close()
    return

#Funktionen

def createModuleGradeLink(Modul,UserID): # Generiert einen Moodle Bewertungs link anhand des Moduls und UserName und der URL base
    return baseMoodleGradeURL + "id="+str(Modul.id)+"&amp;user="+str(UserID)

def createModuleMoodleLink(modul): # Generiert einen Moodle link anhand des Moduls und der URL base
    return baseMoodleURL + "id="+str(modul.id)

def createModuleSchoolMaterialLink(modul): # Generiert einen Schulungsmaterial link andhand der ModulID und BASE url+Section Part
    return baseSchoolMaterialURL + str(modul.id) + baseSchoolMaterialSection

def LookUpClassBookEntrys(driver,modul):
    if(modul.classbookLink != "none"):
        newSoup = BeautifulSoup(webBot.requestHTML(driver,modul.classbookLink),"html.parser") #Lädt die HTML in Beautiful Soup
        for find in newSoup.find_all("tr"): # Sucht die HTML nach allen objekten mit <tr> tag. und geht die mit der for schleife durch
            date = "none" #Set default to None für neuen Tag
            content = [] #Leert Content für neuen tag
            #print(find) # Debug
            dateFound = False #Check Variable
            for fin in find.find_all("td",class_="datecol"): #Sucht die Teil-HTML (Sachen innerhalb des <tr> objekts) nach dem Objekt <td> mit der classe "datecol"
                dateFound = True # Wenn es eins gibt dann hat er das Datum gefunden
                date = fin.get_text() # speichert den Text in der <td> als Variable für später
            if(dateFound == True): #Wenn ein Datum gefunden wurde gibt es auch Klassenbuch einträge
                for fin in find.find_all("td",class_="desccol"): #Sucht die Teil-HTML (Sachen innerhalb des <tr> objekts) nach dem Objekt <td> mit der classe "desccol" und geht diese mit der for schleife durch
                    for fi in fin.find_all("p"): #Sucht die Teil-HTML (Sachen innerhalb des <td> mit der Class "desccol") nach <p> objekten und geht diese mit der for schleife durch
                        if(fi.string != "null"): #Wenn sie nicht null sind.
                            _temp = fi.get_text() #Speichert den Klassenbuch eintrag in eine temp variable
                            _temp = _temp.replace("\u00a0 ","").replace("\u00a0","").replace("o","").replace("\n"," ") # Ersetzt Listen sonderzeichen mit nichts.
                            #print(_temp)
                            if(_temp != ""): #Wenn _temp nicht leer ist.
                                content.append(_temp) # Füge formatierte _temp in die Einträge variable
            if(date != "none" and content != []):# Wenn Datum gefunden wurde und Content nicht leer ist dann füge sie zur Modul hinzu
                modul.setClassBookEntry(date,content) # Classbook Entry ist ein Array mit [[Tag,Array(Content)],[Tag,Array(Content)],[Tag,Array(Content)] usw..]
    return

def LookUpTrainerFromModul(driver,Modul):
    if(driver.current_url != baseIndexURL): # Schaut ob die index schon offen ist
        soup = BeautifulSoup(webBot.requestHTML(driver,baseIndexURL),"html.parser") #Öffnet wenn nicht die Seite und packt es in soup rein
    else: 
        soup = driver.page_source # Wenn seite schon offen ist packt er die html in soup rein.
    card = soup.find("div", attrs={'class':'card', 'data-courseid':''+str(Modul.id)}) #Geht durch alle div mit class activity-content
    for pic in card.find_all("img", attrs={'class': 'rounded-circle'}): #  Sucht nach allen img mit class rounded-circle
        Modul.Trainers.append([pic.get('alt'),pic.get('src'),pic.get('alt')+'.jpeg']) # Fügt dem Modul die Trainer hinzu
    return

    
def LookUpClassBookLink(driver,modul):
    newSoup = BeautifulSoup(webBot.requestHTML(driver,modul.moodleGradeLink),"html.parser") # Lädt HTML in Beautiful Soup
    result = "none" # Set Default Wert
    for item in newSoup.find_all("a",class_="gradeitemheader"):#Suche die HTML nach <a> objekten mit der class "gradeitemheader" und geht alle mit der for schleife durch
       # print(item.get("href")) #debug
        if(item.get("href").startswith(baseClassbookURL)): #Ließt alle Links aus und schaut ob sie wie die Classenbuch URL beginnen- siehe variable = baseClassbookURL
            result = item.get("href")+"&view=4" # nimmt den link und packt &view=4 hinzu, um mehr als nur aktuellen monat anzuzeigen und speichert sie in result variable
    return result #return result

def LookUpSchoolmaterials(driver,modul):
    newSoup = BeautifulSoup(webBot.requestHTML(driver,modul.schoolmaterialLink),"html.parser") # Lädt HTML in Beautiful Soup
    result = "none" # Set Default Wert
    for item_file in newSoup.find_all("a",class_="instancename"):
        modul.schoolmaterials.append([item_file.get("data-title"),item_file.get("href").replace("&redirect=1","")])#Fügt Titel und Downloadlink dem array hinzu
    return result

def setUpMoodleClass(driver,userID,LIST_of_Modules):
    for modul in LIST_of_Modules: # Geht durch eine Liste aus MoodleModul objekten. foreach
        modul.setMoodleLinks(
            createModuleMoodleLink(modul), #
            createModuleGradeLink(modul,userID)
            ) #Erstellt die nötigen Links und packt sie in die Objekt Variablen
        modul.setContentLinks(
            createModuleSchoolMaterialLink(modul)
            ) # Erstellt die content Links
        modul.setClassBookLink(
            LookUpClassBookLink(driver,modul)
            ) #Erstellt den Link
        LookUpClassBookEntrys(driver,modul) # Schreibt das Klassenbuch in das Array
        LookUpTrainerFromModul(driver,modul) # Holt die Namen und Bilder der Trainer
        LookUpSchoolmaterials(driver,modul) # Holt alle Schulungsmaterialien und speichert sie.
        #print(modul.id + " | " + modul.name + " | " +modul.moodleLink + " | " + modul.moodleGradeLink + " | " + modul.classbookLink)
        #if(modul == modules[len(modules)-1]):
        #   print(modul.ClassBookEntry)
        #    print(len(modul.ClassBookEntry))


#Fragt die Module ab (speichert sie in einer liste) und die UserID:
def searchModuleIDsAndUserID(driver):
    modules = [] # Liste der Module
    setUserID = False # Wurde UserID gefunden/gesetzt?
    content = "" # Content definieren.
    if(driver.current_url != "https://lernplattform.gfn.de/grade/report/overview/index.php"):
        content = webBot.requestHTML(driver,"https://lernplattform.gfn.de/grade/report/overview/index.php")
    else:
        content = driver.page_source
    soup = BeautifulSoup(content,"html.parser") # Lädt HTML in Beautiful Soup
    for entry in soup.find_all("tbody"):# Sucht nach allen <tbody> objekten und geht sie im forloop durch
        for item in entry.find_all("a"): # Sucht die Teil-HTML der tbody objekte nach <a> objekten durch
            parsed_url = urlparse(item.get("href")) #nimmt sich die hinterlegten links und lädt sie in urlparse
            if(setUserID == False): #Schaut ob userid schon gesetzt wurde
                setUserID = True #True um die UserID nur 1x zu setzten
                userID = parse_qs(parsed_url.query)['user'][0] #wie ajax requests, schaut den link an und gibt den wert ?user=XXXX die XXXX wieder 
            _tempStr = parse_qs(parsed_url.query)['id'][0] #wie ajax requests, schaut den link an und gibt den wert ?id=XXXX die XXXX wieder 
            modul = Moodlemodule(_tempStr,item.get_text()) #Erstellt ein Moodlemodule Objekt mit der Modul ID und dem Namen des Moduls
            modules.append(modul) #fügt das Objekt in die modules Liste hinzu
    return userID, modules # return die UserID und die Liste der Module
