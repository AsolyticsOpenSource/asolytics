from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import os
import time
import argparse
import sys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from prettytable import PrettyTable, ALL
from typing import List
from decimal import Decimal
from datetime import datetime
from colorama import Fore
import yake
#tabulate, regex, networkx, jellyfish, segtok, yake
import statistics
try:
    from asolytics.similar import App, parser_similar
    from asolytics.local import Localization_of_naming
    from asolytics.reviews import App_reviews, Featured_reviews
    from asolytics.tags import Tag, Google_play_tags, App_tags
    from asolytics.tracker import Tracker_google_play
    from asolytics.extract import Extract_keywords
except:
    from similar import App, parser_similar
    from local import Localization_of_naming
    from reviews import App_reviews, Featured_reviews
    from tags import Tag, Google_play_tags, App_tags
    from tracker import Tracker_google_play
    from extract import Extract_keywords

parser = argparse.ArgumentParser()
parser.add_argument('--key', dest='key', type=str, help='search keyword as the parameter')
parser.add_argument('--hl', dest='hl', type=str, help='Enter the language code')
parser.add_argument('--gl', dest='gl', type=str, help='country')
parser.add_argument('--trends', dest='trends', action='store_true', help='Analysis of trending keys in Google Play')
parser.add_argument('--average', dest='average', type=str, help='Average number of downloads / ratings per day (--average org.telegram.messenger)')

parser.add_argument('--tracker', dest='tracker', type=str, help='Track the position of the application in the search (--tracker "quizzes; zombie games; online shooters")')
parser.add_argument('--id', dest='id', type=str, help='Bundle ID - the application that needs to be tracked')
parser.add_argument('--file', dest='file', action='store_true', help='Use this key if the --tracker option points to a keyword file (each key must be on a newline)')
parser.add_argument('--extract', dest='extract', type=str, help='Identify keywords used in application metadata. The title, developer name, short description, full description, reviews are analyzed. (--extract org.telegram.messenger)')
parser.add_argument('--similar', dest='similar', type=str, help='Analysis of similar applications. Use this key to analyze the pages of your competitors where you appear in similar ones (--similar org.telegram.messenger)')
parser.add_argument('--local', dest='local', type=str, help='Analysis of naming localization. Languages into which the Google Play application page is translated (--local org.thoughtcrime.securesms)')
parser.add_argument('--reviews', dest='reviews', type=str, help='Analyze recorded reviews in different locales. Reviews that are in the top (--reviews org.thoughtcrime.securesms)')
parser.add_argument('--csv', dest='csv', type=str, help='Use this option to save the result to a file, csv can be opened with spreadsheets like Excel (--csv file.csv)')
parser.add_argument('--tags', dest='tags', type=str, help='Tag analysis tool in Google Play, checking the indexing of the application by tags (--tags org.thoughtcrime.securesms)')

args = parser.parse_args()

