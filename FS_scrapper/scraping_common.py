import requests
import selenium
import random
import datetime
import json
import argparse
import csv
import os
from sys import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_chromedriver(use_proxy=False, user_agent=None, headless=False, 
                        images=False):
    """Returns a Chrome WebDriver using proxies and user-agent if specified.
    """
    chrome_options = webdriver.chrome.options.Options()
    if use_proxy:
        myProxy = '127.0.0.1:24000'
        chrome_options.add_argument('--proxy-server=%s' % myProxy)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=2560x1440')
    else:
        chrome_options.add_argument('--start-maximized')
    if not images:
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    if platform == 'linux':
        driver = webdriver.Chrome(options=chrome_options)
    if platform == 'win32':
        driver = webdriver.Chrome(options=chrome_options, executable_path=
            r'C:/Users/odar/Documents/Programming/chromedriver_win32 (74)'\
            r'/chromedriver.exe')
    return driver


def get_geckodriver(use_proxy=False, user_agent=None, headless=False, 
                        images=False):
    """Returns a Firefox WebDriver using proxies and user-agent if specified.
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.add_argument('--no-proxy-server')
    options.add_argument("--proxy-server='direct://'");
    options.add_argument("--proxy-bypass-list=*");

    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.panel.shown', False)
    profile.set_preference("browser.helperApps.neverAsk.openFile",
                           "text/csv,application/vnd.ms-excel") 
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                           "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.download.folderList", 2)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    profile.set_preference("browser.download.dir", dir_path)
    if platform == 'linux':
        driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
    if platform == 'win32':
        driver = webdriver.Firefox(executable_path=r'C:/Users/odar/Documents/Programming'\
            r'/geckodriver-v0.24.0-win64/geckodriver.exe', firefox_profile=profile,
            firefox_options=options)
    return driver


def dict_to_csv(dictionary, columns_data):
    """Saves a dictionary python object to csv format.
    """
    columns = columns_data
    
    try:
        with open('results.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for data in dictionary:
                writer.writerow(data)
    except IOError as ioe:
        print('Error saving results. \n {}'.format(ioe))


def dict_to_json(list_of_dicts, filename):
    """Saves a list of dictionaries Python objects to JSON format.
    """
    with open(filename, 'w') as json_file:
        json.dump(list_of_dicts, json_file, indent=4)


def get_user_agent():
    """Returns a random selected user agent from list.
    """
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like "\
            "Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, "\
            "like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like "\
            "Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) "\
            "Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like "\
            "Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Geck"\
            "o) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) "\
            "Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like "\
            "Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) "\
            "Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (K"\
            "HTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "\
            "Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like "\
            "Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "\
            "Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like "\
            "Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) "\
            "Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "\
            "Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gec"\
            "ko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like"\
            " Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "\
            "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/537.36 (KHTML, "\
            "like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gec"\
            "ko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 ("\
            "KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko)"\
            " Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gec"\
            "ko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like"\
            " Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "\
            "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    ]

    return random.choice(USER_AGENT_LIST)

    