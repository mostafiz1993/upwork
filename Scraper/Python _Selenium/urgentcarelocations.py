import csv
import time
import datetime
from selenium import webdriver
import pyautogui
from selenium.webdriver.common.keys import Keys
import urllib

def csv_file_name_generation(csvFile):
    return open(csvFile, 'w')

def generate_csv(url,writer):
    try:
        writer.writerow({'url' : url})
    except:
        print ('csv write problem')

def generate_csv1(url,name,nameWithCity,dictHoursOfOperation,arrayAcceptedInsurances ,arrayCertification,acceptedPaymentType ,description ,
                  telephone ,servicesOfUC ,streetAddress ,city,state,zipCode, writer):

    try:
        writer.writerow(
            {'url':url,'name' : name,'nameWithCity' : nameWithCity,'HoursOfOperation' : dictHoursOfOperation,'AcceptedInsurances' : arrayAcceptedInsurances,
             'Certification' : arrayCertification,'acceptedPaymentType' : acceptedPaymentType ,'about' : description,
             'telephone' : telephone,'services' : servicesOfUC ,'streetAddress' : streetAddress ,
             'city' : city,'state': state,'zipCode' : zipCode })
    except:
        print('csv write problem')


def create_csv(name):
    fieldnames = ['Name', 'Address', 'PhoneNo', 'Email']
    csvF = csv_file_name_generation(name)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    return writer