options = FirefoxOptions()
options.add_argument("--headless")
#browser = webdriver.Firefox(executable_path="/users/krv/driver/geckodriver", options=options)

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def tags_analysis(bundleId):
    print(Fore.GREEN + "* * * I will do it * * *" + Fore.WHITE)
    print("Bundle ID: " + bundleId)
    if args.hl != None:
        hl = args.hl
        print("Language code: " + hl)
    else:
        hl = "en"
        print("Language code: " + hl)

    if args.gl != None:
        gl = args.gl
        print("Country code: " + gl)
    else:
        gl = "US"
        print("Country code: " + gl)

    gpt = Google_play_tags()
    tag_labels = gpt.start(bundleId, gl, hl)

    x = PrettyTable()
    x.field_names = ["Tag", "The type tag", "The key tag", "Significance for the cluster", "Number of applications", "Indexing by tag"]

    for tag_label in tag_labels:
        tag = gpt.find_by_name(tag_label)
        x.add_row([
            tag_label,
            tag.type_tag(),
            tag.get_keyword(),
            gpt.average_position(tag_label), 
            gpt.count_apps(tag_label),
            gpt.get_index_tag(tag_label)
        ])
    x.hrules = ALL
    x._max_width["Tag"] = 30
    x._max_width["The key tag"] = 30
    print(x.get_string(sortby=("Significance for the cluster")))

    if(args.csv != None):
        save_to_file_csv(x, args.csv)

    print("All applications have been analyzed: {}".format(gpt.count_apps_all))
    print("* * * done! * * *")

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def reviews_analysis(bundleId):
    print(Fore.GREEN + "* * * I will do it * * *" + Fore.WHITE)
    print("Bundle ID: " + bundleId)
    fr = Featured_reviews()
    elements = fr.start(bundleId)

    x = PrettyTable()
    x.field_names = ["Google Play locale", "Publication date" ,"Response", "Rating", "Developer response"]

    all_rate = []
    for element in elements:
        for i, review in enumerate(element.reviews):
            x.add_row([element.hl, element.pub_dates[i], review, element.rates[i], element.dev_response[i]])
            all_rate.append(element.rates[i])
    x.hrules = ALL
    x._max_width["Response"] = 50
    x._max_width["Developer response"] = 40
    print(x.get_string(sortby=("Google Play locale")))
    if(len(all_rate) > 0):
        print("Average score for the feedback feature: " + str(round(sum(all_rate) / len(all_rate), 1)))

    if(args.csv != None):
        save_to_file_csv(x, args.csv)

    print("* * * done! * * *")

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def localization_analysis(bundleId):
    print(Fore.GREEN + "* * * I will do it * * *" + Fore.WHITE)
    print("Bundle ID: " + bundleId)
    lon = Localization_of_naming()
    elements = lon.start(bundleId)

    x = PrettyTable()
    x.field_names = ["Google Play locale", "The name of the application", "The language used"]
    names = []
    for element in elements:
        x.add_row([element[0], element[1], element[2]])
        names.append(element[1])
    print(x.get_string(sortby=("The language used")))
    list_set = set(names)
    unique_list = (list(list_set))
    print("Number of languages used: " + str(len(unique_list)))
    if(args.csv != None):
        save_to_file_csv(x, args.csv)
    print("* * * done! * * *")
    return

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def action_parser_similar_app(bundleId):
    print(Fore.GREEN + "* * * I will do it * * *" + Fore.WHITE)
    print(Fore.RED + "The process of data collection and analysis can be lengthy..." + Fore.WHITE)
    apps = parser_similar(bundleId)
    
    x = PrettyTable()
    x.field_names = ["The name of the application / Bundle ID", "Your position is similar", "Number of downloads", "Downloads per day"]

    pos = []
    ins_x1 = []
    ins_x2 = []
    ins_x1_daily = []
    ins_x2_daily = []
    for item in apps.values():
        item:App = item
        if(item.simular_position(bundleId) != -1):
            x1 = 0
            x2 = 0
            if(item.release_date != None):
                seconds = datetime.now().timestamp() - item.release_date.timestamp()
                days = seconds / (24 * 3600)
                x1 = int(item.installs[0] / days)
                x2 = int(item.installs[1] / days)
            x.add_row([item.name + "\n" + item.link.replace("https://play.google.com/store/apps/details?id=", ""),  
                item.simular_position(bundleId) + 1, 
                "from " + str(item.installs[0]) + " to " + str(item.installs[1]), 
                "from " + str(x1) + " to " + str(x2)])
            pos.append(item.simular_position(bundleId) + 1)
            ins_x1.append(item.installs[0])
            ins_x2.append(item.installs[1])
            ins_x1_daily.append(x1)
            ins_x2_daily.append(x2)
    x.hrules = ALL
    print(x.get_string(sortby=("Your position is similar")))
    print("Analyzed taxes: " + str(len(apps.values())))
    if(len(pos) > 0):
        print("Average position in selections: " + str(round(sum(pos) / len(pos))))
        print("Median positions in selections of similar to dats: " + str(statistics.median(pos)))
        print("Aaverage number of installs to applications on the pages of which you are offended: from " + str(int(sum(ins_x1) / len(ins_x1))) + " to " + str(int(sum(ins_x2) / len(ins_x2))))
        print("The average number of installs to data per tobu, on the pages of which you from are offended: from " + str(int(sum(ins_x1_daily) / len(ins_x1_daily))) + " to " + str(int(sum(ins_x2_daily) / len(ins_x2_daily))))
    else:
        print("Your to data is nowhere from offended in similar!")
    if(args.csv != None):
        save_to_file_csv(x, args.csv)
    print("* * * done! * * *")
    return

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def extract_keywords_metadata_app(bundleId):

    if args.hl != None:
        hl = args.hl
        print("Language code: " + hl)
    else:
        hl = "en"
        print("Language code: " + hl)

    if args.gl != None:
        gl = args.gl
        print("Country code: " + gl)
    else:
        gl = "US"
        print("Country code: " + gl)

    
    ek = Extract_keywords()

    keywords = ek.strat(bundleId, hl, gl)

    valid_keys = ek.position_validator(keywords, bundleId, hl, gl)

    ek.browser_exit()

    x = PrettyTable()
    x.field_names = ["Key phrase", "Significance in the text", "Search position"]

    for item in valid_keys:
        x.add_row([item[0], item[1], item[2]])

    print(x.get_string(sortby=("Search position")))

    print("Number of keywords found: " + str(len(valid_keys)))
    print("Metadata indexing factor (country - " + gl +"; language - " + hl +"): "
         + str(int(100 * len(valid_keys)/len(keywords))) + "%")

    if(args.csv != None):
        save_to_file_csv(x, args.csv)

    print("* * * done! * * *")

    return

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def tracker_position_google_play():

    if(args.id == None): 
        print("You must specify the bundle ID of the application (--id org.telegram.messenger)")
        return
    else:
        bundleId = args.id

    if args.hl != None:
        hl = args.hl
        print("Language code: " + hl)
    else:
        hl = "en"
        print("Language code: " + hl)

    if args.gl != None:
        gl = args.gl
        print("Country code: " + gl)
    else:
        gl = "US"
        print("Country code: " + gl)

    tgp = Tracker_google_play()

    try :
        name = tgp.get_name_app(bundleId, hl, gl)
        print(Fore.GREEN + "Application name: " + name + Fore.WHITE)
    except:
        print("An application with this bundleID ("+ bundleId +") not found on Google Play")
        tgp.close_browser()
        return

    if(not args.file):
        keywords = args.tracker.split(";")
            
    else:
        keywords = []
        try:
            path = args.tracker
            file = open(path, "r", encoding='utf-8')
            for keyword in file:
                keywords.append(keyword.replace("\n", ""))
            file.close()
        except Exception as e:
            print(e.args)

    if(len(keywords) == 0):
        tgp.close_browser()
        return

    map_keywords = tgp.start(bundleId, gl, hl, keywords)

    x = PrettyTable()
    history = tgp.history(map_keywords)
    count_days_in_history = tgp.count_day_in_history(history, map_keywords.keys())
    if count_days_in_history > 0:
        x.field_names = ["Key phrase", "Search position", "Position yesterday", "Has changed", "Entries in names", "Login in the name of the developer"]

        for item in map_keywords.items():
            position_day1 = tgp.find_position_by_day(history, item[0], 1)
            x.add_row([item[0], 
                item[1]["position"] + 1,
                position_day1 + 1, 
                ((item[1]["position"] + 1) - (position_day1 + 1)) * (1 if position_day1 > -1 else -1) * (1 if item[1]["position"] == -1 else -1),
                item[1]["conteins_title"], 
                item[1]["conteins_company"]])
    else:
        x.field_names = ["Key phrase", "Search position", "Entries in names", "Login in the name of the developer"]

        for item in map_keywords.items():
            x.add_row([item[0], item[1]["position"] + 1, item[1]["conteins_title"], item[1]["conteins_company"]])

    print(x.get_string(sortby=("Search position")))

    x1 = PrettyTable()
    if count_days_in_history > 0:
        #x.field_names = ["Key phrase", "Search position", "Has changed", "Entries in names", "Login in the name of the developer"]
        header = ["Key phrase"]
        for i in range(count_days_in_history, 0, -1): header.append("День {}".format(i))
        header.append("Search position")
        header.append("Has changed")
        header.append("Entries in names")
        header.append("Login in the name of the developer")
        x1.field_names = header

        for item in map_keywords.items():
            position_day1 = tgp.find_position_by_day(history, item[0], 1)
            row = [item[0]]
            for i in range(count_days_in_history, 0, -1): row.append(tgp.find_position_by_day(history, item[0], i) + 1)
            row.append(item[1]["position"] + 1)
            row.append(((item[1]["position"] + 1) - (position_day1 + 1)) * (1 if position_day1 > -1 else -1) * (1 if item[1]["position"] == -1 else -1))
            row.append(item[1]["conteins_title"])
            row.append(item[1]["conteins_company"])
            x1.add_row(row)
    else:
        x1.field_names = ["Key phrase", "Search position", "Entries in names", "Login in the name of the developer"]
        for item in map_keywords.items():
            x1.add_row([item[0], item[1]["position"] + 1, item[1]["conteins_title"], item[1]["conteins_company"]])

    if(args.csv != None):
        save_to_file_csv(x1, args.csv)

    print("* * * done! * * *")

    tgp.close_browser()
    return

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def average_install_in_Google_Play(bundleID, gl):

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

    print("I will perform an analysis...")

    #, options=options
    browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
    browser.implicitly_wait(10)
    browser.maximize_window()

    browser.get("https://play.google.com/store/apps/details?id=" + bundleID + "&hl=en&gl=" + gl)

    page_app: WebElement = browser.find_element(By.CLASS_NAME, "Fd93Bb")

    print(Fore.GREEN + "Application name: " + page_app.text + Fore.WHITE)

    review_value = 0
    
    try:
        review: WebElement = browser.find_element(By.CLASS_NAME, "EHUI5b")

        review_str = review.text.replace("reviews", "")

        if review_str.__contains__("K"):
            review_value = Decimal(review_str.replace("K", "")) * 1000
        elif review_str.__contains__("M"):
            review_value = Decimal(review_str.replace("M", "")) * 1000000
        elif review_str.__contains__("B"):
            review_value = Decimal(review_str.replace("B", "")) * 1000000000
        else:
            review_value = Decimal(review_str)

        print("Total number of reviews: " + str(review_value))
    except:
        print("Total number of reviews: " + str(review_value))

    installs: List[WebElement] = browser.find_elements(By.CLASS_NAME, "wVqUob")

    installs_str = None
    for ins in installs:
        if(ins.text.__contains__("Downloads")):
            installs_str = ins.text.replace("\nDownloads", "")

    if(installs_str != None):
        interval = interval_installs.get(installs_str, [0, 0])
        print("Total number of downloads: from " + str(interval[0]) + " to " + str(interval[1]))

    button_deteils: List[WebElement] = browser.find_elements(By.CLASS_NAME, "VfPpkd-Bz112c-LgbsSe")
    
    button_deteils.pop(5).click()

    time.sleep(4)

    deteils: List[WebElement] = browser.find_elements(By.CLASS_NAME, "sMUprd")

    #Released on
    #release_str = deteils.pop(7)
    release_str = None
    for dts in deteils:
        if dts.text.__contains__("Released on"):
            release_str = dts.text.replace("Released on\n", "")
            break
        
    if(release_str == None):
        browser.quit()
        return

    dt = datetime.strptime(release_str, '%b %d, %Y')

    seconds = datetime.now().timestamp() - dt.timestamp()
    days = seconds / (24 * 3600)

    x1 = int(interval[0] / days)
    x2 = int(interval[1] / days)
    print("Average number of downloads per day: from " + str(x1) +" to " + str(x2))

    print("Average number of ratings per day: " + str(int(review_value / Decimal(days))))

    browser.get("https://app.sensortower.com/overview/com.facebook.home?os=android&country=US&tab=about")

    time.sleep(5)

    inputs: List[WebElement] = browser.find_elements(By.CLASS_NAME, "BaseInput-module__input--NDkTj")

    search = None

    for se in inputs:
        if se.get_attribute("placeholder") == "Search for an app...":
            search = se

    if search == None:
        browser.quit()
        return

    search.click()
    search.send_keys(bundleID)

    time.sleep(25)
    
    item = browser.find_element(By.CLASS_NAME, "BaseAutocomplete-module__option--OiqfD")
    strs = item.text.split("\n")

    revenue_str = strs[-1]

    if(revenue_str.__contains__("<")):
        text = "The foreign currency revenue of the application for the last month is less: "
        revenue_str = revenue_str.replace("<", "")
    elif(revenue_str.__contains__(">")):
        text = "The foreign currency revenue of the application for the last month is more: "
        revenue_str = revenue_str.replace(">", "")
    else:
        text = "The foreign currency revenue of the application for the last month is approximately: "

    revenue_str = revenue_str.replace("$", "")

    if revenue_str.__contains__("K"):
        revenue_str = Decimal(revenue_str.replace("K", "")) * 1000
    elif revenue_str.__contains__("M"):
        revenue_str = Decimal(revenue_str.replace("M", "")) * 1000000
    elif revenue_str.__contains__("B"):
        revenue_str = Decimal(revenue_str.replace("B", "")) * 1000000000
    else:
        revenue_str = Decimal(revenue_str)

    print(text + str(revenue_str) + "$")

    #print(item.text)

    item.click()

    #BaseStatistic-module__statistic--swhHO
    statistics: List[WebElement] = browser.find_elements(By.CLASS_NAME, "BaseStatistic-module__statistic--swhHO")

    countries = None
    for stat in statistics:
        if(stat.text.__contains__("Top Countries / Regions")):
            countries = stat.text.replace("Top Countries / Regions\n", "")
            countries = countries.replace("\n,\n", ", ").replace("Russia", "Russian Terrorist State")
            break

    if(countries == None):
        browser.quit()
        return

    print("Countries from which the application receives the most traffic: " + countries)

    #MuiListItem-root
    release_deteils: List[WebElement] = browser.find_elements(By.CLASS_NAME, "MuiListItem-root")

    publisher_country = None

    for rd in release_deteils:
        if(rd.text.__contains__("Publisher Country:")):
            publisher_country = rd.text.replace("Publisher Country:\n", "")
        
    if(publisher_country != None):
        print("Country of Origin: " + publisher_country)

    print('* * * done! * * *')

    browser.quit()

    return 

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def trends_google_play(gl, hl): 

    if hl == "uk":
        alphabet = "абвгґдеєжзіїйклмнопрстуфхцчшщюя"
    elif hl == "ru":
        alphabet = "абвгдежзиклмнопрстуфхцчшщэюя"
    elif hl == "pl":
        alphabet = "aąbсćdеęfghijklłmnńoóprsśtuwyzźż"
    elif hl == "de":
        alphabet = "abcdefghijklmnopqrstuvwxyzäöüß"
    elif hl == "en":
        alphabet = "abcdefghijklmnopqrstuvwxyz"
    elif hl == "es":
        alphabet = "abcdefghiklmnñopqrstuvwxyz"
    elif hl == "cs":
        alphabet = "aábcčdďeéěfghciíjklmnňoópqrřsštťuúůvwxyýzž"
    elif hl == "el":
        alphabet = "αβγδεζηθικλμνξοπρσςτυφχψω"
    elif hl == "it":
        alphabet = "abcdefghilmnopqrstuvzùúòóìíèéà"
    else:
        print(hl + " - this language is not yet supported")
        sys.exit(0)

    # alphabet = "abcdefghijklmnopqrstuvwxyz"

    map_popularity = {}    

    print(Fore.GREEN + "* * * I perform trend analysis... * * *" + Fore.WHITE)

    browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
    browser.implicitly_wait(10)
    browser.maximize_window()

    for char in alphabet:
        browser.get("https://play.google.com/store/search?q="+ char +"&c=apps&hl=" + hl + "&gl=" + gl)
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, "HWAcU").clear()
        browser.find_element(By.CLASS_NAME, "HWAcU").send_keys(char)
        suggests = browser.find_elements(By.CLASS_NAME, "YVhSle")
        minus = 0
        for s in suggests:
            el: WebElement = s
            key = el.get_attribute("data-display-text")
            map_popularity[key] = 6 - minus
            minus += 1

    x = PrettyTable()
    x.field_names = ["Key phrase", "Relative popularity"]

    for item in map_popularity.items():
        x.add_row([item[0], item[1]])

    print(x.get_string(sortby=("Relative popularity"), reversesort=True)) 
    print("Collected keywords: " + str(len(map_popularity)))
    if(args.csv != None):
        save_to_file_csv(x, args.csv)
    print("* * * Completed! * * *")

    browser.quit()
            
    return

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def save_to_file_csv(x:PrettyTable, path:str):
    try:
        with open(path, 'w', newline='', encoding='utf-8') as f_output:
            f_output.write(x.get_csv_string())
        f_output.close()
        print("Збережено в файл: {}".format(os.path.abspath(path)))
    except Exception as e:
        print(e.args)

