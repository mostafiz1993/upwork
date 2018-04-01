
from bs4 import BeautifulSoup
import urllib
import time
prefix = 'https://www.indeed.com'
first_page = urllib.urlopen('https://www.simplyhired.com/search?q=data+scientist&l=New+York%2C+NY&job=OohGNTjvBTZREBhsWz79OmHkqeIRM8zapJkZBOtO0kgutNtNMNKMCw').read()
soup = BeautifulSoup(first_page,'html.parser')
time.sleep(3)
#print soup


def parse_each_page(soup):
    job = soup.find_all("div", class_="complete-serp-result-div")
    for eachJob in job:
        eachJobUrl = urllib.urlopen(prefix + eachJob.a["href"])
        eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
        company = eachJobPage.find_all("div", class_="cmp_title")
        jobTitle = eachJobPage.find_all("b", class_="jobtitle")
        try:
            companyName = company[0].a.text
            job = jobTitle[0].font.text
            print job
            print companyName
        except IndexError:
            pass


def go_to_next_page(url):
    urlopen = urllib.urlopen(prefix + url)
    print prefix + url
    soup = BeautifulSoup(urlopen, "html.parser")
    parse_each_page(soup)
    pagination = soup.find_all("div", class_="pagination")
    next = pagination[0].find_all("a");
    for nextHref in next:
        if "Next" in nextHref.find_all("span")[0].text:
            go_to_next_page(nextHref['href'])


#parse_each_page(soup)


# pagination = soup.find_all("div", class_="pagination")
# next = pagination[0].find_all("a");
# for nextHref in next:
#     if "Next" in nextHref.find_all("span")[0].text:
#         go_to_next_page(nextHref['href'])

#pagination = soup.find_all("div", class_="pagination")
#p = pagination[0].div
#print type(pagination)
#print pagination
#print p


job = soup.find_all("div", class_="card")
for eachJob in job:
    #print type(eachJob)
    url = eachJob.find_all('a', class_='card-link')
    #print url[0]['href']


pagination = soup.find_all("div", class_="pagination")
#print pagination
pages = pagination[0].find_all('a')
for eachpage in pages:
    # if eachpage['class'] == 'next-pagination':
    print eachpage
    try:
        print eachpage.attrs['class']
        if 'next' in  eachpage.attrs['class'][0]:

            print 'hello'
    except:
        print 'ys'
    #print (type(eachpage))
# next = pagination[0].find_all("a");
# for nextHref in next:
#     if "Next" in nextHref.find_all("span")[0].text:
#        print nextHref['href']







