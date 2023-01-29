from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
import time
import sqlite3
from datetime import datetime
from datetime import timedelta

class Tracker_google_play():
    def __init__(self) -> None:
        options = FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
        #browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
        browser.implicitly_wait(3)
        browser.maximize_window()
        self.browser:webdriver.Firefox = browser
        pass

    def start(self, bundleId:str, gl:str, hl:str, keywords:List[str]) -> dict:
        self.bundleId:str = bundleId
        self.gl:str = gl
        self.hl:str = hl
        map_keywords = {}
        try:
            for k in keywords:
                self.browser.get("https://play.google.com/store/search?q="+ k +"&c=apps&hl=" + hl + "&gl=" + gl)
                print(k)

                apps = self.browser.find_elements(By.CLASS_NAME, "Si6A0c")

                links_recommended = []

                try:
                    recommended = self.browser.find_element(By.CLASS_NAME, "zuJxTd")
                    rapps = recommended.find_elements(By.CLASS_NAME, "Si6A0c")

                    for app in rapps:
                        link = app.get_attribute("href")
                        links_recommended.append(link)
                except Exception as e:
                    print("")

                apps_list = []

                for app in apps:
                    link = app.get_attribute("href")
                    if(not links_recommended.__contains__(link)):
                        try:
                            app_name = app.find_element(By.CLASS_NAME, "DdYX5").text
                            company = app.find_element(By.CLASS_NAME, "wMUdtb").text
                            apps_list.append({"link": link, "app_name": app_name, "company": company})
                        except:
                            break

                conteins_title = 0
                conteins_company = 0
                position = -1
                for index, app in enumerate(apps_list):
                    my_link = "https://play.google.com/store/apps/details?id=" + bundleId
                    if(app["link"] == my_link):
                        position = index
                    conteins_title += str(app["app_name"]).lower().count(k.lower())
                    conteins_company += str(app["company"]).lower().count(k.lower())

                map_keywords[k] = { 
                    "position": position,
                    "conteins_title": conteins_title,
                    "conteins_company": conteins_company,
                }
        except Exception as e:
            print(e.args)
        self.save_database_cache(map_keywords)
        return map_keywords
    
    def get_name_app(self, bundleId:str, hl:str, gl:str):
        self.browser.get("https://play.google.com/store/apps/details?id=" + bundleId + "&hl=" + hl + "&gl=" + gl)
        page_app: WebElement = self.browser.find_element(By.CLASS_NAME, "Fd93Bb")
        return page_app.text

    def close_browser(self):
        self.browser.quit()

    def save_database_cache(self, map:dict):
        #print(datetime.today() - timedelta(days=1))
        #select * from aso_tracker where date_track > STRFTIME('%Y-%m-%d %H:%M', "2023-01-28 22:28:00.898");
        con = sqlite3.connect("asolytics.db")
        con.execute("CREATE TABLE IF NOT EXISTS aso_tracker (id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT,  bundle_id TEXT, gl TEXT, hl TEXT, pos INT, date_track DATE);")
        cursor = con.cursor()
        data = []
        for keyword in map.items():
            data.append((keyword[0], self.bundleId, self.gl, self.hl, keyword[1]['position'], datetime.now()))
        if(len(data) > 0):
            cursor.executemany("INSERT INTO aso_tracker(keyword, bundle_id, gl, hl, pos, date_track) VALUES(?, ?, ?, ?, ?, ?);", data)
        con.commit()
        con.close()

    def history(self, map:dict) -> dict:
        res = {}
        con = sqlite3.connect("asolytics.db")
        cursor = con.cursor()
        for key in map.keys():
            for i in range(7):
                yesterday = datetime.today() - timedelta(days = i + 1)
                cursor.execute("SELECT * FROM aso_tracker WHERE date_track < ? AND gl LIKE ? AND hl LIKE ? AND bundle_id LIKE ? AND keyword = ? ORDER BY id DESC LIMIT 1", [yesterday, self.gl, self.hl, self.bundleId, key])
                rows = cursor.fetchall()
                for row in rows:
                    if(i == 0):
                        res[row[1]] = { "day1": row[5] }
                    else:
                        res[row[1]]["day{}".format(i+1)] = row[5]
        con.close()
        return res

    def check_history(self, day:int, hist:dict, keywords:List[str]) -> bool:
        for key in keywords:
            if hist.get(key, None) != None:
               if hist[key].get("day{}".format(day), None) != None:
                    return True
        return False

    def find_position_by_day(self, hist:dict, keyword:str, day:int) -> int:
        if hist.get(keyword, None) != None:
           if hist[keyword].get("day{}".format(day), None) != None:
             return hist[keyword]["day{}".format(day)]
        return -1

    def count_day_in_history(self, hist:dict, kaywords:List[str]) -> int:
        count = 0
        for i in range(1, 8):
            if(self.check_history(i, hist, kaywords)):
                count = i
        return count