###################################################################################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###################################################################################################################

def main():
    if(args.tags != None):
        tags_analysis(args.tags)
        sys.exit()

    if(args.reviews != None):
        reviews_analysis(args.reviews)
        sys.exit()

    if(args.local != None):
        localization_analysis(args.local)
        sys.exit()

    if(args.similar != None):
        action_parser_similar_app(args.similar)
        sys.exit()

    if(args.extract != None):
        extract_keywords_metadata_app(args.extract)
        sys.exit()

    if(args.tracker != None):
        tracker_position_google_play()
        sys.exit()

    if args.average != None:
        if args.gl != None:
            gl = args.gl
            print("Country code: " + gl)
        else:
            gl = "US"
            print("Country code: " + gl)
        average_install_in_Google_Play(args.average, gl)
        sys.exit()

    if args.hl != None:
        hl = args.hl
        print("Language code: " + hl)
    else:
        hl = "en"
        print("Language code: " + hl)

    if args.gl != None:
        gl = args.gl
        print("Country code: " + gl)
    else:
        gl = "US"
        print("Country code: " + gl)

    if args.trends:
        trends_google_play(gl, hl)
        sys.exit(0)
    elif args.key != None:
        print(Fore.GREEN + "I will perform the analysis... " + args.key + Fore.WHITE)
        keyword = args.key
    else:
        print("Specify the key for analysis (--key 'yoga at home')")
        sys.exit(0)

    #&hl=ru&gl=US

    browser = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options=options)
    browser.implicitly_wait(10)
    browser.maximize_window()

    browser.get("https://play.google.com/store/search?q="+ keyword +"&c=apps&hl=" + hl + "&gl=" + gl)

    time.sleep(1)
    browser.find_element(By.CLASS_NAME, "HWAcU").clear()

    browser.find_element(By.CLASS_NAME, "HWAcU").send_keys(keyword)

    suggests = browser.find_elements(By.CLASS_NAME, "YVhSle")

    list1 = []
    map = {}
    map_popularity = {}

    map[keyword] = True
    map_popularity[keyword] = 100
    print(keyword)

    minus = 0
    for s in suggests:
        el: WebElement = s
        key = el.get_attribute("data-display-text")
        if key != keyword:
            print(key)
            list1.append(key)
            map[key] = False
            map_popularity[key] = 100 - minus
            minus += 2


    def google_suggests(lst, level):

        res = []
        for sug in lst:
    
            if map.get(sug, False) == False:
                browser.get("https://play.google.com/store/search?q="+ sug +"&c=apps")
                map[sug] = True

                time.sleep(1)
                browser.find_element(By.CLASS_NAME, "HWAcU").clear()

                browser.find_element(By.CLASS_NAME, "HWAcU").send_keys(sug)

                suggests = browser.find_elements(By.CLASS_NAME, "YVhSle")

                minus = 0
                for s in suggests:
                    el: WebElement = s
                    key = el.get_attribute("data-display-text")
                    print(key)
                    if map.get(key, None) == None:
                        res.append(key)
                        map[key] = False
                        if map_popularity.get(key, None) == None:
                            map_popularity[key] = level - minus
                    minus += 2   

        return res

    list2 = google_suggests(list1, 70)
    list3 = google_suggests(list2, 50)
    list4 = google_suggests(list3, 20)
    list5 = google_suggests(list4, 15)

    x = PrettyTable()
    x.field_names = ["Key phrase", "Relative popularity"]

    for item in map_popularity.items():
        x.add_row([item[0], item[1]])

    print(x.get_string(sortby=("Relative popularity"), reversesort=True))    

    print("Key popularity criterion (" + keyword + ") / The number of derivative suggestions: " + str(len(map)))

    if(args.csv != None):
        save_to_file_csv(x, args.csv)
    print("* * * Completed! * * *")

    browser.quit()

if __name__ == "__main__":
    main()