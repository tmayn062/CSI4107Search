import os
import bs4
from bs4 import BeautifulSoup
import xml.etree.ElementTree as xml

class Course:
    def __init__(self, id, title, description, language):
        self.id = id
        self.title = title
        self.description=description
        self.language=language

    def sanatizeCourseInfo(self):

        # filtering out french courses
        languageSpeficier=self.id[5]

        if languageSpeficier == '5' or languageSpeficier == '7' or languageSpeficier == '6':
            self.language="French"
        else:
            # Stripping french title from billingual course
            if self.title.find('/') > 0:
                self.title = self.title.replace('(3 crÃ©dits / 3 units)', "(3 units)")
                self.title = self.title[self.title.find('/') + 2:]

            if self.description.find('. / ') > 0:
                self.description = self.description[self.description.find('. / ') + 4:]




def main():
    filename = "uOttawaCourseList.xml"
    if os.path.exists(filename)==True:
        if os.path.getsize(filename)<=0:
            pass
        else:
            print("File already exist")
            return

    root = xml.Element("Courses")
    with open("UofO_Courses.html", "r") as f:
        data=f.read()
        soup = BeautifulSoup(data, 'html.parser')
        courseDivBlock = soup.findAll("div", {"class": "courseblock"})
        for courseDiv in courseDivBlock:
            course=getValues(courseDiv)
            if course.language=="English":
                xmlWriter(root, course, filename)



def xmlWriter(root, course, filename):
    userelement = xml.Element("Course")
    root.append(userelement)
    courseID = xml.SubElement(userelement, "courseID")
    courseID.text = course.id
    courseTitle = xml.SubElement(userelement, "courseTitle")
    courseTitle.text = course.title
    courseDescription = xml.SubElement(userelement, "courseDescription")
    courseDescription.text = course.description
    tree = xml.ElementTree(root)
    with open(filename, "wb") as fh:
        tree.write(fh)

def getValues(course):
    currentCourse=Course("xxx","Nil","No description available for this course", "English")

    for element in course:
        ty = type(element)
        if ty is bs4.element.Tag:
            classType = element['class'][0]
            if classType == "courseblocktitle":
                title = element.get_text()
                currentCourse.id = title[:8]
                currentCourse.title = title[9:]

            if classType == "courseblockdesc":
                descript = element.get_text()
                currentCourse.description = descript



    currentCourse.sanatizeCourseInfo()
    return currentCourse






if __name__ == '__main__':
    main()

