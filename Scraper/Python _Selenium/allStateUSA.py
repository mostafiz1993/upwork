import csv
import time
import datetime
from selenium import webdriver
import pyautogui
from selenium.webdriver.common.keys import Keys




def parser():
    # fieldnames = ['url']
    # csvF = csv_file_name_generation('ucare.csv')
    # writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    # writer.writeheader()
    path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get('https://www.google.com/')
    browser.set_window_size(1920, 1080)
    browser.get('https://simple.wikipedia.org/wiki/List_of_United_States_cities_by_population')
    print ('Waiting 10 seconds...')
    #go_to_nextpage(browser,writer)
    allCityInUSA = []
    trs = browser.find_element_by_class_name('mw-parser-output').find_element_by_class_name('wikitable').find_elements_by_tag_name('tr')
    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        for td in tds:
            try:
                print(td.find_element_by_tag_name('a').text)
                city = td.find_element_by_tag_name('a').text
                allCityInUSA.append(city)
                break
            except:
                pass
    print(allCityInUSA)

parser()


