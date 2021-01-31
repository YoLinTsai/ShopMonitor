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

ASOS_URL = [    "https://www.asos.com/us/search/?currentpricerange=5-75&q=new%20balance&sort=freshness",
                "https://www.asos.com/search/?currentpricerange=5-175&q=nike&sort=freshness",
                "https://www.asos.com/au/search/?currentpricerange=5-175&q=nike&sort=freshness",
                "https://www.asos.com/us/search/?currentpricerange=0-140&q=nike&sort=freshness",
                "https://www.asos.com/search/?currentpricerange=5-135&page=1&q=new%20balance&scrollTo=product-22523535&sort=freshness"]

cookie = "browseCountry=TW; browseCurrency=TWD; storeCode=ROW; browseSizeSchema=UK; browseLanguage=en-GB; currency=10085; optimizelyEndUserId=oeu1611834092433r0.25163916243029694; featuresId=c8d8e0af-b190-4fa7-ab83-c357b0c502c0; bt_recUser=0; bt_stdstatus=NOTSTUDENT; floor=1001; asos=PreferredSite=&currencyid=10085&currencylabel=TWD&topcatid=1001&customerguid=af3166b7f0834fdf8c5171f6e12ea8e7; s_ecid=MCMID%7C17895036272560139822200822303156821055; _gcl_au=1.1.382856720.1611834097; asosAffiliate=affiliateId=12496; bt_affid=12496; bt_gclid=Cj0KCQiA3smABhCjARIsAKtrg6J4grBDy_JMHeWiRcYQ8QKHz1l3F7ZP4SKrY_4sUPsrXjTw4o3QV_YaAlomEALw_wcB; _gcl_aw=GCL.1611836390.Cj0KCQiA3smABhCjARIsAKtrg6J4grBDy_JMHeWiRcYQ8QKHz1l3F7ZP4SKrY_4sUPsrXjTw4o3QV_YaAlomEALw_wcB; _gcl_dc=GCL.1611836390.Cj0KCQiA3smABhCjARIsAKtrg6J4grBDy_JMHeWiRcYQ8QKHz1l3F7ZP4SKrY_4sUPsrXjTw4o3QV_YaAlomEALw_wcB; _scid=3a10a529-10c6-49bf-99a3-cbef6fee8fe2; _sctr=1|1611763200000; geocountry=TW; bm_sz=7BCAA9AD250E876D679DE29FF7E2665C~YAAQbcdCyzTv00d3AQAAD+/OUQpNLbKkuJWSrKWBGuDj3TWGeZuahoazjEAIyZsUHEJa4UnzTo3NGwGE9UNuakNeG26cKEYWqOpqwA6kD2/AAM80E/FXcaNX9ulW57/JPPo69O9IrL4cOYqK8DGplFLezJZd9SZzOCu3Vx9b8BB4iaFfRh03u+vDFT3M0A==; siteChromeVersion=au=11&com=11&de=11&dk=11&es=11&fr=11&it=11&nl=11&pl=11&roe=11&row=11&ru=11&se=11&us=11; keyStoreDataversion=3pmn72e-27; ak_bmsc=9DA9A416B642BC92D86CCE29CEA90EE7CB42C76DD03E000070F11460504AF770~pl01bk+tJrGYKV4zmwFTWVathb2mdFYsIIrCJ1dTrcES10D20466yi4OtNcubuyL2vr24irCzstBvHlvGTYuU4zOHmoA+h/G03Xo3a3K2O+3cxb9oO3wnAsfUMzMEO6oDrhxrrm1AbcmUXSBMvwLcmNxSgHjobsrONUY7HpN0oELZ9uag+jgv0m2G689NRCOcVGeQ2p2eaSvr5cUJKiWsY0gVq/+0R+1sxIp5HDcSYwl8=; asos-gdpr22=true; asos-b-sdv629=3pmn72e-27; btpdb.ydg7T9K.dGZjLjcxMzA0Nzc=U0VTU0lPTg; _uetsid=c287b49062bd11eba2ead3b359d1f197; _uetvid=c5e17170615d11ebb60763a4244ca9d8; AMCV_C0137F6A52DEAFCC0A490D4C%40AdobeOrg=-1303530583%7CMCMID%7C17895036272560139822200822303156821055%7CMCAAMLH-1612590072%7C11%7CMCAAMB-1612590072%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1611992472s%7CNONE%7CvVersion%7C3.3.0%7CMCAID%7CNONE%7CMCCIDH%7C0; AMCVS_C0137F6A52DEAFCC0A490D4C%40AdobeOrg=1; _s_fpv=true; s_cc=true; btpdb.ydg7T9K.dGZjLjc0Nzk3NzM=U0VTU0lPTg; _gid=GA1.2.1777317663.1611985274; _ga=GA1.1.331876108.1611834097; plp_columsCount=twoColumns; bm_mi=DCFD1E6D31E9751C95141199C356A6CF~HlfEI0SDdhwD8AqVtK4IljvGAjFonXGXwKnU0NiKj4/LohephZ5gmurWuBv5GUrJQGb+CfTY+XUvy8f7P0wd4M0Ay85B8hCaqHXDXkOUAkP/saoRH6nfPqc2nScOvCQcHurppCkgLkJ5kkdvSvdH/amQgRx4HFngAVsDfW3ZeoO1swazlIEmk7nfZT8gTo2i2CtUO4zu8tx+a9Md1Z/nPcIZ/hJ/dOW1gfhQUpcpHM9yCCLVJMM464jv3BpFoUhw2N37VY5wBgDLLT4ezFqMealIiGujQOM0K1tciYlFDSiX9nk9oYdz3xq5/6fHXPHb; s_pers=%20s_vnum%3D1612108800950%2526vn%253D4%7C1612108800950%3B%20s_invisit%3Dtrue%7C1611987409251%3B%20s_nr%3D1611985609256-Repeat%7C1643521609256%3B%20gpv_e47%3Dno%2520value%7C1611987409259%3B%20gpv_p10%3Ddesktop%2520row%257Csearch%2520page%257Csuccessful%2520search%2520refined%2520page%25201%7C1611987409263%3B; _abck=A1179B2E1BBED7A7748E4905899A0AA1~0~YAAQHsdCy6pF1Ud3AQAA9mLUUQVtTdys4BI9tg+F7vHNdFPLFIfR7yKpx2mcWSGYPml+NYgExuUqqF2wNdZRLCYSlX6QGMNMuEAnXWssWFb6OkwPsDaHAy685AYB87sFxHKrHwEE7iZxVAZ41FziOerMg+Geel3PJwCtJdVvwsNYsE3fH7dHEO5ScZK9jXPmSzALXdiODFIOYgj+ZIgzNNMlzj7a1CbXlFk21r594P03sdIKsOPZZDA9UlwtAQKwmKXoSeuXh8GWvYdATmk6nPaAz1LZvWpbH20k7eQgwSG5OY2JoSM5QyTUGXQi5eyUhgi1Q2d1Cho4xGIJl9gFFS65jmI=~-1~-1~-1; asos-perx=af3166b7f0834fdf8c5171f6e12ea8e7||8e5aecea6a634e2bbe4ec2f5d8eb8699; _ga_54TNE49WS4=GS1.1.1611985274.4.1.1611985610.52"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            ,'cookie': cookie}

