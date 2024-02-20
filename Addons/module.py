import json
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs

class Moodlemodule():
    def __init__(self, modulID, modulName):
        self.id = modulID # MoodleID
        self.name = modulName # Name des Moduls
        self.moodleLink = "" #Link zum Modul
        self.moodleGradeLink = ""# Link zur Modul Bewertungs seite
        self.classbookLink = "" # Link zum Klassenbuch
        self.ClassBookEntry = [] # Einträge ins klassenbuch
    def setMoodleLinks(self, MoodleLink, Gradelink):
        self.moodleLink = MoodleLink
        self.moodleGradeLink = Gradelink
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
baseMoodleURL = "https://lernplattform.gfn.de/course/view.php?"
#               https://lernplattform.gfn.de/course/view.php?id=11923

baseMoodleGradeURL = "https://lernplattform.gfn.de/course/user.php?mode=grade&amp;"
#               "https://lernplattform.gfn.de/course/user.php?mode=grade&amp;id=5989&amp;user=18704"

baseClassbookURL = "https://lernplattform.gfn.de/mod/attendance/view.php?"
#                   https://lernplattform.gfn.de/mod/attendance/view.php?id=359254



#Debug

def printToJson(List_Of_Modules):
    newJson= "" # Temp variable für json
    for mod in List_Of_Modules: # geht durch alle Module in der Liste durch
        newJson = newJson + json.dumps(mod, default= lambda x: x.__dict__,indent=2) #Erstellt für jedes Modul eine json und verbindet sie später miteinander
    return newJson# return verbundenen JSON

#Funktionen

def createModuleGradeLink(Modul,UserID): # Generiert einen Moodle Bewertungs link anhand des Moduls und UserName und der URL base
    return baseMoodleGradeURL + "id="+str(Modul.id)+"&amp;user="+str(UserID)

def createModuleMoodleLink(modul): # Generiert einen Moodle link anhand des Moduls und der URL base
    return baseMoodleURL + "id="+str(modul.id)

def LookUpClassBookEntrys(driver,modul):
    if(modul.classbookLink != "none"):
        driver.get(modul.classbookLink) #Öffnet Klassenbuch link
        # Wait for the page to load (you may need to adjust the wait time)
        driver.implicitly_wait(10) # Wartet
        newSoup = BeautifulSoup(driver.page_source,"html.parser") #Lädt die HTML in Beautiful Soup
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
    
def LookUpClassBookLink(driver,modul):
    driver.get(modul.moodleGradeLink) # Lädt die Bewertungsseite
    # Wait for the page to load (you may need to adjust the wait time)
    driver.implicitly_wait(10)

    newSoup = BeautifulSoup(driver.page_source,"html.parser") # Lädt HTML in Beautiful Soup
    result = "none" # Set Default Wert
    for item in newSoup.find_all("a",class_="gradeitemheader"):#Suche die HTML nach <a> objekten mit der class "gradeitemheader" und geht alle mit der for schleife durch
       # print(item.get("href")) #debug
        if(item.get("href").startswith(baseClassbookURL)): #Ließt alle Links aus und schaut ob sie wie die Classenbuch URL beginnen- siehe variable = baseClassbookURL
            result = item.get("href")+"&view=4" # nimmt den link und packt &view=4 hinzu, um mehr als nur aktuellen monat anzuzeigen und speichert sie in result variable
    return result #return result

def setUpMoodleClass(driver,userID,LIST_of_Modules):
    for modul in LIST_of_Modules: # Geht durch eine Liste aus MoodleModul objekten. foreach
        modul.setMoodleLinks(
            createModuleMoodleLink(modul), #
            createModuleGradeLink(modul,userID)
            ) #Erstellt die nötigen Links und packt sie in die Objekt Variablen
        modul.setClassBookLink(
            LookUpClassBookLink(driver,modul)
            ) #Erstellt den Link
        LookUpClassBookEntrys(driver,modul) # Schreibt das Klassenbuch in das Array
        #print(modul.id + " | " + modul.name + " | " +modul.moodleLink + " | " + modul.moodleGradeLink + " | " + modul.classbookLink)
        #if(modul == modules[len(modules)-1]):
        #   print(modul.ClassBookEntry)
        #    print(len(modul.ClassBookEntry))


#Fragt die Module ab (speichert sie in einer liste) und die UserID:
def searchModuleIDsAndUserID(driver):
    modules = [] # Liste der Module
    setUserID = False # Wurde UserID gefunden/gesetzt?
    soup = BeautifulSoup(driver.page_source,"html.parser") # Lädt HTML in Beautiful Soup
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
