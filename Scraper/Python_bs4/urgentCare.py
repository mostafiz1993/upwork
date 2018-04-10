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

    def getEachUrgentCareUrl(self,base, suffix):
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

    def create_csv(self,csvName,*column):
        csvF = self.csv_file_name_generation(csvName)
        writer = csv.DictWriter(csvF, fieldnames=list(column))
        writer.writeheader()
        return writer

    def write_to_csv(self,name, address, phone,faxNumber,speciality,NpiNumber,lbnName,authOfficialName,entity,organizationSubpart,enumeratioDate,lastUpdated,identifiers,writer):
        try:
            writer.writerow({'Name': name, 'Address' : address, 'phone' : phone, 'fax' : faxNumber, 'speciality' : speciality, 'NpiNumber' : NpiNumber,
                             'lbnName' : lbnName,'authOfficialName' : authOfficialName,'entity' : entity,'organizationSubpart' : organizationSubpart,
                             'enumeratioDate' : enumeratioDate,'lastUpdated' : lastUpdated,'identifiers' : identifiers})
        except:
            print('error while writing to file')
            pass

    def go_to_each_page(self,url,writer):
        soup = self.getSoap(url)
        careCentres = soup.find_all('table', attrs={'class': 'table'})[0].find_all('tr', attrs={'class': 'small'})
        for careCentre in careCentres:
            #print careCentre
            eachCareUrl =  self.getEachUrgentCareUrl(url, careCentre.find('a')['href'])
            self.parse_each_page(eachCareUrl,writer)
            break

    def parse_each_page(self,url, writer):
        soup = self.getSoap(url)
        try:
            name = ' '.join(soup.find_all('div', attrs={'class': 'page-header'})[0].find_all('h1')[0].text.split())
            print name
        except:
            name = ''
        try:
            address = ''
            addressSpans = soup.find('address').find_all('span')
            for addressSpan in addressSpans:
                #print addressSpan.text
                address = address + ' ' + addressSpan.text
            print address.strip()
        except:
            address = ''
        try:
            phone = soup.find('span', attrs= {'itemprop' : 'telephone'}).text
            print phone
        except:
            phone = ''
        try:
            faxNumber = soup.find('span', attrs={'itemprop': 'faxNumber'}).text
            print faxNumber
        except:
            faxNumber = ''
        try:
            faxNumber = soup.find('span', attrs={'itemprop': 'faxNumber'}).text
            print faxNumber
        except:
            faxNumber = ''
        try:
            if  soup.find('div', attrs={'class' : 'table-responsive'}).find('thead').find('h2').text == 'Specialty':
                specialities =  soup.find('div', attrs={'class' : 'table-responsive'}).find('tbody').find_all('tr')
                speciality = ''
                for special in specialities:
                    speciality = speciality + ',' + special.find('span', attrs= {'itemprop' : 'name'}).text
                speciality = speciality[1:]
                print speciality
        except:
            speciality = ''
        try:
            genInfo =  soup.find_all('div', attrs= {'class' : 'row'})[6]
            allGenInfo = genInfo.find_all('tr')
            try:
                NpiNumber = allGenInfo[0].find('code',attrs= {'class' : 'lead'}).text
                print NpiNumber
            except:
                NpiNumber = ''
            try:
                lbnName = allGenInfo[1].find('span').text
                print lbnName
            except:
                lbnName = ''
            try:
                authOfficialName = ' '.join(allGenInfo[2].find('span').text.split())
                print authOfficialName
            except:
                authOfficialName = ''
            try:
                entity = allGenInfo[3].find('span').text
                print entity
            except:
                entity = ''
            try:
                organizationSubpart = ' '.join(allGenInfo[4].find('span').text.split())
                print organizationSubpart
            except:
                organizationSubpart = ''
            try:
                enumeratioDate = allGenInfo[5].find('span').text
                print enumeratioDate
            except:
                enumeratioDate = ''
            try:
                lastUpdated = allGenInfo[6].find('span').text
                print lastUpdated
            except:
                lastUpdated = ''
            try:
                identifiers = ' '.join(allGenInfo[7].find_all('td')[1].text.split())
                print identifiers
            except:
                identifiers = ''

        except:
            NpiNumber = ''
            lbnName = ''
            authOfficialName = ''
            entity = ''
            organizationSubpart = ''
            enumeratioDate = ''
            lastUpdated = ''
            identifiers = ''
        self.write_to_csv(name, address, phone,faxNumber,speciality,NpiNumber,lbnName,authOfficialName,entity,organizationSubpart,enumeratioDate,lastUpdated,identifiers,writer)


    def go_to_next_page(self,url, writer):
        soup = self.getSoap(url)
        self.go_to_each_page(url, writer)
        try:
            paginations = soup.find_all('ul', attrs= {'class' : 'pagination'})[0].find_all('li')
            #print paginations
            if 'Next Page' in paginations[-1].find('a')['title']:
                nextPageUrl =  self.getEachUrgentCareUrl(url,paginations[-1].find('a')['href'])
                print nextPageUrl
                self.go_to_next_page(nextPageUrl, writer)
        except:
            return

    def runParser(self,searchSyntax, csvName):
        writer = self.create_csv(csvName,'Name', 'Address', 'phone', 'fax', 'speciality', 'NpiNumber','lbnName','authOfficialName','entity','organizationSubpart','enumeratioDate',
                                 'lastUpdated','identifiers')
        #url = self.create_url(searchSyntax, location)
        self.go_to_next_page(searchSyntax, writer)


u = HealthGrade()
u.runParser('https://npidb.org/organizations/ambulatory_health_care/urgent-care_261qu0200x','urgentcare.csv')

