import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')

def generate_csv(url,writer):
    try:
        writer.writerow({'url' : url})
    except:
        print ('csv write problem')


def generate_csv1(name,officePhone,Officefax,Website,Email,lastUpadetd,compnayType,hospitalOwnedorAffiliated,
              hoursOfOperation,UCAOACertifiedUrgentCareIssued,certificationValidThrough,aboutTheCompany,
              companyCategories,city,state,country,zip,address1,address2,url,writer):
    try:
        writer.writerow({'name' :name,'officePhone' :officePhone,'Officefax' :Officefax,'Website':Website,'Email':Email,
                         'lastUpdated':lastUpadetd,'companyType':compnayType,'hospitalOwnedorAffiliated':hospitalOwnedorAffiliated,
              'hoursOfOperation':hoursOfOperation,'UCAOACertifiedUrgentCareIssued':UCAOACertifiedUrgentCareIssued,
                         'certificationValidThrough':certificationValidThrough,'aboutTheCompany':aboutTheCompany,
              'companyCategories':companyCategories,'city':city,'state':state,'country':country,'zip':zip,
                         'Address1':address1,'Address2':address2,'url':url})
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
        try:bvbanaim
            url1 =  li.find_element_by_class_name('zsg-photo-card-overlay-link').get_attribute('href')
            print url1
            generate_csv(url1,writer)
        except:
            pass


fieldnames = ['url']
csvF = csv_file_name_generation('zillow.csv')
writer = csv.DictWriter(csvF, fieldnames=fieldnames)
writer.writeheader()

url = 'https://www.zillow.com/homes/fsbo/Palm-Beach-County-FL/house,townhouse_type/2993_rid/3-_beds/0-800000_price/0-3198_mp/mostrecentchange_sort/27.414443,-79.020538,25.998784,-80.896454_rect/8_zm/X1.dash.SS.dash.ik2z5tgz7y7p_5i268_sse/0_mmm/'
path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get(url)
time.sleep(10)
lis = browser.find_element_by_class_name('photo-cards').find_elements_by_tag_name('li')
for li in lis:
    try:
        url1 =  li.find_element_by_class_name('zsg-photo-card-overlay-link').get_attribute('href')
        print url1
        generate_csv(url1,writer)
    except:
        pass
    while(True):
        try:
            if browser.find_element_by_class_name('zsg-pagination-next'):
                browser.find_element_by_class_name('zsg-pagination-next').click()
                time.sleep(10)
                get_property(browser,writer)
            else:
                break
        except:
            break

#parse_each_clinic(url)




