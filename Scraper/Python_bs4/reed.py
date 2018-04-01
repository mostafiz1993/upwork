
from bs4 import BeautifulSoup
import urllib
prefix = 'https://www.reed.co.uk'
first_page = urllib.urlopen('https://www.reed.co.uk/jobs/jobs-in-london?keywords=data+scientist').read()
soup = BeautifulSoup(first_page, "html.parser")


def parse_each_page(soup):
    job = soup.find_all("article", class_="job-result")
    for eachJob in job:
        eachJobUrl = eachJob.find_all('a', class_='gtmJobTitleClickResponsive')
        #print eachJobUrl
        eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])

        eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
        #print eachJobPage
        company = eachJobPage.find_all("span", itemprop="name")
        #jobTitle = eachJobPage.find_all("b", class_="jobtitle")
        try:
            print company.text
            #companyName = company[0].a.text
            #job = jobTitle[0].font.text
            #print job
            #print companyName
        except :
            pass


def go_to_next_page(url):
    urlopen = urllib.urlopen(prefix + url)
    print prefix + url
    soup = BeautifulSoup(urlopen, "html.parser")
    parse_each_page(soup)
    pagination = soup.find_all("div", class_="pagination")
    pages = pagination[0].find_all("a");
    for nextHref in pages:
        try:
            if  'next' in  nextHref.attrs['id']:
                go_to_next_page(nextHref['href'])
        except:
            pass


#parse_each_page(soup)


pagination = soup.find_all("a", id="nextPage")
print pagination[0]['href']
#print pagination
#next = pagination[0].find_all("a")
#print next
for nextHref in pagination:
    try:
        print nextHref.attrs['id']
        if  'next' in  nextHref.attrs['id']:
            print nextHref.attrs['id']
            #go_to_next_page(nextHref['href'])
    except:
        pass







