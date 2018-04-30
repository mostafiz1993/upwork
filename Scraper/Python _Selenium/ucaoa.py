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


def parse_each_clinic(url,writer):
    # path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
    # browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get(url)
    # browser.set_window_size(1920,1080)
    try:
        name = browser.find_element_by_id('SpTitleBar').text
    except:
        name = ''
    try:
        lastUpdated = browser.find_element_by_class_name('deemphasize').find_element_by_tag_name('span').text.replace(
            'Last updated: ', '')
    except:
        lastUpdated = ''
    try:
        email = browser.find_element_by_class_name('deemphasize').find_element_by_xpath('..').find_element_by_tag_name(
            'a').text
    except:
        email = ''
    try:
        allInfo = browser.find_element_by_class_name('deemphasize').find_element_by_xpath('..').text
        if lastUpdated != '':
            allInfo = allInfo.replace(
                browser.find_element_by_class_name('deemphasize').find_element_by_tag_name('span').text, '')
        allInfo = allInfo.replace(
            browser.find_element_by_class_name('deemphasize').find_element_by_xpath('..').find_element_by_class_name(
                'big').text, '')
        if email != '':
            allInfo = allInfo.replace(email, '')
        companyType = allInfo.strip()
    except:
        companyType = ''

    try:
        employersName = browser.find_element_by_id('tdEmployerName')
        allInfo1 = employersName.text
        allhref = employersName.find_elements_by_tag_name('a')
        city = ''
        state = ''
        country = ''
        address1 = ''
        address2 = ''
        for href in allhref:
            if 'txt_city' in href.get_attribute('href'):
                try:
                    city = href.text
                except:
                    city = ''
            if 'txt_state' in href.get_attribute('href'):
                try:
                    state = href.text
                except:
                    state = ''
            if 'txt_country' in href.get_attribute('href'):
                try:
                    country = href.text
                except:
                    country = ''
        if city != '':
            allInfo1 = allInfo1.replace(city, '')
        if state != '':
            allInfo1 = allInfo1.replace(state, '')
        if country != '':
            allInfo1 = allInfo1.replace(country, '')
        if '[ Map ]' in allInfo1:
            allInfo1 = allInfo1.replace('[ Map ]', '')
        try:
            zipAndAddress = allInfo1.strip()
            try:
                zipAndAddress = zipAndAddress.replace(
                    browser.find_element_by_class_name('deemphasize').find_element_by_xpath(
                        '..').find_element_by_class_name('big').text, '')
            except:
                pass
            zA = zipAndAddress.split('\n')
            zA = [item for item in zA if item != '']
            if (len(zA) > 1):
                address1 = zA[0]
            if (len(zA) > 2):
                address2 = zA[1]
            zip = zA[-1]
            print(zA)
            print(zip)
            print(address1)
            print(address2)
        except:
            zip = ''
    except:
        city = ''
        state = ''
        country = ''
        zip = ''
    try:
        telweb = browser.find_element_by_id('tdWorkPhone').text
        try:
            telephone = telweb.replace('Visit Website »', '').strip()
        except:
            telephone = telweb
        try:
            officePhone = telephone[0:telephone.rfind('(Phone)') + 7]
        except:
            officePhone = ''
        try:
            officeFax = telephone[telephone.rfind('(Phone)') + 7:]
        except:
            officeFax = ''
        if 'Website' in telweb:
            website = browser.find_element_by_id('tdWorkPhone').find_element_by_tag_name('a').get_attribute('href')
        else:
            website = ''

    except:
        officeFax = ''
        officePhone = ''
        website = ''
    try:
        workingHour = browser.find_element_by_class_name('CstmFldVal').text
    except:
        workingHour = ''

    try:
        hospitalOwnedorAffiliated = ''
        hoursOfOperation = ''
        UCAOACertifiedUrgentCareIssued = ''
        certificationValidThrough = ''
        aboutTheCompany = ''
        companyCategories = ''
        CstmFldRows = browser.find_elements_by_class_name('CstmFldRow')
        for CstmFldRow in CstmFldRows:
            if 'Hospital Owned/Affiliated?:' in CstmFldRow.find_element_by_tag_name('label').text:
                try:
                    hospitalOwnedorAffiliated = CstmFldRow.find_element_by_class_name('CstmFldVal').text
                except:
                    hospitalOwnedorAffiliated = ''
            if 'Hours of Operation:' in CstmFldRow.find_element_by_tag_name('label').text:
                try:
                    hoursOfOperation = CstmFldRow.find_element_by_class_name('CstmFldVal').text
                except:
                    hoursOfOperation = ''
            if 'UCAOA Certified Urgent Care Issued:' in CstmFldRow.find_element_by_tag_name('label').text:
                try:
                    UCAOACertifiedUrgentCareIssued = CstmFldRow.find_element_by_class_name('CstmFldVal').text
                except:
                    UCAOACertifiedUrgentCareIssued = ''
            if 'Certification Valid Through:' in CstmFldRow.find_element_by_tag_name('label').text:
                try:
                    certificationValidThrough = CstmFldRow.find_element_by_class_name('CstmFldVal').text
                except:
                    certificationValidThrough = ''
            if 'Description:' in CstmFldRow.find_element_by_tag_name('label').text:
                try:
                    aboutTheCompany = CstmFldRow.find_element_by_class_name('CstmFldVal').text
                except:
                    aboutTheCompany = ''
            if 'Categories:' in CstmFldRow.find_element_by_tag_name('label').text:
                try:
                    companyCategories = CstmFldRow.find_element_by_class_name('CstmFldVal').text
                except:
                    companyCategories = ''
    except:
        pass

    # if 'Website' in telweb:
    #     try:
    #         web =  browser.find_element_by_id('tdWorkPhone').find_element_by_tag_name('a').get_attribute('href')
    #         browser.get(web)
    #         time.sleep(1)
    #         image = pyautogui.screenshot()
    #         image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    #         cv2.imwrite('Screenshots/' + name + ".png", image)
    #     except:
    #         pass
    generate_csv1(name,officePhone,officeFax,website,email,lastUpdated,companyType,hospitalOwnedorAffiliated,
              hoursOfOperation,UCAOACertifiedUrgentCareIssued,certificationValidThrough,aboutTheCompany,
              companyCategories,city,state,country,zip,address1,address2,url,writer)



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

fieldnames = ['name','officePhone','Officefax','Website','Email','lastUpdated','companyType','hospitalOwnedorAffiliated',
              'hoursOfOperation','UCAOACertifiedUrgentCareIssued','certificationValidThrough','aboutTheCompany',
              'companyCategories','city','state','country','zip','Address1','Address2','url']
csvF = csv_file_name_generation('ucaoa.csv')
writer = csv.DictWriter(csvF, fieldnames=fieldnames)
writer.writeheader()
path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get('https://www.google.com/')
browser.set_window_size(1920,1080)
# with open('ucaoa_new2.csv', "rb" ) as theFile:
#     #reader = csv.DictReader( theFile )
#     for line in theFile.readlines():
#         url = line.strip().decode('utf-8')
#         try:
#             parse_each_clinic(url,writer)
#         except:
#             pass

parse_each_clinic('http://ucaoa.site-ym.com/members/?id=51877684',writer)

#parser()



