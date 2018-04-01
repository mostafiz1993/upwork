
from bs4 import BeautifulSoup
import urllib
prefix = 'https://www.careerbuilder.com'
first_page = urllib.urlopen('https://www.careerbuilder.com/jobs-data-scientist-in-new-york?keywords=data+scientist&location=new+york').read()
soup = BeautifulSoup(first_page, "html.parser")


def parse_each_page(soup):
    print 'yo'
    job = soup.find_all("div", class_="job-row")
    for eachJob in job:
        eachJobUrl = eachJob.find_all('a')
        #print eachJobUrl
        print prefix + eachJobUrl[0]["href"]
        eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])
        eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
        company = eachJobPage.find_all("h2", id="job-company-name")
        jobt = eachJobPage.find_all("div", class_="card")
        jobt1 = jobt[0].find_all('h1')
        jobtitle = jobt1[0].text
        try:
            print company[0].text
            #companyName = company[0].a.text
            #job = jobTitle[0].font.text
            print jobtitle
            #print companyName
        except :
            pass


def go_to_next_page(url):
    urlopen = urllib.urlopen( url)
    print url
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


#pagination = soup.find_all("div", class_="pagination")
pagination = soup.find_all("a",id='next-button')
print pagination[0]['href']
# print
# for nextHref in next:
#     try:
#         print nextHref.attrs['id']
#         if  'next' in  nextHref.attrs['id']:
#             print nextHref.attrs['id']
#             print nextHref['href']
#             #go_to_next_page(nextHref['href'])
#     except:








