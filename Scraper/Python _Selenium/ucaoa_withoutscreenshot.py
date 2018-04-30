import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import numpy as np
import imutils
import cv2

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')

def generate_csv(url,writer):
    try:
        writer.writerow({'url' : url})
    except:
        print ('csv write problem')


def generate_csv1(url,name,employername,phoneNo,website,writer):
    try:
        writer.writerow({'url' : url,'name' : name , 'employer' : employername,'PhoneNo' : phoneNo,'Website' : website})
    except:
        print ('csv write problem')




def create_csv(name):
    fieldnames = ['Name', 'Address', 'PhoneNo', 'Email']
    csvF = csv_file_name_generation(name)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    return writer


def parse_each_clinic(url,writer):
    # path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
    # browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get(url)
    time.sleep(1)
    #browser.set_window_size(1920,1080)
    try:
        name = browser.find_element_by_id('SpTitleBar').text
    except:
        name = 'N/A'
    try:
        employersName =  browser.find_element_by_id('tdEmployerName').text.strip()
        if '[ Map ]' in employersName:
            employersName = employersName.replace('[ Map ]','').strip()
    except:
        employersName = ''
    try:
        telweb = browser.find_element_by_id('tdWorkPhone').text
        telephone = telweb.replace('Visit Website »', '').strip()
        if 'Website' in telweb:
            website = browser.find_element_by_id('tdWorkPhone').find_element_by_tag_name('a').get_attribute('href')
        else:
            website = ''
    except:
        telephone =''
        website = ''
    try:
        workingHour =   browser.find_element_by_class_name('CstmFldVal').text
    except:
        workingHour = ''
    generate_csv1(url,name,employersName,telephone,website,writer)



# def parser():
#     fieldnames = ['url']
#     csvF = csv_file_name_generation('ucaoa.csv')
#     writer = csv.DictWriter(csvF, fieldnames=fieldnames)
#     writer.writeheader()
#     path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
#     browser = webdriver.Chrome(executable_path=path_to_chromedriver)
#     browser.get('http://ucaoa.site-ym.com/searchserver/people.aspx?id=FB47D646-BA01-48D3-99CA-BECE6B11487D&cdbid=&canconnect=0&canmessage=0&map=False&toggle=True&hhSearchTerms=')
#     #browser.maximize_window()
#     print 'Waiting 30 seconds...'
#     time.sleep(5)
#     allClinic = browser.find_elements_by_class_name('lineitem')
#     print allClinic
#     for clinic in allClinic:
#         url = clinic.find_element_by_tag_name('a').get_attribute('href')
#         generate_csv(url,writer)
#         print url
#     while(True):
#         pages = browser.find_element_by_class_name('DotNetPager').find_elements_by_tag_name('a')
#         for page in pages:
#             pageUrl = page.text
#             print pageUrl
#         browser.execute_script("window.scrollTo(0, 500);")
#         try:
#             nextPage = browser.find_element_by_class_name('DotNetPager').find_element_by_tag_name('span').find_element_by_xpath('following-sibling::a')
#             nextPage.click()
#             time.sleep(5)
#             allClinic = browser.find_elements_by_class_name('lineitem')
#             print allClinic
#             for clinic in allClinic:
#                 url = clinic.find_element_by_tag_name('a').get_attribute('href')
#                 generate_csv(url,writer)
#                 print url
#         except:
#             break
#     browser.close()



    # a = browser.get_cookies()
    #
    # [browser.add_cookie(b) for b in a]
    # browser.get('https://www.truepeoplesearch.com/')
    #formName = browser.find_element_by_class_name("geosuggest").find_element_by_tag_name('input')

    #formAddress = browser.find_element_by_name("CityStateZip")
    #formName.send_keys('New York')
    #time.sleep(2)
    #formName = browser.find_element_by_class_name("geosuggest").find_elements_by_tag_name('li')[0].click
    #formAddress.send_keys(address)
    #print browser.find_element_by_tag_name('form').find_element_by_xpath("//input[@type='submit']").get_attribute('class')

    # browser.find_element_by_class_name('unIvGtQP').find_element_by_tag_name('form').click()
    #browser.find_element_by_tag_name('form').find_element_by_xpath("//input[@type='submit']").click()
    #browser.find_element_by_tag_name('form').find_element_by_xpath("//input[@type='submit']").click()
    #time.sleep(2)
    #
    # try:
    #     nextPageUrlFlag = 1
    #     searhResults = browser.find_elements_by_class_name('card')
    #     try:
    #         nextPageUrl = browser.find_element_by_id('btnNextPage').get_attribute('href')
    #     except:
    #         nextPageUrlFlag = 0
    #     print len(searhResults)
    #     personUrlList = []
    #     for searhResult in searhResults:
    #         try:
    #             url = searhResult.find_element_by_tag_name('a').get_attribute('href')
    #             personUrlList.append(url)
    #         except:
    #             pass
    #     print personUrlList
    #     print nextPageUrl
    #     i = 1
    #     for personUrl in personUrlList:
    #         if (i == 1):
    #             i += 1
    #             continue
    #         parse_each_person(personUrl,browser,writer)
    #         time.sleep(4)
    #     if nextPageUrlFlag == 1:
    #         time.sleep(4)
    #         pagination(nextPageUrl,browser,writer)
    #     else:
    #         browser.close()
    # except:
    #     pass
    # try:
    #     browser.close()
    # except:
    #     print 'DOne'

fieldnames = ['url','name','employer','PhoneNo','Website']
csvF = csv_file_name_generation('ucaoa.csv')
writer = csv.DictWriter(csvF, fieldnames=fieldnames)
writer.writeheader()
path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get('https://www.google.com/')
browser.set_window_size(1920,1080)
with open('ucaoa.csv', "rb" ) as theFile:
    #reader = csv.DictReader( theFile )
    for line in theFile.readlines():
        url = line.strip().decode('utf-8')
        try:
            parse_each_clinic(url,writer)
        except:
            pass

#parser()



