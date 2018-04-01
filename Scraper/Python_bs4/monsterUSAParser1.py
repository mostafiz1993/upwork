
# coding: utf-8

# In[32]:

import requests, time
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')

try:
    df = pd.read_csv('monsterUSAData.csv')
except:
    df = pd.DataFrame(columns=['job_id', 'job_title', 'job_link', 'comapny_name', 'location', 'date_posted','industry', 'salary', 'job_description'])


# In[33]:

# auth = requests.post("http://api.raasforce.com/Token","grant_type=password&username=azim.raasforce@gmail.com&password=123456")
# token = auth.json()['access_token']

job = 'Solutions Architect'
url = 'https://www.monster.com/jobs/search/?q=' +job + '&sort=dt.rv.di&page={}'

soup = get_soup(url.format('1'))
jobs = soup.find('section', {'id': 'resultsWrapper'}).findAll('article', {'class': 'js_result_row'})

total_results = soup.find('h2', {'class': 'page-title visible-xs'}).text.split('Jobs')[0].strip()
if total_results[-1]=='+': total_results = int(total_results[:-1])
total_pages = int(total_results/len(jobs))

print(total_pages)

# In[34]:

def job_details(job):
    a = 'class'
    b = 'jobTitle'
    c = 'div'
    t = job.find(c, {a: b})
    
    job_title = t.text.strip()
    job_id = t.find('a')['data-m_impr_j_jawsid']
    job_link = t.find('a')['href']
    company_name = job.find('div', {'class': 'company'}).text.strip()
    location = job.find('div', {'class': 'job-specs-location'}).text.strip()
    date_posted = job.find('div', {'class': 'job-specs-date'}).text.strip()
    
    industry = ''
    salary = ''
    job_description = ''
    if 'job-openings.monster.com' in job_link:
        new_soup = get_soup(job_link)
        # for x in new_soup.findAll('section', {'class': 'summary-section'}):
        #     if x.find('h2').text.strip() == 'Industries':
        #         industry = x.find('h3').text.strip()

        #     elif x.find('h2').text.strip() == 'Salary':
        #         salary = x.find('h3').text.strip()

        try:
            job_description = new_soup.find('div', {'id': 'JobDescription'}).text.strip().replace('  ', '').replace('\xa0', '')
        except:
            pass
               
    return [job_id, job_title, job_link, company_name, location, date_posted, industry, salary, job_description]


# In[35]:

for page in range(4, total_pages+1):
    soup = get_soup(url.format(str(page)))
    jobs = soup.find('section', {'id': 'resultsWrapper'}).findAll('article', {'class': 'js_result_row'})
    print('Current Page:'+str(page) )
   
    #headers = {'Authorization': 'Bearer '+token }

    for job in jobs:
        job_info = job_details(job)
       
        job_id = job_info[0]
        job_title = job_info[1]
        job_link = job_info[2]
        company_name = job_info[3]
        location = job_info[4]
        date_posted = job_info[5]
        salary = job_info[7]
        desc = job_info[8]
        
        data = {
                'DisplayId'     :       job_id,
                'JobTitle'      :       job_title,
                'JobDescription':       desc,
                'WorkAddress'   :       location,
                'SeoMetaDescription'   :job_link,
                'SeoMetaTitle'   :      company_name,
                'SeoMetaTags'    :      salary,
                'CompanyName'    :      company_name,
                'JobEducation'   :      date_posted
                }

        print(data)
        # try:
        #     r = requests.post("http://api.raasforce.com/api/HtmlExtractJob/SaveToTempTable", data,headers=headers)
        #     status = r.json()['id']
        # except:
        #     p = 0

        time.sleep(2)
   
    #break #remove this to get all jobs
    

    print('*******************************')
    print('***********  Done  ************')


# In[ ]:



