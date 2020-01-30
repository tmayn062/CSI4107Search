"""Course HTML file pre-processing."""
import os
import bs4
from bs4 import BeautifulSoup
import xml.etree.ElementTree as xml


class Course:
    """Course holds the information for courses."""

    def __init__(self, id, title, description, language):
        """Course init."""
        self.id = id
        self.title = title
        self.description = description
        self.language = language

    def sanitizeCourseInfo(self):
        """Clean up the course information from the file."""
        # filtering out french courses
        languageSpecifier = self.id[5]

        if languageSpecifier in ['5', '7', '6']:
            self.language = "French"
        else:
            # Stripping french title from billingual course
            if self.title.find('/') > 0:
                self.title = self.title.replace(
                    '(3 crÃ©dits / 3 units)', "(3 units)")
                self.title = self.title[self.title.find('/') + 2:]

        if self.description.find('. / ') > 0:
            self.description = (self.description[self.description.find('. / ')
                                + 4:])


def parse(filename):
    """Parse HTML course list file."""
    if os.path.exists(filename) is True:
        if os.path.getsize(filename) <= 0:
            pass
        else:
            print("Parsed file already exists")
            return

    root = xml.Element("Courses")
    with open("UofO_Courses.html", "r") as f:
        data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
        courseDivBlock = soup.findAll("div", {"class": "courseblock"})
        for courseDiv in courseDivBlock:
            course=getValues(courseDiv)
            if course.language=="English":
                if course.description=="No description available for this course":
                    pass
                else:
                    xmlWriter(root, course, filename)


def xmlWriter(root, course, filename):
    """Write XML."""
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
    """Get course values."""
    currentCourse = Course(
        "xxx", "Nil", "No description available for this course", "English")

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

    currentCourse.sanitizeCourseInfo()
    return currentCourse
