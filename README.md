# berichtsheft
Moodle crawler with local storage.<br/>
Gets all the information from a Moodle site and stores it  locally. The program is written in Python, using the Selenium WebDriver library to interact with the Moodle-Website. It downloads all usefull data you can access with your moodle Account.<br/>
<br/>
Edit credentials.json  to include your Moodle username and password, then run the script
the script takes about 1-2 Min to crawl  all courses of a moodle site.  The data is stored in the "module_data" folder.<br/>
<br/>
# Folder Structure (pre run):<br/>
[MainFolder]<br/>
- |--> Addons  (contains all addon files)<br/>
  -  |--> docWriter.py    (class for writing documentation in a file)<br/>
  -  |--> module.py        (main class for module handling)<br/>
  -  |--> webBot.py          (WebBrowser automation using Selenium WebDriver)<br/>
- |--credentials.json (contains login information)<br/>
- |--main.py  (the main python file that runs the program)<br/>
- |--requirements.txt  (python dependencies)<br/>
- |--README.md   (this document)<br/>
 <br/><br/>
# Folder Structure (after run):<br/>
[MainFolder]<br/>
- |--> Addons  (contains all addon files)<br/>
  -  |--> docWriter.py    (class for writing documentation in a file)<br/>
  -  |--> module.py        (main class for module handling)<br/>
  -  |--> webBot.py          (WebBrowser automation using Selenium WebDriver)<br/>
- |--> module_data       (folder containing collected data from modules)<br/>
  -  |--> NAME_OF_MODULE<br/>
     -   |--> Classbook <br/>
         -    |--DATE_OF_CLASS.txt (Classbook entry of the Day)<br/>
         -    |...<br/>
     -   |--> SchoolMaterials<br/>
         -    |--NAME.pdf  (collected material, downloaded)<br/>
         -    |...<br/>
     -   |--> Trainers<br/>
         -    |--Trainer.jpeg (Named after Trainer itself. Contains image of trainer.)<br/>
     -   |--Data.json<br/>
- |--credentials.json (contains login information)<br/>
- |--main.py  (the main python file that runs the program)<br/>
- |--requirements.txt  (python dependencies)<br/>
- |--README.md   (this document)<br/>

## Requirements
- python3
- os
- beautifulSoup4
- pathlib
- requests
- urllib
- json
- selenium
- Internet connection


## Installion 
### Windows
- Make sure you have [git](https://git-scm.com/download/win) on your system and [python3](https://www.python.org/downloads/).
- Clone the repositoy on your local machine.
```sh
git clone https://github.com/U-L-M-S/berichtsheft
```
- go inside the directory you just cloned
```sh
cd berichtsheft
```
- install the required packages (I recommend using [CMD](https://learn.microsoft.com/de-de/windows-server/administration/windows-commands/cmd))
```sh
pip install -r requirements.txt
```
- open the project in your favorite IDE (example: VSC)
```sh
code .
```
- Make sure to change your credentials on **credentials.json**

### Linux
- Normally  [git](https://git-scm.com/) should be standard in every linux distro and [python3](https://www.python.org/) can be easily installed using your package manager.

- Clone the repositoy on your local machine.
```sh
git clone https://github.com/U-L-M-S/berichtsheft
```
- go inside the directory you just cloned
```sh
cd berichtsheft
```
- install the required packages
```sh
pip install -r requirements.txt
```
- open the project in your favorite IDE (example: VSC)
```sh
code .
```
- Make sure to change your credentials on **credentials.json**
