import requests
from bs4 import BeautifulSoup
import datetime
import json
class Chapter:
    def __init__(self,chapterName:str,link:str,date:str,pagnation: int | None = None):
        self.chapterName =chapterName
        self.link = link
        self.date = date
        self.pagnation = pagnation
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
    @staticmethod
    def fetchJPChapters() -> list["Chapter"]:
        headers = {"Referer": "https://ncode.syosetu.com/","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"}
        session = requests.Session()
        session.headers.update(headers)
        with open("jpsite.json","r") as file:
            latestChapter = json.loads(file.readline())
            lastPeg = latestChapter["lastPagnation"]+1
        baseUrl = f"https://ncode.syosetu.com/n2267be/?p="
        site = session.get(baseUrl+str(lastPeg))
        if (site.status_code == 404):
            lastPeg+=-1
            site = session.get(baseUrl+str(lastPeg))
        bs = BeautifulSoup(site.text,("html.parser"))
        recentChapters = [x for x in bs.find_all("div",class_="p-eplist__sublist")[-5:-1]]
        chapters: list["Chapter"] = []
        for chapter in recentChapters:
            time =  chapter.find("div",class_="p-eplist__update").text.split(" ")[0].strip("\n")
            chapterName = chapter.find("a",class_="p-eplist__subtitle").text
            link = "https://ncode.syosetu.com/" + chapter.find("a",class_="p-eplist__subtitle").get("href")
            chapters.append(Chapter(chapterName,link,time,lastPeg))
      
        return chapters
    def writeToJson(self,filename:str):
        with open (filename,"w") as file:
            data = {
                "chapterName": self.chapterName,
                "link": self.link,
                "date": self.date,
                    }

            if self.pagnation is not None:
                data["lastPagnation"] = self.pagnation

            file.write(json.dumps(data))


def main():
    # chapterlist: list[Chapter] = Chapter.fetchLastedChapters()
    # chapterlist.sort()
    # chapterlist[0].writeToJson("lastestChapter.json")
    Chapter.fetchJPChapters()[-2].writeToJson("jpsite.json")
    # print(Chapter.readFromJson("lastestChapter.json"))
if (__name__ == "__main__"):
    main()


