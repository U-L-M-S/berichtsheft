import os
from mdutils.mdutils import MdUtils
from mdutils import Html
from Addons.module import Moodlemodule

def createMDFromModul(name,modul):
    file = MdUtils(file_name=name,title="")
    file.new_header(level=1,title="Moodle-Infos:")
    file.write("Moodle-ModulID : "+modul.id)
    file.write("\nMoodle-ModulName : "+modul.name)
    file.write("\nMoodle-ModulLink : "+modul.moodleLink)
    file.write("\nMoodle-BewertungLink : "+modul.moodleGradeLink)
    file.write("\nMoodle-KlassenbuchLink : "+modul.classbookLink)
    file.new_paragraph()
    for tag in modul.ClassBookEntry:
        file.new_header(level=1,title=tag[0])
        for row in tag[1]:
            file.write("\n"+row)
        file.new_paragraph()
    file.create_md_file()
    return

