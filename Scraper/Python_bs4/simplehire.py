
from bs4 import BeautifulSoup
import urllib
prefix = 'https://www.simplyhired.com'
first_page = urllib.urlopen('https://www.simplyhired.com/search?q=data+scientist&l=New+York%2C+NY&job=sgAXyBDovfng2zwlmC_A1owZr6iGckzK8o2WWPdUFYEkirWbgzN4AA').read()
soup = BeautifulSoup(first_page, "html.parser")


def parse_each_page(soup):
    job = soup.find_all("div", class_="card")
    for eachJob in job:
        eachJobUrl = eachJob.find_all('a', class_='card-link')
        eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])
        eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
        company = eachJobPage.find_all("span", class_="company")
        jobTitle = eachJobPage.find_all("h1", itemprop="title")
        try:
            print company[0].text
            #companyName = company[0].a.text
            #job = jobTitle[0].font.text
            print jobTitle[0].text
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


pagination = soup.find_all("a", class_="next-pagination")
print pagination[0]['href']
#next = pagination[0].find_all("a");
# for nextHref in pagination:
#     try:
#         print nextHref.attrs['class']
#         if  'next' in  nextHref.attrs['class'][0]:
#             print nextHref['href']
#             #go_to_next_page(nextHref['href'])
#     except:
#         pass







