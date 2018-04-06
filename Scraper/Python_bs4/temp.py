import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import re

from urlparse import urljoin


def getEachHospitalUrl(base,suffix):
    return urljoin(base, suffix)

def getSoap(url):
    try:
        page = urllib.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')



def write_to_csv(hName,streetAddress,city,state,postalCode,phoneNo,writer):
    try:
        writer.writerow({'hospitalName' : hName,'streetAddress' : streetAddress, 'city' : city,
                         'state' : state, 'postalCode' : postalCode, 'phoneNo' : phoneNo})
    except:
        print('error while writing to file')
        pass



def parse_each_page(url,writer):
    soup = getSoap(url)
    try:
        Hospitals = soup.find_all('table', attrs={'class': 'default'})[0].find_all('tr')
        for hospital in Hospitals[1:]:
            print hospital
            try:
                hospitalName = hospital.find('span', attrs={'itemprop': 'name'}).text
                print hospitalName
            except:
                hospitalName = 'N/A'
            try:
                streetAddress = hospital.find('span', attrs={'itemprop': 'streetAddress'}).text
                print streetAddress
            except:
                streetAddress = 'N/A'
            try:
                city = hospital.find('span', attrs={'itemprop': 'addressLocality'}).text
                print city
            except:
                city = 'N/A'
            try:
                state = hospital.find('span', attrs={'itemprop': 'addressRegion'}).text
                print state
            except:
                state = 'N/A'
            try:
                postalCode = hospital.find('span', attrs={'itemprop': 'postalCode'}).text
                print postalCode
            except:
                postalCode = 'N/A'
            try:
                phone = hospital.find_all('td', attrs={'class': 'hidden-phone'})[1].text
                print phone
            except:
                phone = 'N/A'
            write_to_csv(hospitalName, streetAddress, city, state, postalCode, phone, writer)
    except:
        print 'No hospital found in the location'
        return

def go_to_next_page(url,writer):
    parse_each_page(url,writer)
    soup = getSoap(url)
    try:
        paginations = soup.find_all('div', attrs={'class': 'pagination'})[0].find_all('a')
        for pagination in paginations:
            print pagination.text
            if pagination.text == 'next':
                nextPageUrl = getEachHospitalUrl(url,pagination['href'])
                print nextPageUrl
                go_to_next_page(nextPageUrl,writer)
    except:
        return

def create_url(searchSyntax,location):
    par1 = searchSyntax[searchSyntax.find('?') + 1:searchSyntax.find('=')]
    encodedurl = {par1: location}
    url = searchSyntax[:searchSyntax.find('?') + 1] + urllib.urlencode(encodedurl)
    return url

def create_csv(csvName):
    fieldnames = ['hospitalName', 'streetAddress', 'city', 'state', 'postalCode', 'phoneNo']
    csvF = csv_file_name_generation(csvName)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    return writer

def runParser(searchSyntax,location,csvName):
    writer = create_csv(csvName)
    #soup = getSoap(searchSyntax)
    url = create_url(searchSyntax,location)
    #print url
    go_to_next_page(url,writer)
    # Hospitals =  soup.find_all('table',attrs={'class' : 'default'})[0].find_all('a', attrs={'itemprop' : 'url'})
    # for hospital in Hospitals:
    #     if 'clinic-directory' not in hospital['href']:
    #         eachHospitalUrl =   getEachHospitalUrl(searchSyntax,hospital['href'])
    #         print eachHospitalUrl
            #parse_each_page(eachHospitalUrl,writer)

    # try:
    #     paginations = soup.find_all('div', attrs={'class' : 'pagination'})[0].find_all('a')
    #     for pagination in paginations:
    #         print pagination.text
    #         if pagination.text == 'next':
    #             nextPageUrl =  pagination['href']
    #             print nextPageUrl
    # #     go_to_next_page(nextPageUrl,writer)
    # except:
    #     pass
    # csvF.close()
runParser('http://www.urgentcaremedicals.com/search.php?q=new+york','new york','urgentcaremedicals.csv')



