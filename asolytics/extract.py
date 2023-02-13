from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
import time
import yake

class Extract_keywords:

    def __init__(self) -> None:
        self.options = FirefoxOptions()
        self.options.add_argument("--headless")
        self.browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=self.options)
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()
        pass

    def strat(self, bundleId:str, hl:str, gl:str) -> List[tuple]:
        
        #self.get_content(browser, bundleId, hl, gl)
        full_content = [self.get_content(self.browser, bundleId, hl, gl)]
        links = self.get_links(self.browser, bundleId)
        for i, link in enumerate(links):
            if i < 3:
                id = link.replace("https://play.google.com/store/apps/details?id=", "")
                str_content = self.get_content(self.browser, id, hl, gl)
                full_content.append(str_content)

        keywords = []
        for txt in full_content:
            keys = self.__keywords_extractor(txt, hl)
            for k in keys:
                if not self.conteins_keywords(keywords, k[0]):
                    keywords.append(k)

        return keywords

    def conteins_keywords(self, keywords:List[tuple], key:str) -> bool:
        for k in keywords:
            if(k[0] == key):
                return True
        return False

    def browser_exit(self):
        self.browser.quit()

    def get_links(self, browser:webdriver.Firefox, bundleId) -> List[str]:
        links = []
        try:
            browser.get("https://play.google.com/store/apps/details?id="+ bundleId +"&hl=en&gl=US")
            elements:List[WebElement] = browser.find_elements(By.CLASS_NAME, "WpHeLc")
            button = self.__find_element_by_attribute_value(elements, "aria-label", "See more information on Similar apps")
            if(button == None):
                button = self.__find_element_by_attribute_value(elements, "aria-label", "See more information on Similar games")
            if(button != None):
                button.click()
                time.sleep(2)
                browser.refresh()
                elements:List[WebElement] = browser.find_elements(By.CLASS_NAME, "Si6A0c")
                for el in elements:
                    href = el.get_attribute("href")
                    if (not links.__contains__(href)) and (href != None and href.startswith("https://play.google.com/store/apps/details?id=")):
                        links.append(href)
                for e in links: 
                    print(e)
        except Exception as e:
            print(e.args)
        return links

    def get_content(self, browser, bundleId:str, hl:str, gl:str):
        text = ""
        try:
            browser.get("https://play.google.com/store/apps/details?id=" + bundleId + "&hl=" + hl + "&gl=" + gl)
            web_title_app: WebElement = browser.find_element(By.CLASS_NAME, "Fd93Bb")
            title_app = web_title_app.text
   
            web_description_app: WebElement = browser.find_element(By.CLASS_NAME, "bARER")
            description_app = web_description_app.text

            elements = browser.find_elements(By.CLASS_NAME, "EGFGHd")
            text_review = ""
            for el in elements:
                web_text_review:List[WebElement] = el.find_elements(By.CLASS_NAME, "h3YV2d")
                if len(web_text_review) > 0:
                    text_review += web_text_review[0].text + " "

            web_dev_name: WebElement = browser.find_element(By.CLASS_NAME, "Vbfug")
            dev_name = web_dev_name.text

            text = "{} {} {} {}.".format(title_app, description_app, text_review, dev_name)
            print(title_app)
        except Exception as e:
            print("sssdasd err")
            print(e.args)
        return text

    def __find_element_by_attribute_value(self, elements:List[WebElement], attribute_name:str, attribute_value:str) -> WebElement:
        for el in elements:
            attr = el.get_attribute(attribute_name)
            if(attr != None and attr.lower() == attribute_value.lower()):
                return el
        return None

    def __keywords_extractor(self, full_text:str, hl:str) -> List[tuple]:
        language = hl
        max_ngram_size = 3
        deduplication_threshold = 0.9
        
        extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, features=None, top=100)
        list_keywords = extractor.extract_keywords(full_text)
        return list_keywords

    def position_validator(self, keywords, bundleId:str, hl:str, gl:str):
        relevant_keys = []
        for inx, x in enumerate(keywords):
            #time.sleep(1)
            self.browser.get("https://play.google.com/store/search?q="+ x[0] +"&c=apps&hl=" + hl + "&gl=" + gl)
            print(x)
            links: List[WebElement] = self.browser.find_elements(By.TAG_NAME, "a")

            for index, l in  enumerate(links):
                link = l.get_attribute("href")
                if( link == ("https://play.google.com/store/apps/details?id=" + bundleId)):
                    position = index - 5
                    print("{} / {}".format(position, inx))
                    relevant_keys.append([x[0], x[1], position])
        return relevant_keys