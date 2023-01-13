from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
import time
import copy
from datetime import datetime

class App:

    release_date:datetime = None

    def __init__(self, link, name = "", installs = [], level = 0, similar_list = []) -> None:
        self.link = link
        self.name = name
        self.installs = installs
        self.leval = level
        self.similar_list = similar_list
        pass

    def simular_position(self, bundleID):
        lk = "https://play.google.com/store/apps/details?id=" + bundleID
        if self.similar_list.__contains__(lk):
            return self.similar_list.index(lk)
        else:
            return -1

def parser_similar(bundleID = "org.telegram.messenger") -> dict:
    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
    #browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
    browser.implicitly_wait(10)
    browser.maximize_window()
    app = checking_similar_apps(browser=browser, level=0, bundleID=bundleID)
    map_apps = {}
    def in_depth(app: App, lev:int, max):
        if(app != None):
            for i, link in enumerate(app.similar_list):
                link:str = link
                if(map_apps.get(link, None) == None and i <= max):
                    app1 = checking_similar_apps(
                            browser=browser,
                            level=lev,
                            bundleID=link.replace("https://play.google.com/store/apps/details?id=", "")
                        )
                    if(app1 != None):  
                        map_apps[link] = app1
                    print(str(i + 1) + " / " + str(len(app.similar_list)) + " / " + str(lev))
    in_depth(app, 1, 256)
    lst = copy.copy(map_apps).values()
    for i, a in enumerate(lst):
        in_depth(a, 2, 16)
        print(str(i + 1) + " / " + str(len(lst)))
    for item_app in map_apps.values():
        item_app:App = item_app
        if(item_app.simular_position(bundleID) != -1):
            item_app.release_date = get_release_date(browser, item_app.link)
            print(item_app.release_date)

    browser.quit()
    return map_apps

def get_release_date(browser:webdriver.Firefox, link:str) -> datetime:
    browser.get(link + "&hl=en&gl=US")
    button_deteils: List[WebElement] = browser.find_elements(By.CLASS_NAME, "VfPpkd-Bz112c-LgbsSe")
    btn_deteils = find_element_by_attribute_value(button_deteils, "aria-label", "See more information on About this app")
    if(btn_deteils == None):
        btn_deteils = find_element_by_attribute_value(button_deteils, "aria-label", "See more information on About this game")
    if(btn_deteils != None):
        btn_deteils.click()
        time.sleep(5)
        deteils: List[WebElement] = browser.find_elements(By.CLASS_NAME, "sMUprd")
        #Released on
        release_str = None
        for dts in deteils:
            if dts.text.__contains__("Released on"):
                release_str = dts.text.replace("Released on\n", "")
                dt = datetime.strptime(release_str, '%b %d, %Y')
                return dt
    return None

def checking_similar_apps(bundleID = "", level = 0, browser:webdriver = None): 
    browser.get("https://play.google.com/store/apps/details?id="+ bundleID +"&hl=en&gl=US")
    title_div: List[WebElement] = browser.find_elements(By.CLASS_NAME, "Fd93Bb")
    title = None
    if(len(title_div) > 0):
        title = title_div[0].text
    interval_installs = { 
        '0+'   : [1, 5],
        '1+'   : [1, 5],
        '5+'   : [6, 10],
        '10+'  : [11, 50],
        '50+'  : [51, 100],
        '100+' : [101, 500],
        '500+' : [501, 1000],
        '1K+'  : [1001, 5000],
        '5K+'  : [5001, 10000],
        '10K+' : [10001, 50000],
        '50K+' : [50001, 100000],
        '100K+': [100001, 500000],
        '500K+': [500001, 1000000],
        '1M+'  : [1000001, 5000000],
        '5M+'  : [5000001, 10000000],
        '10M+' : [10000001, 50000000],
        '50M+' : [50000001, 100000000],
        '100M+': [100000001, 500000000],
        '500M+': [500000001, 1000000000],
        '1B+'  : [1000000001, 5000000000],
        '5B+'  : [5000000001, 10000000000],
        '10B+' : [10000000001, 50000000000],
    }
    installs: List[WebElement] = browser.find_elements(By.CLASS_NAME, "wVqUob")
    installs_str = None
    for ins in installs:
        if(ins.text.__contains__("Downloads")):
            installs_str = ins.text.replace("\nDownloads", "")
    interval = None
    if(installs_str != None):
        interval = interval_installs.get(installs_str, [0, 0])
    elements:List[WebElement] = browser.find_elements(By.CLASS_NAME, "WpHeLc")
    app = None 
    button = find_element_by_attribute_value(elements, "aria-label", "See more information on Similar apps")
    if(button == None):
        button = find_element_by_attribute_value(elements, "aria-label", "See more information on Similar games")
    if(button != None):
        button.click()
        time.sleep(2)
        elements:List[WebElement] = browser.find_elements(By.CLASS_NAME, "Si6A0c")
        links = []
        for el in elements:
            href = el.get_attribute("href")
            if (not links.__contains__(href)) and (href != None and href.startswith("https://play.google.com/store/apps/details?id=")):
                links.append(href)
        for e in links: 
            print(e)
        if(title != None and len(links) > 0 and interval != None):    
            app = App(
                    link="https://play.google.com/store/apps/details?id="+ bundleID,
                    name=title, 
                    installs=interval, 
                    similar_list=links,
                    level=level
                )
                                                                                                               
    return app

def find_element_by_attribute_value(elements:List[WebElement], attribute_name:str, attribute_value:str) -> WebElement:
    for el in elements:
        attr = el.get_attribute(attribute_name)
        if(attr != None and attr.lower() == attribute_value.lower()):
            return el
    return None