import requests
import json
import webbrowser
import os
from selenium import webdriver
import sys
from lxml import etree, html
from io import StringIO
import time
from datetime import datetime
from pynput import keyboard
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

headers = {'authority': 'www.asos.com'
            ,'method': 'GET'
            ,'path': '/search/?q=new+balance'
            ,'scheme': 'https'
            ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,'accept-encoding': 'gzip, deflate, br'
            ,'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
            ,'cache-control': 'max-age=0'
            ,'if-none-match': 'W/"5552e-cA/yOC/oPEqKlGJTCuEOPig1648""'
            ,'referer': 'https://www.asos.com/'
            ,'sec-fetch-dest': 'document'
            ,'sec-fetch-mode': 'navigate'
            ,'sec-fetch-site': 'same-origin'
            ,'sec-fetch-user': '?1'
            ,'upgrade-insecure-requests': '1'
            ,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

class FileWriter:
    def __init__(self, filename):
        self.fp = open(filename, "a")

    def write(self, string):
        self.fp.write(string)

    def close(self):
        self.fp.close()

driver = webdriver.Chrome()
logger = FileWriter("newGoodData.txt")
with open('config.json') as config_file: 
    config = json.load(config_file) 

class Good:
    def __init__(self, desc, price, href):
        self.desc = desc
        self.price = price
        self.href = href

class Distiller:
    def __init__(self, mode, config, headers):
        self.mode = mode
        self.url = config["url"]
        self.keyWords = config["keywords"]
        self.title = config["title"]
        self.headers = headers
        #self.firstCheckURL()
        self.goodList = self.getCurGoodList()
        self.showGoodList(2)

    def showGoodList(self, showNum):
        if showNum == 0:
            pass
        else:
            print('\033\n[1;;46m'+self.title+'\033[0m')
            for i in range(showNum):
                good = self.goodList[i]
                print("Name:\t"+good.desc)
                print("Price:\t"+good.price)
        return

    def refreshGoodList(self):
        # get url response again and check if new good arrives
        curGoodList = self.getCurGoodList()
        newGoodList = []
        checkPoint = -1;

        
        testGoodList = []
        testGoodList.append(Good("new balance 327","test","test"))
        testGoodList.extend(curGoodList)

        curGoodList=testGoodList
        

        for i in range(len(curGoodList)):
            if curGoodList[i].desc == self.goodList[0].desc:
                checkPoint = i

        showNum = 2
        if checkPoint == 0:
            showNum = 0
        elif checkPoint == -1:
            self.goodList = curGoodList
            newGoodList = curGoodList
        else:
            self.goodList = curGoodList
            newGoodList = curGoodList[0:checkPoint]

        if checkPoint != 0:
            self.writeNewGoodInfo(newGoodList)
            self.checkKeyWords(newGoodList)
            #self.checkKeyWords(self.goodList)

    def writeNewGoodInfo(self, goodList):
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d, %H:%M:%S\n")
        logger.write(current_time)
        for good in goodList:
            logger.write(self.title+"\n")
            logger.write(good.desc+"\n")
            logger.write(good.href+"\n")

    def checkKeyWords(self, goodList):
        for kw in self.keyWords:
            for good in goodList:
                curDesc = good.desc.lower()
                if curDesc.find(kw.lower()) != -1:
                    slackWrapper.pinSlack(self.title, good.desc, good.href)

    def getCurGoodList(self):
        goodList = []

        if self.mode == 'selenium':
            global driver
            while len(goodList) == 0:
                try:
                    driver.get(self.url)
                    HTML = driver.page_source
                    soup = BeautifulSoup(HTML, "lxml")
                    for article in soup.find_all('article'):
                        e = article.find_all('a')[0]
                        token = e.get('aria-label').split('; ')
                        href = e.get('href')
                        goodList.append(Good(token[0], token[1], href))
                    #self.driver.close()
                except:
                    continue
        else:
            try:
                #response = requests.get(url, headers=headers)
                response = requests.get(self.url, headers=self.headers, timeout=5)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            #self.setCookie(requests.utils.dict_from_cookiejar(response.cookies))
            parser = etree.HTMLParser()
            tree = html.fromstring(response.content)
            goods = tree.xpath('//article/a')


            for i in range(len(goods)):
                token = goods[i].attrib['aria-label'].split('; ')
                href = goods[i].attrib['href']
                goodList.append(Good(token[0], token[1], href))

        return goodList

class SlackWrapper:
    def __init__(self,config):
        self.webhookURL = config["webhookURL"]
        self.headers = config["headers"]
    
    def pinSlack(self, website, desc, href):
        message = website + "\n" + desc + '\n' + href + '\n'
        data = {'text': message}
        r = requests.post(self.webhookURL, data=json.dumps(data), headers=self.headers)

def on_press(key):
    pass

def on_release(key):
    try:
        if key.char == 'q':
            global exit_flag
            exit_flag = False
            return False
    except:
        pass

slackWrapper = SlackWrapper(config["slack"])
exit_flag = False
interval = 5 #sec

def main():

    #initial and first check
    distillers = []
    print('\033[1;;45m  First Check  \033[0m')
    for i in range(len(config["distiller"])):
        distillers.append(Distiller('selenium', 
            config["distiller"][i],
            headers))

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not exit_flag:
            time.sleep(interval);
            now = datetime.now()
            current_time = now.strftime("%Y/%m/%d, %H:%M:%S")

            for i in range(len(distillers)):
                distillers[i].refreshGoodList()

            print("\r" + "Last Check Time =", 
                "\033[1;40;46m"+current_time+"\033[0m", end="")

        print("\033[1;;42m\n Quit Checking New Goods~ \033[0m")
    
if __name__ == '__main__':
    main()