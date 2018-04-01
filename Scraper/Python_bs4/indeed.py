
from bs4 import BeautifulSoup
import urllib
prefix = 'https://www.indeed.com'
first_page = urllib.urlopen('https://www.indeed.com/jobs?q=data+scientist').read()
soup = BeautifulSoup(first_page, "html.parser")







def parse_each_page(soup):
    job = soup.find_all("div", class_="row")
    for eachJob in job:
        print 'yo'
        eachJobUrl = eachJob.find_all('a', class_='turnstileLink')
        eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])
        eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
        company1 = eachJobPage.find_all("div", class_="cmp_title")
        company = company1[0].find_all('a')
        #jobTitle = eachJobPage.find_all(property['jobTitileIn'], attrs=c)
        jobLocation = eachJobPage.find_all('input', id='where')
        jobt = eachJobPage.find_all('b', class_='jobtitle')
        jobt1 = jobt[0].find_all('font')
        try:
            companyName = company[0].text
            #job = jobTitle[0].font.text
            #print job
            #print companyName
            print jobLocation[0]['value']
            print jobt1[0].text
            print companyName
            # for item in jobLocation:
            #     print item.text
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


parse_each_page(soup)


pagination = soup.find_all("div", class_="pagination")
next = pagination[0].find_all("a")[-1]
print type(next)
print str(next)
if 'Next' in str(next):
    print next[0]['href']
# for nextHref in next:
#     if "Next" in nextHref.find_all("span")[0].text:
#         go_to_next_page(nextHref['href'])


# pagination = soup.find_all("span", class_="np")
# print pagination[0].parent.parent
# next = pagination[0].find_all("a");
# for nextHref in next:
#     if "Next" in nextHref.find_all("span")[0].text:
#         go_to_next_page(nextHref['href'])





