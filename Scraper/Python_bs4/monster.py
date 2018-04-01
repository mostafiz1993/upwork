
from bs4 import BeautifulSoup
import urllib2,requests
prefix = 'https://www.monster.com'
# first_page = urllib.urlopen('https://www.monster.com/jobs/search/?q=Data-Scientist&where=new-york&intcid=skr_navigation_nhpso_searchMain').read()
# soup = BeautifulSoup(first_page, "html.parser")

def getSoap(url):
    try:
        page = urllib2.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')

soup = getSoap('https://www.monster.com/jobs/search/?q=Data-Scientist&where=new-york')

def parse_each_page(soup):
    job = soup.find_all("div", attrs={"class":"js_result_container clearfix primary"})
    #print job[0]
    for eachJob in job:
        #print eachJob
        eachJobUrl = eachJob.find_all('a')
        print eachJobUrl
        eachJobUrl = eachJobUrl[0]["href"]
        eachJobPage = getSoap(eachJobUrl)
        company = eachJobPage.find_all("h3", class_="name")
        #jobTitle = eachJobPage.find_all("b", class_="jobtitle")
        try:
            print company
            #companyName = company[0].a.text
            #job = jobTitle[0].font.text
            #print job
            #print companyName
        except :
            pass


def go_to_next_page(url):
    urlopen = prefix + url
    print prefix + url
    soup = getSoap(urlopen)
    parse_each_page(soup)
    pagination = soup.find_all("div", class_="pagination")
    pages = pagination[0].find_all("a");
    for nextHref in pages:
        try:
            if  'next' in  nextHref.attrs['class'][0]:
                go_to_next_page(nextHref['href'])
        except:
            pass


parse_each_page(soup)


pagination = soup.find_all("div", class_="pagingWrapper")
next = pagination[0].find_all("a");
for nextHref in next:
    try:
        if  'next' in  nextHref.attrs['class'][0]:
            go_to_next_page(nextHref['href'])
    except:
        pass