def parse_each_uc(browser,url,writer):

    browser.get(url)
    print('Waiting 10 seconds...')
    time.sleep(0.3)
    pyautogui.click(1354, 690)
    #time.sleep(1)
    name = ''
    dictHoursOfOperation = {}
    arrayAcceptedInsurances = []
    arrayCertification = []
    acceptedPaymentType = ''
    description = ''
    telephone = ''
    servicesOfUC = {}
    streetAddress = ''
    city = ''
    state = ''
    zipCode = ''
    name = ''
    nameWithCity = ''
    try:
        name = browser.find_element_by_xpath('//h1[@itemprop= "name"]').text
    except:
        name = 'N/A'
    print(name)
    try:
        nCity = browser.find_element_by_class_name('city-state-title').text
        nameWithCity = name + ' ' + nCity
    except:
        nameWithCity = 'N/A'
    #print(name)
    try:
        streetAddress = browser.find_element_by_xpath('//span[@itemprop= "streetAddress"]').text
    except:
        streetAddress = 'N/A'
    #print(streetAddress)
    try:
        city = browser.find_element_by_xpath('//span[@itemprop= "addressLocality"]').text
    except:
        city = 'N/A'
    #print(city)
    try:
        state = browser.find_element_by_xpath('//span[@itemprop= "addressRegion"]').text
    except:
        state = 'N/A'
    #print(state)
    try:
        zipCode = browser.find_element_by_xpath('//span[@itemprop= "postalCode"]').text
    except:
        zipCode = 'N/A'
    #print(zipCode)
    try:
        h3s = browser.find_elements_by_tag_name('h3')
        for h3 in h3s:
            #print(h3.text)
            if h3.text == 'HOURS OF OPERATION':
                try:
                    hourOfoperations = h3.find_element_by_xpath('..').find_elements_by_tag_name('li')
                    for hourOfoperation in hourOfoperations:
                        #print(hourOfoperation.find_element_by_class_name('day').text)
                        #print(hourOfoperation.find_element_by_class_name('hour').text.strip())
                        dictHoursOfOperation[hourOfoperation.find_element_by_class_name('day').text] = hourOfoperation.find_element_by_class_name('hour').text.strip()
                except:
                    dictHoursOfOperation = {'N/A' : 'N/A'}
                #print(dictHoursOfOperation)

            if h3.text == 'ACCEPTED INSURANCES':
                try:
                    acceptedInsurances = h3.find_element_by_xpath('..').find_elements_by_tag_name('li')
                    for acceptedInsurance in acceptedInsurances:
                        arrayAcceptedInsurances.append(acceptedInsurance.text)
                except:
                    arrayAcceptedInsurances.append('N/A')
                #print(arrayAcceptedInsurances)

            if h3.text == 'ACCEPTED PAYMENT TYPES':
                try:
                    acceptedPaymentTypes = h3.find_element_by_xpath('..').find_elements_by_tag_name('div')
                    for acceptedPayment in acceptedPaymentTypes:
                        acceptedPaymentType += acceptedPayment.text
                except:
                    acceptedPaymentType = 'N/A'
                #print(acceptedPaymentType)
            if h3.text == 'CERTIFICATIONS AND ACCREDITATIONS':
                try:
                    certifications = h3.find_element_by_xpath('..').find_elements_by_tag_name('li')
                    for certification in certifications:
                        arrayCertification.append(certification.text)
                except:
                    arrayCertification.append( 'N/A')
                #print(arrayCertification)
    except:
        pass
    try:
        desTags = browser.find_element_by_class_name('overview').find_elements_by_tag_name('p')
        flag = 1
        for des in desTags:
            if flag == 0:
                break
            try:
                for href in des.find_elements_by_tag_name('a'):
                    #print(href.text)
                    if href.text =='more':
                        flag = 0
                        href.click()
                        time.sleep(0.1)
                        descriptions = browser.find_element_by_class_name('overview').find_elements_by_tag_name('p')
                        for descript in descriptions:
                            description += descript.text
                        break
            except:
                description = 'N/A'
        if flag == 1:
            descriptions = browser.find_element_by_class_name('overview').find_elements_by_tag_name('p')
            for descript in descriptions:
                description += descript.text
    except:
        description = 'N/A'
    #print(description)
    #print(description[-4:])
    try:
        if description[-4:] == 'less':
            description =  description[:-4]
    except:
        pass
    #pyautogui.click(1354, 690)
    #time.sleep(0.1)
    try:
        services = browser.find_elements_by_class_name('service-group')
        for service in services:
            #print(service.find_element_by_tag_name('h3').text)
            serviceName = service.find_element_by_tag_name('h3').text
            service.find_element_by_tag_name('h3').find_element_by_tag_name('i').click()
            subServicelists = service.find_element_by_class_name('list').find_elements_by_tag_name('li')
            subServices = ''
            for subServicelist in subServicelists:
                #print(subServicelist.text.strip())
                subServices += subServicelist.text.strip() + ','
            servicesOfUC[serviceName] = subServices[:-1]
    except:
        servicesOfUC['N/A'] = 'N/A'
    #print(servicesOfUC)

    try:
        browser.get(browser.find_element_by_class_name('contact').find_element_by_tag_name('a').get_attribute('href'))
        # time.sleep(2)
        telephone = browser.find_element_by_class_name('fa-phone').find_element_by_xpath('..').text
    except:
        telephone = 'N/A'
    #print(telephone)
    generate_csv1(url,name,nameWithCity, dictHoursOfOperation, arrayAcceptedInsurances, arrayCertification, acceptedPaymentType,
                  description,
                  telephone, servicesOfUC, streetAddress, city, state, zipCode, writer)


def get_url_ofUC(browser,writer):
    try:
        ucares = browser.find_element_by_id('resultsList').find_elements_by_class_name('result')
        for ucare in ucares:
            print(ucare.find_element_by_tag_name('a').get_attribute('href'))
            url = ucare.find_element_by_tag_name('a').get_attribute('href')
            generate_csv(url,writer)
    except:
        print('No Url')

def go_to_nextpage(browser,writer):
    try:
        get_url_ofUC(browser,writer)
        pyautogui.click(1354, 690)
        pyautogui.click(1354, 690)
        pyautogui.click(1354, 690)
        pyautogui.click(1354, 690)
        time.sleep(2)
        browser.find_element_by_class_name('next-page').click()
        go_to_nextpage(browser,writer)
    except:
        pass


