import requests
from bs4 import BeautifulSoup
import datetime
import json
class Chapter:
    def __init__(self,chapterName:str,link:str,date:str):
        self.chapterName =chapterName
        self.link = link
        self.date = date
    def _dateToInt(self) -> tuple[int, int, int,int,int,int]:
        if (self.date.find("T") == -1):
            small = None
        else:
            small = self.date.split("T")[1]
        big = self.date.split("T")[0]
        return tuple(map(int, big.split("-")+small.split("+")[0].split(":") if small is not None else []))
    def __gt__(self, other):
        return self._dateToInt() > other._dateToInt()
    def __eq__(self, other):
        return  self.date == other.date
    def __str__(self):
        return f'Chapter Name: {self.chapterName}, link: {self.link}, date: {self.date}'
    @staticmethod
    def readFromJson(filename:str) -> "Chapter":
        with open (filename, 'r') as file:
            try:
                chapterInfo = json.loads(file.readline())
            except:
                chapterInfo = {"chapterName":"empty","link":"n/a","date":"0000-00-00T00:00:00+00:00"}
            return Chapter(**chapterInfo)
    @staticmethod
    def fetchLastedChapters() -> list["Chapter"]:
        site = requests.get("https://witchculttranslation.com/")
        bs = BeautifulSoup(site.text,("html.parser"))
        recentChapters = [x for x in bs.find_all("li",class_="rpwe-li rpwe-clearfix")]
        li: list[Chapter] = []
        for chapter in recentChapters:
            link = chapter.find("a").get("href")
            name = chapter.find("a").getText()
            date = chapter.find("time").get("datetime")
            li.append(Chapter(name,link,date))
        return li
    def writeToJson(self,filename:str):
        with open (filename,"w") as file:
            file.write(json.dumps({"chapterName": self.chapterName,"link":self.link,"date":self.date}))


def main():
    # chapterlist: list[Chapter] = Chapter.fetchLastedChapters()
    # chapterlist.sort()
    # chapterlist[0].writeToJson("lastestChapter.json")
    pass
    # print(Chapter.readFromJson("lastestChapter.json"))
if (__name__ == "__main__"):
    main()


