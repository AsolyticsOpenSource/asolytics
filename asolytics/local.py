from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
import time
from langdetect import detect

class Localization_of_naming: 

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

    def get_title(self, browser:webdriver.Firefox, bundleId:str, language:str) -> str:
        title = None
        try:
            browser.get("https://play.google.com/store/apps/details?id=" + bundleId + "&hl=" + language)
            title_web = browser.find_elements(By.CLASS_NAME, "Fd93Bb")
            if(len(title_web) > 0):
                 title = title_web[0].text
        except Exception as e:
            print(e.args)
        return title

    def start(self, bundleId:str):
        options = FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
        #browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
        browser.implicitly_wait(3)
        browser.maximize_window()
        lst = []
        for hl in self.locals:
           title = self.get_title(browser, bundleId, hl)
           if(title != None):
                item = [hl, title, detect(title)]
                lst.append(item)
                print(item)
        browser.quit()
        return lst