def parser(searchSyntax,city):
    par1 = searchSyntax[searchSyntax.find('?') + 1:searchSyntax.find('=')]
    encodedurl = {par1: city}
    url = searchSyntax[:searchSyntax.find('?') + 1] + urllib.parse.urlencode(encodedurl) + '&proximity=50'
    print(url)
    browser.get(url)
    # print ('Waiting 10 seconds...')
    time.sleep(20)
    go_to_nextpage(browser,writer)

# fieldnames = ['url']
# csvName =datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + 'ucare.csv'
# csvF = csv_file_name_generation(csvName)
# writer = csv.DictWriter(csvF, fieldnames=fieldnames)
# writer.writeheader()
path_to_chromedriver = '/home/mostafiz/Downloads/chrome1/chromedriver'  # change path as needed
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
browser.get('https://www.google.com/')
browser.set_window_size(1920, 1080)
# allcityInUSA = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'Detroit', 'San Jose', 'Austin', 'Jacksonville', 'San Francisco', 'Indianapolis', 'Columbus', 'Fort Worth', 'Charlotte', 'Seattle', 'El Paso', 'Dallas', 'Denver', 'Washington', 'Memphis', 'Boston', 'Nashville', 'Baltimore', 'Oklahoma City', 'Portland', 'Las Vegas', 'Louisville', 'Milwaukee', 'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Long Beach', 'Kansas City', 'Mesa', 'Atlanta', 'Virginia Beach', 'Omaha', 'Colorado Springs', 'Raleigh', 'Miami', 'Oakland', 'Minneapolis', 'Tulsa', 'Cleveland', 'Wichita', 'New Orleans', 'Arlington', 'Bakersfield', 'Tampa', 'Aurora', 'Honolulu', 'Anaheim', 'Santa Ana', 'Corpus Christi', 'Riverside', 'St. Louis', 'Lexington', 'Pittsburgh', 'Stockton', 'Anchorage', 'Cincinnati', 'Saint Paul', 'Greensboro', 'Toledo', 'Newark', 'Plano', 'Henderson', 'Lincoln', 'Orlando', 'Jersey City', 'Chula Vista', 'Buffalo', 'Fort Wayne', 'Chandler', 'St. Petersburg', 'Laredo', 'Durham', 'Irvine', 'Madison', 'Norfolk', 'Lubbock', 'Gilbert', 'Winston–Salem', 'Glendale', 'Reno', 'Hialeah', 'Garland', 'Chesapeake', 'Irving', 'North Las Vegas', 'Scottsdale', 'Baton Rouge', 'Fremont', 'Richmond', 'Boise', 'San Bernardino', 'Birmingham', 'Spokane', 'Rochester', 'Modesto', 'Des Moines', 'Oxnard', 'Tacoma', 'Fontana', 'Fayetteville', 'Moreno Valley', 'Columbus', 'Huntington Beach', 'Yonkers', 'Montgomery', 'Aurora', 'Glendale', 'Shreveport', 'Akron', 'Little Rock', 'Amarillo', 'Augusta', 'Mobile', 'Grand Rapids', 'Salt Lake City', 'Huntsville', 'Tallahassee', 'Grand Prairie', 'Overland Park', 'Knoxville', 'Brownsville', 'Worcester', 'Newport News', 'Santa Clarita', 'Providence', 'Fort Lauderdale', 'Garden Grove', 'Oceanside', 'Rancho Cucamonga', 'Santa Rosa', 'Port St. Lucie', 'Chattanooga', 'Tempe', 'Jackson', 'Cape Coral', 'Vancouver', 'Ontario', 'Sioux Falls', 'Peoria', 'Springfield', 'Pembroke Pines', 'Elk Grove', 'Salem', 'Corona', 'Lancaster', 'Eugene', 'Palmdale', 'McKinney', 'Salinas', 'Fort Collins', 'Cary', 'Hayward', 'Springfield', 'Pasadena', 'Macon', 'Pomona', 'Alexandria', 'Escondido', 'Sunnyvale', 'Lakewood', 'Kansas City', 'Rockford', 'Torrance', 'Hollywood', 'Joliet', 'Bridgeport', 'Clarksville', 'Paterson', 'Naperville', 'Frisco', 'Mesquite', 'Savannah', 'Syracuse', 'Dayton', 'Pasadena', 'Orange', 'Fullerton', 'McAllen', 'Killeen', 'Hampton', 'Bellevue', 'Warren', 'Miramar', 'West Valley City', 'Olathe', 'Columbia', 'Sterling Heights', 'Thornton', 'New Haven', 'Waco', 'Charleston', 'Thousand Oaks', 'Visalia', 'Cedar Rapids', 'Elizabeth', 'Roseville', 'Gainesville', 'Carrollton', 'Stamford', 'Denton', 'Midland', 'Coral Springs', 'Concord', 'Topeka', 'Simi Valley', 'Surprise', 'Lafayette', 'Kent', 'Hartford', 'Santa Clara', 'Victorville', 'Abilene', 'Murfreesboro', 'Evansville', 'Vallejo', 'Athens', 'Allentown', 'Berkeley', 'Norman', 'Ann Arbor', 'Beaumont', 'Independence', 'Columbia', 'Springfield', 'El Monte', 'Fargo', 'Peoria', 'Provo', 'Lansing', 'Odessa', 'Downey', 'Wilmington', 'Arvada', 'Costa Mesa', 'Round Rock', 'Carlsbad', 'Miami Gardens', 'Westminster', 'Inglewood', 'Rochester', 'Fairfield', 'Elgin', 'West Jordan', 'Clearwater', 'Manchester', 'Lowell', 'Gresham', 'Cambridge', 'Ventura', 'Temecula', 'Waterbury', 'Antioch', 'Billings', 'High Point', 'Richardson', 'Richmond', 'West Covina', 'Pueblo', 'Murrieta', 'Centennial', 'Norwalk', 'North Charleston', 'Everett', 'Pompano Beach', 'Daly City', 'Palm Bay', 'Burbank', 'Wichita Falls', 'Boulder', 'Green Bay', 'Broken Arrow', 'West Palm Beach', 'College Station', 'Pearland', 'Santa Maria', 'El Cajon', 'San Mateo', 'Lewisville', 'Rialto', 'Davenport', 'Lakeland', 'Clovis', 'Edison', 'Sandy Springs', 'Tyler', 'Las Cruces', 'South Bend', 'Farmington Hills', 'Erie']
# for city in allcityInUSA:
#     print(city)
#     parser('https://www.urgentcarelocations.com/urgent-care-near-me?q=Portland',city)
# #writer.close()
# csvF.close()
csvName = 'in_ucare.csv'
with open(csvName, "rb" ) as theFile:
    #reader = csv.DictReader( theFile )
    fieldnames1 = ['url','name','nameWithCity','HoursOfOperation','AcceptedInsurances' ,'Certification','acceptedPaymentType' ,'about' ,'telephone' ,'services' ,'streetAddress' ,'city','state','zipCode' ]
    csvName1 = datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + 'out_ucare.csv'
    csvF1 = csv_file_name_generation(csvName1)
    writer1 = csv.DictWriter(csvF1, fieldnames=fieldnames1)
    writer1.writeheader()
    count = 0
    for line in theFile.readlines():
        urlUC = line.strip().decode('utf-8')
        try:
            print('count = ' + str(count))
            parse_each_uc(browser,urlUC,writer1)
            count += 1

        except:
            pass
    #parse_each_uc(browser, 'https://www.urgentcarelocations.com/ny/college-point/9947-xpress-medical-walk-in-urgent-care', writer1)

