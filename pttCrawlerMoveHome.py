from calendar import c
import time
import urllib.request as req
import requests
import bs4
import time
import datetime as dt
import pytz


# LineNotify
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    
    return r.status_code

def message(mes):
    token = "yourLineToken"
    message = ("\n"+mes)
    lineNotifyMessage(token, message)


def getRoot(url):
    request = req.Request(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"})

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    return bs4.BeautifulSoup(data, "html.parser")


def checkTriggerRule(allTitlesSoup, titleSoup, triggerRule):
    # index = int()
    if -1 != titleSoup.a.string.find(triggerRule):
        index = int(allTitlesSoup.index(titleSoup))
        return index    
    else:
        index = int(-1)
        return index
    

url = "https://www.ptt.cc/bbs/xxx/index.html"

twZone = pytz.timezone("Asia/Taipei")
utcZone = pytz.timezone("UTC")

# 此set存放已觸發的title
alreadySendTitle = {""}

i = 0
while i==0:
    root = getRoot(url)
    print("已發過title的set")
    print(alreadySendTitle)

    classTitle="title"
    allTitlesSoup = root.find_all("div", classTitle)

    # 爬日期
    classDate = "date"
    titleDateSoup = root.find_all("div", classDate)

    # 取得當天日期
    utcTime = utcZone.localize(dt.datetime.now())
    taipeiTime = utcTime.astimezone(twZone)
    print("utcTime")
    print(utcTime)
    print("taipeiTime")
    print(taipeiTime)
    month = taipeiTime.month
    day = taipeiTime.day
    
    # 爬蟲的日期格式需要客製化
    if day < 10:
        day = "0" + str(day)
    if month < 10:
        month = " " + str(month)
    currentDate = str(month) + "/" + str(day)
    print("今天" + currentDate)

    # 確認首頁是否有文章, 若無則重新 request url
    if titleDateSoup.__len__() <= 5:
        message("title less than 5")
        # 爬取上一頁url
        classLast = "btn wide"
        lastPageSoup = root.find_all("a", classLast)
        pageList = []
        for page in lastPageSoup:
            pageList.append("https://www.ptt.cc" + page.get("href"))

        lastPageUrl = pageList[1]
        root = getRoot(lastPageUrl)
        allTitlesSoup = root.find_all("div", classTitle)
        titleDateSoup = root.find_all("div", classDate)

    for titleSoup in allTitlesSoup:
        if titleSoup.a != None:
            # 確認此篇title是否已發過line
            if (titleSoup.a.string in alreadySendTitle):
                print("此title已發過")
                continue
            # 此處修改觸發條件
            index = checkTriggerRule(allTitlesSoup, titleSoup, "詢價")
            print("是否觸發新聞")
            print("爬蟲的日期:" + str(titleDateSoup[index].string))
            print(str(-1 != index and (currentDate == titleDateSoup[index].string)))

            if (-1 != index and (currentDate == titleDateSoup[index].string)):
            
                message(titleSoup.a.string)
                alreadySendTitle.add(titleSoup.a.string)
                now = dt.datetime.now()
                print("發送成功" + str(now))
            else:
                continue

    # 當日23:30後清空 set: alreadySendTitle
    utcTime = utcZone.localize(dt.datetime.now())
    endOfDay = utcTime.astimezone(twZone)
    setClearTime = dt.time(23, 30, 0, 0)

    if (endOfDay.time() > setClearTime):
        message(str(endOfDay.time()))
        message("重設set")
        alreadySendTitle.clear()
   
    print("---end for loop----")
    time.sleep(900)



