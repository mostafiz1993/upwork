import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import re

from urlparse import urljoin


class HealthGrade:
    #i = 2
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

    def write_to_csv(self,name, address, phone,faxNumber,speciality,NpiNumber,lbnName,dbaName,authOfficialName,entity,organizationSubpart,enumeratioDate,lastUpdated,identifiers,writer):
        try:
            writer.writerow({'Name': name, 'Address' : address, 'phone' : phone, 'fax' : faxNumber, 'speciality' : speciality, 'NpiNumber' : NpiNumber,
                             'lbn' : lbnName,'dba' : dbaName,'authOfficialName' : authOfficialName,'entity' : entity,'organizationSubpart' : organizationSubpart,
                             'enumeratioDate' : enumeratioDate,'lastUpdated' : lastUpdated,'identifiers' : identifiers})
            print 'in writing'
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
            #break

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
            NpiNumber = ''
            lbnName = ''
            authOfficialName = ''
            entity = ''
            organizationSubpart = ''
            enumeratioDate = ''
            lastUpdated = ''
            identifiers = ''
            dbaName = ''
            print len(allGenInfo)
            for genInfo in allGenInfo:
                print genInfo.find('td').text
                if 'NPI Number' in genInfo.find('td').text:
                    try:
                        NpiNumber = genInfo.find('code',attrs= {'class' : 'lead'}).text
                        print NpiNumber
                    except:
                        NpiNumber = ''
                if 'LBN' in genInfo.find('td').text:
                    try:
                        lbnName = ' '.join(genInfo.find('span').text.split())
                        print lbnName
                    except:
                        lbnName = ''
                if 'DBA' in genInfo.find('td').text:
                    try:
                        dbaName = ' '.join(genInfo.find_all('td')[1].text.split())
                        print dbaName
                    except:
                        dbaName = ''
                if 'Authorized official' in genInfo.find('td').text:
                    try:
                        authOfficialName = ' '.join(genInfo.find('span').text.split())
                        print authOfficialName
                    except:
                        authOfficialName = ''

                if 'Entity' in genInfo.find('td').text:
                    try:
                        entity = ' '.join(genInfo.find('span').text.split())
                        print entity
                    except:
                        entity = ''
                if 'Organization subpart' in genInfo.find('td').text:
                    try:
                        organizationSubpart = ' '.join(genInfo.find('span').text.split())
                        print organizationSubpart
                    except:
                        organizationSubpart = ''
                if 'Enumeration date' in genInfo.find('td').text:
                    try:
                        enumeratioDate = genInfo.find('span').text
                        print enumeratioDate
                    except:
                        enumeratioDate = ''
                if 'Last updated' in genInfo.find('td').text:
                    try:
                        lastUpdated = genInfo.find('span').text
                        print lastUpdated
                    except:
                        lastUpdated = ''

                if 'Identifiers' in genInfo.find('td').text:
                    try:
                        identifiers = ' '.join(genInfo.find_all('td')[1].text.split())
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
            dbaName = ''

        self.write_to_csv(name, address, phone,faxNumber,speciality,NpiNumber,lbnName,dbaName,authOfficialName,entity,organizationSubpart,enumeratioDate,lastUpdated,identifiers,writer)


    def go_to_next_page(self,url, writer):
        soup = self.getSoap(url)
        self.go_to_each_page(url, writer)
        try:
            paginations = soup.find_all('ul', attrs= {'class' : 'pagination'})[0].find_all('li')
            if 'Next Page' in paginations[-1].find('a')['title']:
                nextPageUrl =  self.getEachUrgentCareUrl(url,paginations[-1].find('a')['href'])
                print nextPageUrl
                print writer
                #if self.i <= 2:
                    #self.i += 1
                self.go_to_next_page(nextPageUrl, writer)
        except:
            return

    def runParser(self,searchSyntax, csvName):
        writer = self.create_csv(csvName,'Name', 'Address', 'phone', 'fax', 'speciality', 'NpiNumber','lbn','dba','authOfficialName','entity','organizationSubpart','enumeratioDate',
                                 'lastUpdated','identifiers')
        self.go_to_next_page(searchSyntax, writer)


u = HealthGrade()
u.runParser('https://npidb.org/organizations/ambulatory_health_care/urgent-care_261qu0200x','urgentcare.csv')


#https://npidb.org/organizations/ambulatory_health_care/urgent-care_261qu0200x
