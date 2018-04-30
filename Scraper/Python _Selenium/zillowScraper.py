import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')

def generate_csv(url,writer):
    try:
        writer.writerow({'url' : url})
    except:
        print ('csv write problem')


def generate_csv1(street,fullAddress,owner,url,writer):
    try:
        writer.writerow({'Street' : street, 'FullAddress' : fullAddress, 'Owner' : owner,'url':url})
    except:
        print ('csv write problem')





def create_csv(name):
    fieldnames = ['Name', 'Address', 'PhoneNo', 'Email']
    csvF = csv_file_name_generation(name)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    return writer


def parse_each_clinic(url):
    path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get(url)

def get_property(b,writer):
    lis = b.find_element_by_class_name('photo-cards').find_elements_by_tag_name('li')
    for li in lis:
        try:
            # print li
            # print li.text
            # hover = ActionChains(browser).move_to_element(li)
            # hover.perform()
            # time.sleep(1)
            url1 =  li.find_element_by_class_name('zsg-photo-card-overlay-link').get_attribute('href')
            print (url1)
            generate_csv(url1,writer)
        except:
            pass



def parse_each_property(url,cookie,writer):
    [browser.add_cookie(b) for b in cookie]
    browser.get(url)
    time.sleep(2)
    print(pyautogui.position())
    pyautogui.click(1354, 690)
    pyautogui.click(1354, 690)
    pyautogui.click(1354, 690)
    pyautogui.click(1354, 690)
    pyautogui.click(1354, 690)
    pyautogui.click(1354, 690)
    time.sleep(2)
    pyautogui.click(1354, 200)
    # browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)
    try:
        s = browser.find_element_by_class_name('addr_city').text
    except:
        s = ''
    try:
        a =browser.find_element_by_class_name('addr_city').find_element_by_xpath('..').text
    except:
        a = ''
    try:
        o = browser.find_element_by_id('listing-provided-by-module').find_element_by_tag_name('p').text
    except:
        o = ''
    generate_csv1(s,a,o,url,writer)
# fieldnames = ['url']
# csvF = csv_file_name_generation('zillow.csv')
# writer = csv.DictWriter(csvF, fieldnames=fieldnames)
# writer.writeheader()

# url = 'https://www.zillow.com/homedetails/10052-Umberland-Pl-Boca-Raton-FL-33428/46509942_zpid/'
# path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
# browser = webdriver.Chrome(executable_path=path_to_chromedriver)
# browser.get(url)
# browser.set_window_size(1920,1080)
# time.sleep(5)
# # elm = browser.find_element_by_tag_name('html')
# # elm.send_keys(Keys.END)
# # time.sleep(2)
# # elm.send_keys(Keys.HOME)
# print(pyautogui.position())
# pyautogui.click(1354, 631)
# pyautogui.click(1354, 631)
# pyautogui.click(1354, 631)
# pyautogui.click(1354, 631)
# pyautogui.click(1354, 631)
# pyautogui.click(1354, 631)
# #browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
# time.sleep(2)
#
# print (browser.find_element_by_class_name('addr_city').text)
# print (browser.find_element_by_class_name('addr_city').find_element_by_xpath('..').text)
# print (browser.find_element_by_id('listing-provided-by-module').find_element_by_tag_name('p').text)

fieldnames = ['Street', 'FullAddress', 'Owner', 'url']
csvF = csv_file_name_generation('zillow.csv')
writer = csv.DictWriter(csvF, fieldnames=fieldnames)
writer.writeheader()
path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get('https://www.google.com/')
browser.set_window_size(1920, 1080)
browser.get('https://www.zillow.com/homedetails/10052-Umberland-Pl-Boca-Raton-FL-33428/46509942_zpid/')
cookie = browser.get_cookies()
with open('out_zillow.csv', "rb" ) as theFile:
    #reader = csv.DictReader( theFile )
    for line in theFile.readlines():
        url = line.strip().decode('utf-8')
        try:
            parse_each_property(url,cookie,writer)
        except:
            pass

# time.sleep(10)
# lis = browser.find_element_by_class_name('photo-cards').find_elements_by_tag_name('li')
# for li in lis:
#     try:
#         #print li
#         #print li.text
#     # hover = ActionChains(browser).move_to_element(li)
#     # hover.perform()
#     # time.sleep(1)
#         url1 =  li.find_element_by_class_name('zsg-photo-card-overlay-link').get_attribute('href')
#         print url1
#         generate_csv(url1,writer)
#     except:
#         pass
#
#     while(True):
#         try:
#             if browser.find_element_by_class_name('zsg-pagination-next'):
#                 browser.find_element_by_class_name('zsg-pagination-next').click()
#                 time.sleep(10)
#                 get_property(browser,writer)
#             else:
#                 break
#         except:
#             break

#parse_each_clinic(url)




