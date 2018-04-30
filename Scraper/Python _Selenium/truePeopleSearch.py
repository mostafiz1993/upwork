import csv
import time
import datetime
from selenium import webdriver

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')

def generate_csv(name,address,telephone,email,writer):
    try:
        writer.writerow({'Name' : name, 'Address' : address, 'PhoneNo': telephone,'Email': email})
    except:
        print 'csv write problem'

def parse_each_person(url,browser,writer):
    try:
        name = 'N/A'
        address = 'N/A'
        telephone = []
        email = []
        browser.get(url)
        time.sleep(30)
        browser.get(url)
        try:
            if browser.find_element_by_xpath("//span[@class='h2']"):
                name = browser.find_element_by_xpath("//span[@class='h2']").text
        except:
            pass
        try:
            if browser.find_element_by_xpath("//a[@data-link-to-more='address']"):
                address = browser.find_element_by_xpath("//a[@data-link-to-more='address']").text
        except:
            pass
        try:
            emailDivs = browser.find_elements_by_class_name('content-label')
            for emailDiv in emailDivs:
                if 'Email Addresses' in emailDiv.text:
                    print emailDiv.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..")
                    emails = emailDiv.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_elements_by_class_name('content-value')
                    for e in emails:
                        email.append(e.text)
        except:
            pass
        try:
            if browser.find_elements_by_xpath("//a[@data-link-to-more='phone']"):
                telephones = browser.find_elements_by_xpath("//a[@data-link-to-more='phone']")
                for t in telephones:
                    telephone.append(t.text)
        except:
            pass
        generate_csv(name, address, telephone,email, writer)
    except:
        print 'Problem Parsing'


def pagination(nextPageUrl,browser,writer):
    browser.get(nextPageUrl)
    searhResults = browser.find_elements_by_class_name('card')
    nextPageUrlFlag = 1
    try:
        nextPageUrl = browser.find_element_by_id('btnNextPage').get_attribute('href')
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
    i = 1
    for personUrl in personUrlList:
        if i == 1:
            i += 1
            continue
        time.sleep(4)
        parse_each_person(personUrl,browser,writer)
    if nextPageUrlFlag == 1:
        time.sleep(4)
        pagination(nextPageUrl,browser,writer)
    else:
        browser.close()


def create_csv(name):
    fieldnames = ['Name', 'Address', 'PhoneNo', 'Email']
    csvF = csv_file_name_generation(name)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    return writer


def parser(name,address,writer):
    path_to_chromedriver = '/home/mostafiz/Downloads/chrome/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get('https://www.truepeoplesearch.com/')

    print 'Waiting 30 seconds...'
    time.sleep(30)

    a = browser.get_cookies()

    [browser.add_cookie(b) for b in a]
    browser.get('https://www.truepeoplesearch.com/')
    formName = browser.find_element_by_name("Name")
    formAddress = browser.find_element_by_name("CityStateZip")
    formName.send_keys(name)
    formAddress.send_keys(address)
    browser.find_element_by_id("btnSubmit").click()
    time.sleep(3)
    #
    try:
        nextPageUrlFlag = 1
        searhResults = browser.find_elements_by_class_name('card')
        try:
            nextPageUrl = browser.find_element_by_id('btnNextPage').get_attribute('href')
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
        print nextPageUrl
        i = 1
        for personUrl in personUrlList:
            if (i == 1):
                i += 1
                continue
            parse_each_person(personUrl,browser,writer)
            time.sleep(4)
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
        print 'DOne'


with open('input.csv', "rb" ) as theFile:
    reader = csv.DictReader( theFile , delimiter="\t")
    writer = create_csv('TruePeopleSearch.csv')
    for line in reader:
        name = line['FIRSTNAME'] + ' ' + line['MIDDLENAME'] + ' ' + line['LASTNAME']
        address = line['ADDRESS'] + ' ' +  line['ADDRESS2LINE'] + ' ' + line['CITY'] + ' ' + line['STATE']
        parser(name,address,writer)




