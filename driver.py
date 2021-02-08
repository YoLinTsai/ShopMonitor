from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

testURL = "https://www.asos.com/au/nike/nike-air-max-zephyr-eoi-trainers-in-metallic-silver/prd/21396910?colourwayid=60163761&SearchQuery=nike"

class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def connect(self, url):
        self.driver.get(url)

    def addAllToBag(self):
        select = Select(self.driver.find_element_by_id('main-size-select-0'))
        for i in range(1,len(select.options)):
            select.select_by_index(i)
            click_element = self.driver.find_element_by_xpath('//button[@aria-label="Add to bag"]')
            while True:
                try:
                    click_element.click()
                    break
                except:
                    continue 
        '''
        for option in select.options:
            print(option.text)
        '''

    def close(self):
        self.driver.close()

def main():
    with open('config.json') as config_file: 
        config = json.load(config_file)

    driver = Driver()
    driver.connect(testURL)
    driver.addAllToBag()
    time.sleep(5)
    #driver.close()


if __name__ == '__main__':
    main()