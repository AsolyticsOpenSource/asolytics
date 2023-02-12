from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
import time

class App_reviews():
    def __init__(self, hl:str, reviews:List[str], rates:List[float], pub_dates:List[str], dev_response:List[str]) -> None:
        self.hl:str = hl
        self.reviews:List[str] = reviews
        self.rates:List[float] = rates
        self.pub_dates:List[str] = pub_dates
        self.dev_response:List[str] = dev_response
        pass

class Featured_reviews():

    #https://support.google.com/googleplay/android-developer/answer/9844778?hl=en#zippy=%2Cview-list-of-available-languages

    locals = [
        "af",
        "sq",
        "am",
        "ar",
        "hy-AM",
        "az-AZ",
        "bn-BD",
        "eu-ES",
        "be",
        "bg",
        "my-MM",
        "ca",
        "zh-HK",
        "zh-CN",
        "zh-TW",
        "hr",
        "cs-CZ",
        "da-DK",
        "nl-NL",
        "en-IN",
        "en-SG",
        "en-ZA",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-US",
        "et",
        "fil",
        "fi-FI",
        "fr-CA",
        "fr-FR",
        "gl-ES",
        "ka-GE",
        "de-DE",
        "el-GR",
        "gu",
        "iw-IL",
        "hi-IN",
        "hu-HU",
        "is-IS",
        "id",
        "it-IT",
        "ja-JP",
        "kn-IN",
        "kk",
        "km-KH",
        "ko-KR",
        "ky-KG",
        "lo-LA",
        "lv",
        "lt",
        "mk-MK",
        "ms",
        "ms-MY",
        "ml-IN",
        "mr-IN",
        "mn-MN",
        "ne-NP",
        "no-NO",
        "fa",
        "fa-AE",
        "fa-AF",
        "fa-IR",
        "pl-PL",
        "pt-BR",
        "pt-PT",
        "pa",
        "ro",
        "rm",
        "ru-RU",
        "sr",
        "si-LK",
        "sk",
        "sl",
        "es-419",
        "es-ES",
        "es-US",
        "sw",
        "sv-SE",
        "ta-IN",
        "te-IN",
        "th",
        "tr-TR",
        "uk",
        "ur",
        "vi",
        "zu"
    ]

    def start(self, bundleId) -> List[App_reviews]:
        options = FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
        #browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
        browser.implicitly_wait(3)
        browser.maximize_window()
        list_ar:List[App_reviews] = []
        for index, hl in enumerate(self.locals):
            print("({} / {})".format(index + 1, len(self.locals)))
            ar = self.get_reviews(browser, bundleId, hl)
            if(ar != None):
                list_ar.append(ar)
            #break

        browser.quit()
        return list_ar

    def get_reviews(self, browser:webdriver.Firefox, bundleId:str, hl:str) -> App_reviews:
        ar:App_reviews = None
        try:
            hls = hl.split("-")
            if len(hls) > 1:
                browser.get("https://play.google.com/store/apps/details?id=" + bundleId + "&hl=" + hl + "&gl=" + hls[1])
            else:
                browser.get("https://play.google.com/store/apps/details?id=" + bundleId + "&hl=" + hl)
            elements = browser.find_elements(By.CLASS_NAME, "EGFGHd")
            reviews_list:List[str] = []
            rates_list:List[str] = []
            pub_dates:List[str] = []
            dev_response:List[str] = []
            for el in elements:
                web_text:List[WebElement] = el.find_elements(By.CLASS_NAME, "h3YV2d")
                web_rate:List[WebElement] = el.find_elements(By.CLASS_NAME, "Z1Dz7b")
                web_pub_dates:List[WebElement] = el.find_elements(By.CLASS_NAME, "bp9Aid")
                web_dev_response:List[WebElement] = el.find_elements(By.CLASS_NAME, "ras4vb")
                if(len(web_text) > 0):
                    reviews_list.append(web_text[0].text)
                    rates_list.append(len(web_rate))
                    pub_dates.append(web_pub_dates[0].text)
                    if len(web_dev_response) > 0:
                        dev_response.append(web_dev_response[0].text)
                    else:
                        dev_response.append("")
                    print("({}) Rate: ".format(hl) + str(len(web_rate)))
            ar = App_reviews(hl,reviews_list, rates_list, pub_dates, dev_response)
        except Exception as e:
            print(e.args)
        return ar