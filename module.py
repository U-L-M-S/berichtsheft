import json
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
import module

class Moodlemodule():
    def __init__(self, modulID, modulName):
        self.id = modulID
        self.name = modulName
        self.moodleLink = ""
        self.moodleGradeLink = ""
        self.classbookLink = ""
        self.ClassBookEntry = []
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
    newJson= ""
    for mod in List_Of_Modules:
        newJson = newJson + json.dumps(mod, default= lambda x: x.__dict__,indent=2)
    return newJson

#Funktionen

def createModuleGradeLink(Modul,UserID):
    return baseMoodleGradeURL + "id="+str(Modul.id)+"&amp;user="+str(UserID)

def createModuleMoodleLink(modul):
    return baseMoodleURL + "id="+str(modul.id)

def LookUpClassBookEntrys(driver,modul):
    if(modul.classbookLink != "none"):
        driver.get(modul.classbookLink)
        # Wait for the page to load (you may need to adjust the wait time)
        driver.implicitly_wait(10)
        newSoup = BeautifulSoup(driver.page_source,"html.parser")
        for find in newSoup.find_all("tr"):
            date = "none"
            content = []
            #print(find)
            dateFound = False
            for fin in find.find_all("td",class_="datecol"):
                dateFound = True
                date = fin.get_text()
            if(dateFound == True):
                for fin in find.find_all("td",class_="desccol"):
                    for fi in fin.find_all("p"):
                        if(fi.string != "null"):
                            _temp = fi.get_text()
                            _temp = _temp.replace("\u00a0 ","").replace("\u00a0","").replace("o","").replace("\n"," ")
                            #print(_temp)
                            if(_temp != ""):
                                content.append(_temp)
            if(date != "none" and content != []):
                modul.setClassBookEntry(date,content)     
    return
    
def LookUpClassBookLink(driver,modul):
    driver.get(modul.moodleGradeLink)
    # Wait for the page to load (you may need to adjust the wait time)
    driver.implicitly_wait(10)

    newSoup = BeautifulSoup(driver.page_source,"html.parser")
    result = "none"
    for item in newSoup.find_all("a",class_="gradeitemheader"):
       # print(item.get("href"))
        if(item.get("href").startswith(baseClassbookURL)):
            result = item.get("href")+"&view=4"
    return result

def setUpMoodleClass(driver,userID,LIST_of_Modules):
    for modul in LIST_of_Modules:
        modul.setMoodleLinks(
            createModuleMoodleLink(modul),
            createModuleGradeLink(modul,userID)
            ) #Erstellt die nötigen Links
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
    modules = []
    setUserID = False
    soup = BeautifulSoup(driver.page_source,"html.parser")
    for entry in soup.find_all("tbody"):
        for item in entry.find_all("a"):
            parsed_url = urlparse(item.get("href"))
            if(setUserID == False):
                setUserID = True
                userID = parse_qs(parsed_url.query)['user'][0]
            _tempStr = parse_qs(parsed_url.query)['id'][0]
            modul = module.Moodlemodule(_tempStr,item.get_text())
            modules.append(modul)
    return userID, modules
