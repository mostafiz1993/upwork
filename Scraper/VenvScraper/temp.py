import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import numpy as np
import imutils
import cv2

def parse_each_clinic(url):
    path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get(url)
    #browser.set_window_size(1920,1080)
    try:
        name = browser.find_element_by_id('SpTitleBar').text
    except:
        name = ''
    try:
        lastUpdated = browser.find_element_by_class_name('deemphasize').find_element_by_tag_name('span').text.replace('Last updated: ','')
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
            allInfo = allInfo.replace(browser.find_element_by_class_name('deemphasize').find_element_by_tag_name('span').text,'')
        allInfo = allInfo.replace(browser.find_element_by_class_name('deemphasize').find_element_by_xpath('..').find_element_by_class_name('big').text,'')
        if email != '':
            allInfo = allInfo.replace(email,'')
        companyType = allInfo.strip()
    except:
        companyType = ''


    try:
        employersName =  browser.find_element_by_id('tdEmployerName')
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
        if city  != '':
            allInfo1 = allInfo1.replace(city,'')
        if state != '':
            allInfo1 = allInfo1.replace(state, '')
        if country != '':
            allInfo1 = allInfo1.replace(country, '')
        if '[ Map ]' in allInfo1:
            allInfo1 = allInfo1.replace('[ Map ]', '')
        try:
            zipAndAddress = allInfo1.strip()
            try:
                zipAndAddress = zipAndAddress.replace(browser.find_element_by_class_name('deemphasize').find_element_by_xpath('..').find_element_by_class_name('big').text,'')
            except:
                pass
            zA = zipAndAddress.split('\n')
            zA = [item for item in zA if item != '']
            if (len(zA) > 1):
                address1 = zA[0]
            if (len(zA) > 2):
                address2 = zA[1]
            zip = zA[-1]
            print (zA)
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
            officeFax = telephone[telephone.rfind('(Phone)')+7:]
        except:
            officeFax = ''
        if 'Website' in telweb:
            website = browser.find_element_by_id('tdWorkPhone').find_element_by_tag_name('a').get_attribute('href')
        else:
            website = ''

    except:
        officeFax =''
        officePhone = ''
        website = ''
    try:
        workingHour =   browser.find_element_by_class_name('CstmFldVal').text
    except:
        workingHour = ''

    try:
        hospitalOwnedorAffiliated =''
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
    print(name)
    print(officePhone)
    print(officeFax)
    print(website)
    print(lastUpdated)
    print (companyType)
    print(email)
    print(hospitalOwnedorAffiliated)
    print(hoursOfOperation)
    print(UCAOACertifiedUrgentCareIssued)
    print(certificationValidThrough)
    print(aboutTheCompany)
    print(companyCategories)
    print(city)
    print(state)
    print(country)
    print(zip)

parse_each_clinic('http://ucaoa.site-ym.com/members/?id=51877684')