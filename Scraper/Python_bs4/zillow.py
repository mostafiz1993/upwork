import csv
import requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd



data = []
def resume_to_csv(workexp,education):
    print [workexp]
    print [education]
    dfworkexp= pd.DataFrame([workexp])
    dfeducation = pd.DataFrame([education])
    data.append({'experience': dfworkexp, 'education': dfeducation})
    df = pd.DataFrame(data)
    print df['education']
    for index, row in df.iterrows():
        for i,r in row.iterrows():
            print r
    #df.to_csv('itest1.csv')




def getSoap(url):
    try:
        page = urllib.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')

def parse_each_page(soup):
    try:
        resumes = soup.find_all('div', attrs = {'class' :'app_name'})
        print len(resumes)
        for eachResume in resumes:
            try:
                eachResumeUrl = eachResume.find('a')
                resumeUrl =  'https://www.indeed.com' + eachResumeUrl['href']
            except:
                print 'Resume Url not Found'
            try:
                print resumeUrl
                eachResumePage = getSoap(resumeUrl)
            except:
                print 'Problem to load resume page'
            try:
                resumeDes = eachResumePage.find_all('div', attrs={'id' : 'resume_body'})
            except:
                resumeDes = ''
            #print resumeDes
            # print type(resumeDes)
            # print len(resumeDes)
            allDivOfBody = resumeDes[0].find_all('div',attrs={'class' : lambda L: L and L.endswith('content')})
            print allDivOfBody
            #print len(allDivOfBody)
            dictworkexps = {}
            dicteducations = {}
            dictpubs = {}
            for div in allDivOfBody:
                if 'workExperience-content' in div['class']:
                    workexps = div.find_all('div', attrs = {'class' : lambda L: L and L.startswith('work-experience-section') })
                    print len(workexps)
                    i = 1
                    for workexp in workexps:
                        key = 'exp' + str(i)
                        dictworkexps[key] = workexp.text
                        i += 1
                    print dictworkexps
                if 'education-content' in div['class']:
                    educations = div.find_all('div', attrs={'class': lambda L: L and L.startswith('education-section')})
                    print len(educations)
                    i = 1
                    for education in educations:
                        key = 'edu' + str(i)
                        dicteducations[key] = education.text
                        i += 1
                    print dicteducations
                if 'skills-content' in div['class']:
                    skills = div.find_all('div', attrs={'class': lambda L: L and L.startswith('skill-container')})
                    print len(skills)
                    dictskills = {}
                    i = 1
                    for skill in skills:
                        key = 'skill' + str(i)
                        dictskills[key] = skill.text
                        i += 1
                    print dictskills
                if 'links-content' in div['class']:
                    links = div.find_all('div', attrs={'class': lambda L: L and L.startswith('link-section')})
                    print len(links)
                    dictlinks = {}
                    i = 1
                    for link in links:
                        key = 'link' + str(i)
                        dictlinks[key] = link.text
                        i += 1
                    print dictlinks
                if 'certification-content' in div['class']:
                    certifications = div.find_all('div', attrs={'class': lambda L: L and L.startswith('certification-section')})
                    print len(certifications)
                    dictcerts = {}
                    i = 1
                    for certification in certifications:
                        key = 'cert' + str(i)
                        dictcerts[key] = certification.text
                        i += 1
                    print dictcerts

                if 'publications-content' in div['class']:
                    publications = div.find_all('div',attrs={'class': lambda L: L and L.startswith('publication-section')})
                    print len(publications)
                    i = 1
                    for publication in publications:
                        key = 'pub' + str(i)
                        dictpubs[key] = publication.text
                        i += 1
                    print dictpubs
                if 'additionalInfo-content' in div['class']:
                    addInfos = div.find_all('div', attrs={'id': lambda L: L and L.startswith('additionalinfo-section')})
                    print len(addInfos)
                    dictadinfos = {}
                    i = 1
                    for info in addInfos:
                        key = 'adinfo' + str(i)
                        dictadinfos[key] = info.text
                        i += 1
                    print dictadinfos
            resume_to_csv(dictworkexps,dicteducations)
            break

    except:
        print 'No resume Found'
    #     generate_csv(jobId, eachJobUrl, jobTitle, jobLocation, company, jobDescription, writer)
    #     break

def go_to_next_page(url):
    print url
    try:
        soup = getSoap(url)
    except:
        print 'cant load pagination page'
    parse_each_page(soup)
    try:
        pagination = soup.find_all('a', attrs={'class': 'next'})
        nextPageUrl = 'https://www.indeed.com/resumes' + pagination[0]['href']
        go_to_next_page(nextPageUrl)
    except:
        print 'No pagination'

def runParser(searchSyntax):
    soup = getSoap(searchSyntax)
    print soup
    # try:
    #     pagination = soup.find_all('a', attrs={'class': 'next'})
    #     nextPageUrl =  'https://www.indeed.com/resumes' + pagination[0]['href']
    #     go_to_next_page(nextPageUrl)
    # except:
    #     print 'No pagination'

runParser('https://www.zillow.com/homedetails/121-Parkwood-Dr-Royal-Palm-Beach-FL-33411/46896650_zpid/')



