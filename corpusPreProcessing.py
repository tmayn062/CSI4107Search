from bs4 import BeautifulSoup
import requests
import html


def main():
    result=requests.get("file:///C:/Users/boerg/AppData/Local/Temp/7zO80923AD7/UofO_Courses.html")
    tree=html.fromstring()

    pass

