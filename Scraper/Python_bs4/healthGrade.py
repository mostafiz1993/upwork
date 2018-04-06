import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import re

from urlparse import urljoin


class HealthGrade:

    def create_url(self,searchSyntax, location):
        par1 = searchSyntax[searchSyntax.find('?') + 1:searchSyntax.find('=')]
        encodedurl = {par1: location}
        url = searchSyntax[:searchSyntax.find('?') + 1] + urllib.urlencode(encodedurl)
        return url

    def getEachHospitalUrl(self,base, suffix):
        return urljoin(base, suffix)

    def getSoap(self,url):
        try:
            page = urllib.urlopen(url).read()
            return BeautifulSoup(page, "html.parser")
        except:
            r = requests.get(url.format('1'))
            return BeautifulSoup(r.content, 'html.parser')

    def csv_file_name_generation(self,csvFile):
        csvFileName = datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y") + '_' + csvFile
        return open(csvFileName, 'w')

    def create_csv(self,csvName):
        fieldnames = ['hospitalName', 'streetAddress', 'city', 'state', 'postalCode', 'noOfAffiliatedProvider']
        csvF = self.csv_file_name_generation(csvName)
        writer = csv.DictWriter(csvF, fieldnames=fieldnames)
        writer.writeheader()
        return writer

    def write_to_csv(self,hName, streetAddress, city, state, postalCode, noOfAffiliatedProvider, writer):
        try:
            writer.writerow({'hospitalName': hName, 'streetAddress': streetAddress, 'city': city,
                             'state': state, 'postalCode': postalCode, 'noOfAffiliatedProvider': noOfAffiliatedProvider})
        except:
            print('error while writing to file')
            pass

    def parse_each_page(self,url, writer):
        soup = self.getSoap(url)
        try:
            Hospitals = soup.find_all('div', attrs={'class': 'listingInformationColumn'})
            for hospital in Hospitals:
                try:
                    hospitalName = hospital.find_all('a', attrs = {'class' : 'providerSearchResultSelectAction'})[0].text
                    #print hospitalName
                except:
                    hospitalName = 'N/A'
                try:
                    address = hospital.find_all('div', attrs={'class': 'address'})[0].text
                    #print address
                    splitedAddress = address.split(',')
                    try:
                        streetAddress = splitedAddress[0]
                        #print streetAddress
                    except:
                        streetAddress = 'N/A'
                    try:
                        city = splitedAddress[1].strip()
                        #print city
                    except:
                        city = 'N/A'
                    try:
                        state = splitedAddress[2].strip().split(' ')[0]
                        #print state
                    except:
                        state = 'N/A'
                    try:
                        postalCode = splitedAddress[2].strip().split(' ')[1]
                        #print postalCode
                    except:
                        postalCode = 'N/A'

                except:
                    hospitalName = 'N/A'
                    streetAddress = 'N/A'
                    city = 'N/A'
                    state = 'N/A'
                    postalCode = 'N/A'
                try:
                    afprovs = hospital.find_all('li',attrs = {'class' : 'dataDebug'})
                    noOfAffiliatedProvider = 0
                    for afprov in afprovs:
                        if 'Affiliated' in afprov.text:
                            noOfAffiliatedProvider = int(re.findall(r'\d+', afprov.text )[0])
                            #print noOfAffiliatedProvider
                            break
                except:
                    noOfAffiliatedProvider = 0
                self.write_to_csv(hospitalName, streetAddress, city, state, postalCode, noOfAffiliatedProvider, writer)
        except:
            print 'No hospital found in the location'
            return

    def go_to_next_page(self,url, writer):
        self.parse_each_page(url, writer)
        soup = self.getSoap(url)
        try:
            paginations = soup.find_all('span', attrs= {'class' : 'nextPage'})[0].find_all('a', attrs={'class': 'paginationRight'})
            #print paginations
            for pagination in paginations:
                nextPageUrl =  pagination['href']
                #print nextPageUrl
                self.go_to_next_page(nextPageUrl, writer)
        except:
            return

    def runParser(self,searchSyntax, location, csvName):
        writer = self.create_csv(csvName)
        url = self.create_url(searchSyntax, location)
        self.go_to_next_page(url, writer)


u = HealthGrade()
u.runParser('https://www.healthgrades.com/hospital-directory/search/HospitalsResults?loc=New+York%2C+NY','new york,ny','healthgrade.csv')


