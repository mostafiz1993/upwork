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



def generate_csv(hName,address,noOfAprov,writer):
    try:
        writer.writerow({'HospitalName' : hName, 'Address' : address, 'NoOfAffiliatedProvider': noOfAprov})
    except:
        print('error found')
        pass



def parse_each_page(hospitalUrl,writer):
    eachHospitalPage = getSoap(hospitalUrl)
    try:
        hName = eachHospitalPage.find_all(attrs={'class' : 'summary-hero-address'})
        hospitalName =  hName[0].find('h1').text
    except:
        hospitalName = 'N/A'
        print 'No hospital name found'
        pass
    try:
        haddress = eachHospitalPage.find_all(attrs={'itemprop' : 'address'})
        parsedhAddress =  haddress[0].text
        hAddress = ''
        for a in parsedhAddress.split(','):
            if '\n' in a:
                hAddress = hAddress + ',' + a.strip().replace('\n',',')
                continue
            hAddress = hAddress + ',' + a.strip()
    except:
        hAddress = [',']
        pass
    try:
        afprovider = eachHospitalPage.find_all(attrs={'class' : 'results-header'})
        noOfAffiliatedProvider = re.findall(r'\d+', afprovider[0].text )
    except:
        pass
    generate_csv(hospitalName, hAddress[1:], int(noOfAffiliatedProvider[0]), writer)


def go_to_next_page(url,writer):
    soup = getSoap(url)
    Hospitals =  soup.find_all('a', attrs={'class' : 'providerSearchResultSelectAction'})
    for hospital in Hospitals:
        if 'clinic-directory' not in hospital['href']:
            eachHospitalUrl =   getEachHospitalUrl(url,hospital['href'])
            parse_each_page(eachHospitalUrl,writer)
    try:
        pagination = soup.find_all('span', attrs={'class': 'nextPage'})[0].find('a')
        nextPageUrl = pagination[0]['href']
        go_to_next_page(nextPageUrl,writer)
    except:
        return


def runParser(searchSyntax,location,csvName):
    fieldnames = ['HospitalName', 'Address', 'NoOfAffiliatedProvider']
    csvF = csv_file_name_generation(csvName)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    soup = getSoap(searchSyntax)
    Hospitals =  soup.find_all('a', attrs={'class' : 'providerSearchResultSelectAction'})
    for hospital in Hospitals:
        if 'clinic-directory' not in hospital['href']:
            eachHospitalUrl =   getEachHospitalUrl(searchSyntax,hospital['href'])
            parse_each_page(eachHospitalUrl,writer)
    #
    try:
        pagination = soup.find_all('span', attrs={'class' : 'nextPage'})[0].find('a')
        nextPageUrl =  pagination[0]['href']
        go_to_next_page(nextPageUrl,writer)
    except:
        pass
    csvF.close()
runParser('https://www.healthgrades.com/hospital-directory/search/HospitalsResults?loc=New+York%2C+NY','new york,ny','healthgrade.csv')



