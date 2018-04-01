import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

path_to_chromedriver = '/home/mostafiz/Downloads/chrome/chromedriver' # change path as needed




def generate_csv(category, name, avgTag, price,writer):
    try:
        print category + name + price
        writer.writerow({'Category' : category, 'Name' : name, 'avg_tag' : avgTag, 'high_avg_price': price})
    except:
        print 'problem'
        pass


browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get('https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=data&sc.keyword=Data+Scientist&locT=C&locId=1132348&jobType=')
jobLinks = browser.find_elements_by_class_name("jobLink")
for joblink in jobLinks:
    print joblink.get_attribute('href')

# postCode = browser.find_element_by_id("postcode5")
# parameter = browser.find_element_by_id("inputTxt2")
# postCode.send_keys(Keys.CONTROL + "a")
# postCode.send_keys( '11357')
# browser.find_element_by_id("button1").click()
# alert = browser.switch_to.alert
# alert.accept()
# browser.find_element_by_id("button1").click()
# alert = browser.switch_to.alert
# alert.accept()
# if "Square Feet*" in browser.find_element_by_xpath("(//td[@class='p1h2'])[2]").text:
#     try:
#         parameter.send_keys(Keys.CONTROL + "a")
#         parameter.send_keys( '100')
#         browser.find_element_by_id("button1").click()
#         alert = browser.switch_to.alert
#         alert.accept()
#     except:
#         pass
# else:
#     try:
#         parameter.send_keys(Keys.CONTROL + "a")
#         parameter.send_keys('1')
#         browser.find_element_by_id("button1").click()
#         # time.sleep(2)
#         alert = browser.switch_to.alert
#         alert.accept()
#     except:
#         pass
# table = browser.find_element_by_class_name('tout')
# try:
#     rows = table.find_elements_by_xpath("//tr[starts-with(@id ,'r')]")
#     for row in rows:
#         try:
#             checkbox = row.find_element_by_tag_name('i')
#             if checkbox.get_attribute('class') == 'ix fa fa-check-square-o fa-lg':
#                 checkbox.click()
#             if 'labor' in row.text.lower():
#                 checkbox.click()
#         except:
#             pass
#     time.sleep(1)
#     try:
#         price =  table.find_element_by_id('s4').text
#     except:
#         price = 'N/A'
#     try:
#         name =  browser.find_element_by_class_name('p1h1').text
#     except:
#         name = 'N/A'
#     try:
#         avgTag = table.find_element_by_class_name('sf6').find_element_by_class_name('sf1').text
#     except:
#         avgTag = 'N/A'
#     generate_csv(category, name, avgTag, price, writer)
# except:
#     pass
browser.close()




