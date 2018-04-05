import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import time
from celery import shared_task,current_task
import re


property = {}
identifierofEachJobAttr = {}
identifierofEachJobUrl = {}
jobTitileAttr = {}
jobCompanyAttr = {}
jobLocationAttr = {}
paginationAttr = {}
jobIdAttr = {}
jobDescriptionAttr = {}
csvFileName = ''

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



def generate_csv(jobId,eachJobUrl,jobTitle,jobLocation,jobCompany,jobDescription,writer):
    try:
        jobTitle = re.sub('[^0-9a-zA-Z]+', ' ', jobTitle)
        jobLocation = re.sub('[^0-9a-zA-Z]+', ' ', jobLocation)
        jobCompany = re.sub('[^0-9a-zA-Z]+', ' ', jobCompany)
        jobDescription = re.sub('[^0-9a-zA-Z]+', ' ', jobDescription)
        #print(jobId + " " + jobLocation )
        writer.writerow({'JobId' : jobId, 'JobUrl' : eachJobUrl, 'JobTitle': jobTitle, 'JobLocation': jobLocation,
                         'Company': jobCompany, 'JobDescription': jobDescription})
        #csvF.write(jobTitle + ',' + jobLocation + ',' + jobCompany + '\n')
    except:
        print('error found')
        pass



def initParameter(csvFile):
    with open(csvFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            property[row[0]] = row[1]
            #if row[0].split(',')[0] == 'valueOfIdentifierofEachJobAttr':
            #print row
        identifierofEachJobAttr[property['identifierofEachJobAttr']] = property['valueOfIdentifierofEachJobAttr']
        identifierofEachJobUrl[property['identifierofEachJobUrl']] = property['valueOfIdentifierofEachJobUrl']
        jobIdAttr[property['jobIdAttr']] = property['valueOfjJobIDAttr']
        jobTitileAttr[property['jobTitileAttr']] = property['valueOfjJobTitileAttr']
        jobCompanyAttr[property['jobCompanyAttr']] = property['valueOfJobCompanyAttr']
        jobLocationAttr[property['jobLocationAttr']] = property['valueOfjJobLocationAttr']
        paginationAttr[property['paginationAttr']] = property['valueOfPaginationAttr']
        jobDescriptionAttr[property['jobDescriptionAttr']] = property['valueOfjJobDescriptionAttr']

def parse_each_page(soup,writer):
    job = soup.find_all(property['eachJobIn'], attrs = identifierofEachJobAttr)
    for eachJob in job:
        if int(property['directEachjobUrl']) == 1:
            eachJobUrl = eachJob.find_all(property['EachJobUrlIn'])
            #print eachJobUrl
        else:
            eachJobUrl = eachJob.find_all(property['EachJobUrlIn'], attrs = identifierofEachJobUrl)
        if int(property['prefixFlag']) == 1:
            eachJobUrl = property['prefix'] + eachJobUrl[0]["href"]
        else:
            eachJobUrl = eachJobUrl[0]["href"]

        eachJobPage = getSoap(eachJobUrl)
        if int(property['directJobId']) == 1:
            jobIdIn = eachJobPage.find_all(property['jobIdIn'], attrs=jobIdAttr)
            #print(jobIdIn)
            # print jobIdIn
            try:
                jobId = jobIdIn[0][property['JobIdInAttr']]

            except:
                jobId = ''
                pass
        else:
            jobId = 'no job id'
        if int(property['jobCompanyBranch']) == 1:
            companyt = eachJobPage.find_all(property['jobCompanyIn'], attrs = jobCompanyAttr)
            try:
                companyt1 = companyt[0].find_all(property['jobCompanyBranchAttr'])
                company = companyt1[0].text

            except:
                company=''
                pass
        else:
            companyt = eachJobPage.find_all(property['jobCompanyIn'], attrs=jobCompanyAttr)
            try:
                company = companyt[0].text
            except:
                company = ''
                pass
        if int(property['jobTitileBranch']) == 1:
            jobt = eachJobPage.find_all(property['jobTitileIn'], attrs=jobTitileAttr)
            try:
                jobt1 = jobt[0].find_all(property['jobTitileBranchAttr'])
                jobTitle = jobt1[0].text
            except:
                jobTitle = ''
                pass
        else:
            jobt = eachJobPage.find_all(property['jobTitileIn'], attrs=jobTitileAttr)
            try:
                jobTitle = jobt[0].text
            except:
                jobTitle = ''
                pass

            #companyName = company[0].a.text
            #job = jobTitle[0].font.text

        jobL = eachJobPage.find_all(property['jobLocationIn'], attrs=jobLocationAttr)
        if property['jobLocationIn'] == 'input':
            try:
                jobLocation = jobL[0]['value']
            except:
                jobLocation = ''
                pass
        else:
            try:
                jobLocation = jobL[0].text
            except:
                jobLocation = ''
                pass

        if int(property['directJobDescription']) == 1:
            jobdes = eachJobPage.find_all(property['jobDescriptionIn'], attrs=jobDescriptionAttr)
            try:
                jobDescription = ''
                for des in jobdes:
                    jobDescription = jobDescription + des.text
            except:
                jobDescription = ''
                pass
        else:
            jobDescription = 'test'


        generate_csv(jobId, eachJobUrl, jobTitle, jobLocation, company, jobDescription, writer)


def go_to_next_page(url,writer):
    if int(property['prefixPaginationFlag']) == 1:
        try:
            urlopen = property['prefix'] + url
        except:
            return
    else:
        try:
            urlopen = url
        except:
            return
    print(url)

    soup = getSoap(urlopen)
    parse_each_page(soup,writer)
    if int(property['directPagination']) != 1:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
        try:
            go_to_next_page(next['href'],writer)
        except:
            return

    else:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        #print(pagination[0]['href'])
        try:
            go_to_next_page(pagination[0]['href'],writer)
        except:
            return

def runParser(searchSyntax,location,csvName):
    #url = 'https://www.simplyhired.com/search?q=data+scientist&l=New+York'

    #time.sleep(firstTime)
    # par1 = searchSyntax[searchSyntax.find('?') + 1:searchSyntax.find('=')]
    # par2 = searchSyntax[searchSyntax.find('&') + 1:searchSyntax.rfind('='):]
    # encodedurl = {par1: jobTtile, par2: location}
    # url =  searchSyntax[:searchSyntax.find('?') + 1] + urllib.urlencode(encodedurl)
    # print url
    soup = getSoap(searchSyntax)
    Hospitals =  soup.find_all('a', attrs={'class' : 'providerSearchResultSelectAction'})
    for hospital in Hospitals:
        print hospital
    # print(csvName)
    # initParameter(csvName)
    # fieldnames = ['JobId', 'JobUrl', 'JobTitle', 'JobLocation', 'Company', 'JobDescription']
    # csvF = csv_file_name_generation(csvName)
    # writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    # writer.writeheader()
    # print("intermediate step")
    # pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
    # print pagination
    # next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
    # print next
    # print next['href']
    # parse_each_page(soup,writer)
    # if int(property['directPagination']) != 1:
    #     pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
    #     next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
    #     try:
    #         go_to_next_page(next['href'],writer)
    #     except:
    #         pass
    # else:
    #     pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
    #     # print pagination[0]['href']
    #     try:
    #         go_to_next_page(pagination[0]['href'],writer)
    #     except:
    #         pass
    # csvF.close()
runParser('https://www.healthgrades.com/hospital-directory/search/HospitalsResults?loc=New+York%2C+NY','new york,ny','healthgrade.csv')