keyWords = [['327'],
            ['Jordan', 'Dunk', 'Air force'],
            ['Jordan', 'Dunk', 'Air force'],
            ['Jordan', 'Dunk', 'Air force'],
            ['327']]

title = ["US New Balance",
        "NIKE",
        "AU NIKE",
        "US NIKE",
        "New Balance"]

class Good:
    def __init__(self, desc, price, href):
        self.desc = desc
        self.price = price
        self.href = href

def get(url):
    response = requests.get(url, headers=headers)
    return response

class Distiller:
    def __init__(self, url, cookie, keyWords, headers, title):
        self.url = url
        self.cookie = cookie
        self.keyWords = keyWords
        self.headers = headers
        self.title = title
        self.goodList = self.parseHTML(get(self.url))
        self.showGoodList(2)

    def setCookie(self, cookie):
        self.cookie = cookie

    def showGoodList(self, showNum):
        if showNum == 0:
            pass
        else:
            print('\033[1;;46m'+self.title+'\033[0m')
            for i in range(showNum):
                good = self.goodList[i]
                print("Name:\t"+good.desc)
                print("Price:\t"+good.price)
        return

    def refreshGoodList(self):
        # get url response again and check if new good arrives
        try:
            response = get(self.url)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)

        curGoodList = self.parseHTML(response) 
        self.setCookie(requests.utils.dict_from_cookiejar(response.cookies))
        newGoodList = []
        checkPoint = -1;
        for i in range(len(curGoodList)):
            if curGoodList[i].desc == self.goodList[0].desc:
                checkPoint = i

        if checkPoint == 0:
            pass
        elif checkPoint == -1:
            self.goodList = curGoodList
            newGoodList = curGoodList
        else:
            self.goodList = curGoodList
            newGoodList = curGoodList[0:checkPoint]

        self.showGoodList(len(newGoodList))
        self.checkKeyWords(newGoodList)

    def checkKeyWords(self, goodList):
        for kw in self.keyWords:
            for good in goodList:
                if good.desc.find(kw) != -1:
                    slackWrapper.pinSlack(self.title, good.desc, good.href)

    def parseHTML(self, response):
        parser = etree.HTMLParser()
        tree = html.fromstring(response.content)
        goods = tree.xpath('//article/a')

        goodList = []
        for i in range(len(goods)):
            token = goods[i].attrib['aria-label'].split('; ')
            href = goods[i].attrib['href']

            goodList.append(Good(token[0], token[1], href))
        return goodList

class SlackWrapper:
    def __init__(self):
        self.webhookURL = "https://hooks.slack.com/services/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"
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
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
            exit_flag = True
            return False
    except:
        pass

slackWrapper = SlackWrapper()
exit_flag = False
interval = 10 #sec

def main():

    #initial and first check
    distillers = []
    print('\033[1;;45m  First Check  \033[0m')
    for i in range(len(ASOS_URL)):
        distillers.append(Distiller(ASOS_URL[i], cookie, keyWords[i], headers, title[i]))

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not exit_flag:
            time.sleep(interval);
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            for i in range(len(distillers)):
                distillers[i].refreshGoodList()

            print("\r" + "Last Check Time =", 
                "\033[1;40;46m"+current_time+"\033[0m", end="")

        print("\033[1;;42m\n Quit Checking New Goods~ \033[0m")
    
if __name__ == '__main__':
    main()