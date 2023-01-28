from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
import time
from urllib.parse import urlparse, parse_qs

class Tag():
    def __init__(self, name:str, link:str) -> None:
        self.name:str = name
        self.link:str = link
        pass

    def check_search_tag(self) -> bool:
        return self.link.startswith("https://play.google.com/store/search")

    def type_tag(self) -> str:
        if self.link.startswith("https://play.google.com/store/search"):
            return "Пошуковий"
        elif self.link.startswith("https://play.google.com/store/apps/category/"):
            return "Категорійний"
        else:
            return "Невідомий"

    def get_keyword(self) -> str:
        if(self.check_search_tag()):
            urp = urlparse(self.link)
            mq = parse_qs(urp.query)
            lst = mq.get("q", "")
            if len(lst) > 0:
                return lst[0]
            else:
                return ""
        else:
            return ""

class App_tags():
    def __init__(self, bundle_id:str, tags:List[Tag]) -> None:
        self.bundle_id:str = bundle_id
        self.tags:List[Tag] = tags
        pass

    def position(self, keyword) -> int:
        if self.tags.__contains__(keyword):
            return self.tags.index(keyword)
        return -1

class Google_play_tags():

    all_apps_tags:List[App_tags] = []
    tags_app_index = {}
    count_apps_all = 0

    def start(self, bundleID:str, gl:str, hl:str) -> set:
        options = FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
        #browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
        browser.implicitly_wait(3)
        browser.maximize_window()

        my_tags = self.get_tags(browser, bundleID, gl, hl)
        at = App_tags(bundleID, my_tags)
        self.all_apps_tags.append(at)
        app_links:List[str] = self.get_similar_links(browser, bundleID, gl)
        self.count_apps_all = len(app_links)
        for i, l in enumerate(app_links):
            b_id = l.replace("https://play.google.com/store/apps/details?id=", "")
            ts = self.get_tags(browser, b_id, gl, hl)
            self.all_apps_tags.append(App_tags(b_id, ts))
            print("[ {} / {} ]".format((i +1), len(app_links)))

        all_tags:set[str] = set()
        for aat in self.all_apps_tags:
            for t_str in aat.tags: all_tags.add(t_str.name)
        
        for t in all_tags:
            self.tags_app_index[t] = self.app_indexing(browser, gl, hl, t, bundleID)

        browser.quit()
        return all_tags

    def get_index_tag(self, keyword:str) -> int:
        return self.tags_app_index.get(keyword, -1)
    
    def app_indexing(self, browser:webdriver.Firefox, gl:str, hl:str, keyword:str, bundleId:str):
        tag = self.find_by_name(keyword)
        if tag != None:
            if(tag.check_search_tag()): 
                browser.get("{}&hl={}&gl={}".format(tag.link, hl, gl))
            else:
                browser.get("{}?hl={}&gl={}".format(tag.link, hl, gl))
            web_links:List[WebElement] = browser.find_elements(By.CLASS_NAME, "Si6A0c")
            for i, link in enumerate(web_links):
                link = link.get_attribute("href")
                if(link == "https://play.google.com/store/apps/details?id={}".format(bundleId)):
                    print("{} [ {} / {} ]".format(keyword, True, (i + 1)))
                    return i + 1
            print("{} [ {} ]".format(keyword, False))
        return -1
    
    def find_by_name(self, keyword:str) -> Tag:
        for app in self.all_apps_tags: 
            for tag in app.tags:
                if(tag.name == keyword):
                    return tag
        return None

    def average_position(self, keyword:str) -> float:
        num = []
        for app in self.all_apps_tags:
                    for i, tag in enumerate(app.tags):
                        if(tag.name == keyword):
                            num.append(i + 1)
        if(len(num) > 0):
           return round(sum(num) / len(num), 1)
        return -1

    def count_apps(self, keyword:str) -> int:
        count = 0
        for app in self.all_apps_tags:
                    for i, tag in enumerate(app.tags):
                        if(tag.name == keyword):
                            count += 1
        return count


    def get_tags(self, browser:webdriver.Firefox, bundleID:str, gl:str, hl:str) -> List[Tag]:
        tags:List[Tag] = []
        try:
            browser.get("https://play.google.com/store/apps/details?id={}&hl={}&gl={}".format(bundleID, hl, gl))
            tags_web_block:List[WebElement] = browser.find_elements(By.CLASS_NAME, "Uc6QCc")
            if(len(tags_web_block) > 0):
                elements:List[WebElement] = tags_web_block[0].find_elements(By.CLASS_NAME, "WpHeLc")
                for el in elements:
                    tag = Tag(el.get_attribute("aria-label"), el.get_attribute("href"))
                    print(el.get_attribute("aria-label"))
                    tags.append(tag)
        except Exception as e:
            print(e.args)
        return tags

    def get_similar_links(self, browser:webdriver.Firefox, bundleID:str, gl:str) -> List[str]:
        links = []
        try:
            browser.get("https://play.google.com/store/apps/details?id={}&hl=en&gl={}".format(bundleID, gl))
            elements:List[WebElement] = browser.find_elements(By.CLASS_NAME, "WpHeLc")
            button = self.find_element_by_attribute_value(elements, "aria-label", "See more information on Similar apps")
            if(button == None):
                button = self.find_element_by_attribute_value(elements, "aria-label", "See more information on Similar games")
            if(button != None):
                button.click()
                time.sleep(2)
                elements:List[WebElement] = browser.find_elements(By.CLASS_NAME, "Si6A0c")
                for el in elements:
                    href = el.get_attribute("href")
                    if (not links.__contains__(href)) and (href != None and href.startswith("https://play.google.com/store/apps/details?id=")):
                        links.append(href)
        except Exception as e:
            print(e.args)
        return links

    def find_element_by_attribute_value(self, elements:List[WebElement], attribute_name:str, attribute_value:str) -> WebElement:
        for el in elements:
            attr = el.get_attribute(attribute_name)
            if(attr != None and attr.lower() == attribute_value.lower()):
                return el
        return None