
from bs4 import BeautifulSoup
import urllib
prefix = 'https://www.glassdoor.com'
first_page = urllib.urlopen('https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=data&sc.keyword=Data+Scientist&locT=C&locId=1132348&jobType=').read()
soup = BeautifulSoup(first_page, "lxml")
print soup

def parse_each_page(soup):
    job = soup.find_all("li", class_="jl")
    for eachJob in job:
        eachJobUrl = eachJob.find_all('a', class_='jobLink')
        eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])
        eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
        company = eachJobPage.find_all("a", class_="plain")
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
    urlopen = urllib.urlopen(prefix + url)
    print prefix + url
    soup = BeautifulSoup(urlopen, "html.parser")
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


pagination = soup.find_all("div", class_="pagingControls")
print pagination
#next = pagination[0].find_all("li");
# for nextHref in next:
#     try:
#         if  'next' in  nextHref.attrs['class'][0]:
#             #go_to_next_page(nextHref['href'])
#             print nextHref
#     except:
#         pass







