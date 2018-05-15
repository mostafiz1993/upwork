import csv
import time
import datetime
from selenium import webdriver
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36']


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



def parse_each_property(url,cookie,writer,user_agent_index,flag,path_to_chromedriver):
    if(flag):
        opts = Options()
        opts.add_argument(user_agent_list[(12-(user_agent_index%12))*(user_agent_index/12)])
        browser = webdriver.Chrome(executable_path=path_to_chromedriver,chrome_options=opts)
    browser.get(url)
    [browser.add_cookie(b) for b in cookie]

    time.sleep(2)
    print(pyautogui.position())
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
#opts = Options()
#opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4")
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get('https://www.google.com/')
browser.set_window_size(1920, 1080)
browser.get('https://www.zillow.com/homedetails/10052-Umberland-Pl-Boca-Raton-FL-33428/46509942_zpid/')
cookie = browser.get_cookies()
#parse_each_property('https://www.zillow.com/homedetails/10052-Umberland-Pl-Boca-Raton-FL-33428/46509942_zpid/',cookie,writer)
uagent_index = 0
i = 0
flag = False
with open('out_zillow.csv', "rb" ) as theFile:
    #reader = csv.DictReader( theFile )
    for line in theFile.readlines():
        url = line.strip().decode('utf-8')
        try:
            if (uagent_index%12) > 10:
                flag = True
                i += 1
                if (i>11):
                    i = 0
            else:
                flag = False

            parse_each_property(url,cookie,writer,i,flag,path_to_chromedriver)
            print('yes')
            uagent_index += 1

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







