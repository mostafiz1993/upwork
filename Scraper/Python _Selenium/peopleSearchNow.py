import csv
import time
import datetime
from selenium import webdriver

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')

def generate_csv(name,address,telephone,otherTelephone,householdIncome,currentHomeValue,writer):
    try:
        writer.writerow({'Name' : name, 'Address' : address, 'PhoneNo': telephone, 'OtherPhoneNo': otherTelephone,
                         'HouseholdIncome': householdIncome, 'CurrentHomeValue': currentHomeValue})
    except:
        print 'csv write problem'


def parse_each_person(url,browser,writer):
    try:
        browser.get(url)
        details = browser.find_elements_by_class_name('result-full-info-block')
        print len(details)
        name = 'N/A'
        address = 'N/A'
        telephone = []
        otherTelephone = []
        householdIncome = 'N/A'
        currentHomeValue = 'N/A'
        for detail in details:
            try:
                if detail.find_element_by_tag_name('h1'):
                    name = detail.find_element_by_tag_name('h1').text
            except:
                pass
            try:
                if detail.find_element_by_xpath("//span[@itemprop='address']"):
                    address = detail.find_element_by_xpath("//span[@itemprop='address']").text
            except:
                pass
            try:
                if 'Current Phone:' in detail.find_element_by_tag_name('p').text:
                    telephones = detail.find_elements_by_tag_name('a')
                    for t in telephones:
                        telephone.append(t.find_element_by_xpath("//span[@itemprop='telephone']").text)
            except:
                pass
            try:
                if 'Other Phone Numbers:' in detail.find_element_by_tag_name('p').text:
                    otherTelephones = detail.find_elements_by_tag_name('a')
                    for t in otherTelephones:
                        otherTelephone.append(t.text)
            except:
                pass
            try:
                if 'Household Income:' in detail.find_element_by_tag_name('p').text:
                    householdIncome = detail.find_element_by_class_name(
                        'result-full-info-content').find_element_by_tag_name('p').text
            except:
                pass
            try:
                if 'Estimated Current Home Value:' in detail.find_element_by_tag_name('p').text:
                    currentHomeValue = detail.find_element_by_class_name(
                        'result-full-info-content').find_element_by_tag_name('p').text
            except:
                pass

        print telephone
        generate_csv(name, address, telephone, otherTelephone, householdIncome, currentHomeValue, writer)
    except:
        print 'Problem Parsing'


def pagination(nextPageUrl,browser,writer):
    browser.get(nextPageUrl)
    searhResults = browser.find_elements_by_class_name('result-search-block')
    nextPageUrlFlag = 1
    try:
        nextPageUrl = browser.find_element_by_class_name('paginator-next').get_attribute('href')
    except:
        nextPageUrlFlag = 0
    print len(searhResults)
    personUrlList = []
    for searhResult in searhResults:
        try:
            url = searhResult.find_element_by_tag_name('a').get_attribute('href')
            personUrlList.append(url)
        except:
            pass
    print personUrlList
    for personUrl in personUrlList:
        time.sleep(4)
        parse_each_person(personUrl,browser,writer)
    if nextPageUrlFlag == 1:
        time.sleep(4)
        pagination(nextPageUrl,browser,writer)
    else:
        browser.close()

def create_csv(name):
    fieldnames = ['Name', 'Address', 'PhoneNo', 'OtherPhoneNo', 'HouseholdIncome','CurrentHomeValue']
    csvF = csv_file_name_generation(name)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    return writer


def parser(name,address,writer):
    path_to_chromedriver = '/home/mostafiz/Downloads/chrome/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get('https://www.peoplesearchnow.com/')

    print 'Waiting 10 seconds...'
    time.sleep(10)
    a = browser.get_cookies()
    print a

    [browser.add_cookie(b) for b in a]
    browser.get('https://www.peoplesearchnow.com/')
    print browser.find_element_by_class_name('main-title').text
    formName = browser.find_element_by_name("name")
    formAddress = browser.find_element_by_name("address")
    formName.send_keys(name)
    formAddress.send_keys(address)
    browser.find_element_by_name("search-fio").click()
    time.sleep(3)

    try:
        nextPageUrlFlag = 1
        searhResults = browser.find_elements_by_class_name('result-search-block')
        try:
            nextPageUrl = browser.find_element_by_class_name('paginator-next').get_attribute('href')
        except:
            nextPageUrlFlag = 0
        print len(searhResults)
        personUrlList = []
        for searhResult in searhResults:
            try:
                url = searhResult.find_element_by_tag_name('a').get_attribute('href')
                personUrlList.append(url)
            except:
                pass
        print personUrlList
        for personUrl in personUrlList:
            time.sleep(4)
            parse_each_person(personUrl,browser,writer)
        if nextPageUrlFlag == 1:
            time.sleep(4)
            pagination(nextPageUrl,browser,writer)
        else:
            browser.close()
    except:
        pass
    try:
        browser.close()
    except:
        print 'Done'

with open('input.csv', "rb" ) as theFile:
    reader = csv.DictReader( theFile , delimiter="\t")
    writer = create_csv('PeopleSearchNow.csv')
    for line in reader:
        name = line['FIRSTNAME'] + ' ' + line['MIDDLENAME'] + ' ' + line['LASTNAME']
        address = line['ADDRESS'] + ' ' +  line['ADDRESS2LINE'] + ' ' + line['CITY'] + ' ' + line['STATE']
        parser(name,address,writer)



