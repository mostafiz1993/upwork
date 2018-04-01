import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import mechanize
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

path_to_chromedriver = '/home/mostafiz/Downloads/chrome/chromedriver' # change path as needed





def getSoap(url):
    try:
        page = urllib.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')


def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')



def generate_csv(category, name, price,writer):
    try:
        writer.writerow({'Category' : category, 'Name' : name, 'avg_price': price})
        #csvF.write(jobTitle + ',' + jobLocation + ',' + jobCompany + '\n')
    except:
        pass

#runParser('https://www.simplyhired.com/search?q=data+scientist&l=New+York','New York' ,'Etl developer','simplyhire.csv')

def parse_page(url,writer,category):
    print url
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get(url)
    username = browser.find_element_by_id("postcode5")
    password = browser.find_element_by_id("inputTxt2")
    # username.clear()
    # username.send_keys("11357")
    # password.clear()
    # password.send_keys("100")
    username.send_keys(Keys.CONTROL + "a")
    username.send_keys( '11357')
    #password.send_keys(Keys.CONTROL + "a")
    #password.send_keys( '100')
    #username.sendKeys(Keys.chord(Keys.CONTROL, "a"), "11357")
    #password.sendKeys(Keys.chord(Keys.CONTROL, "a"), "100");
    print 'no'
    #try:
    browser.find_element_by_id("button1").click()
    #time.sleep(2)
    alert = browser.switch_to.alert
    alert.accept()
    browser.find_element_by_id("button1").click()
    #time.sleep(2)
    alert = browser.switch_to.alert
    alert.accept()
    time.sleep(1)
    print browser.find_element_by_xpath("(//td[@class='p1h2'])[2]").text
#    print 'yo'

    if "Square Feet*" in browser.find_element_by_xpath("(//td[@class='p1h2'])[2]").text:
        password.send_keys(Keys.CONTROL + "a")
        password.send_keys( '100')
        browser.find_element_by_id("button1").click()
        #time.sleep(2)
        alert = browser.switch_to.alert
        alert.accept()
        time.sleep(1)
    price =  browser.find_element_by_id('s4').text
    name =  browser.find_element_by_class_name('p1h1').text
    generate_csv(category, name, price,  writer)
    browser.close()
        # alert = browser.switch_to.alert
        # alert.accept()

        #print("no alert")
    # password.send_keys(Keys.CONTROL + "a")
    # password.send_keys( '100')
    #print browser

    # alert = browser.switch_to_alert()
    # alert.accept()
    # browser.close()

    # br = mechanize.Browser()
    # br.open(url)
    # br.select_form(nr=0)
    # br.form.find_control(id = 'postcode5').__setattr__('value', '11357')
    # br.form.find_control(id='inputTxt2').__setattr__('value', '100')
    # #br.form['inpurtTxt2'] = '1'
    #
    # # Login
    # br.form.click
    # html = br.response().read()
    # soup1 = BeautifulSoup(html,'html.parser')
    # print soup1
    # #page_soup = getSoap(url)
    # print soup1.find_all('tr', {'class': 'sf6'})

    # Select the first (index zero) form

    #print page_soup


soup = getSoap('https://homewyse.com/services/index.html')
#print soup
prefix = 'https://homewyse.com'
categorys =  soup.find_all('div', attrs={'data-role': 'collapsible'})

fieldnames = ['Category','Name','avg_price']
csvF = csv_file_name_generation("output.csv")
writer = csv.DictWriter(csvF, fieldnames=fieldnames)
writer.writeheader()
for category in categorys:

    #print category.h2.text
    if category.h2.text == 'Flooring':
        subCategorys =  category.find_all('a')
        for subCategory in subCategorys:
            subCategoryUrl =  prefix + subCategory['href']
            parse_page(subCategoryUrl,writer,category.h2.text)
            #break
        #print 'yes'
