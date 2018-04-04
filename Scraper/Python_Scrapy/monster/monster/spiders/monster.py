import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'monster'

    def __init__(self, *args, **kwargs):
        super(AuthorSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
        #start_urls = ['https://www.monster.com/jobs/search/?q=data-scientist&where=New-York__2C-NY']
    i = 2
    def parse(self, response):

        # for item in response.css('button.mux-btn').extract():
        #     try:
        #         if 'Load more jobs' in item:
        #             if self.i ==2:
        #                 print 'tested'
        #                 nextPageUrl = response.request.url + '&page=' + str(self.i)
        #                 yield scrapy.Request(nextPageUrl, callback=self.parse)
        #             else:
        #                 nextPageUrl = response.request.url.replace('&page='+str(self.i-1),'&page='+str(self.i))
        #                 yield scrapy.Request(nextPageUrl, callback=self.parse)
        #             self.i += 1
        #     except:
        #         pass

        urls = response.css('section.card-content a::attr(href)').extract()
        for url in urls:
            if 'job-openings.monster.com' in url:
                yield  scrapy.Request(url,callback=self.parse_each_page)



    def parse_each_page(self,response):
        jobUrl = response.request.url
        try:
            jobTitle = response.css('h1.title::text').extract_first()
        except:
            jobTitle = ''
        try:
            jobTypeIndex = response.css('section.summary-section dt.key::text').extract().index('Job type')
            jobType = response.css('section.summary-section dd.value::text')[jobTypeIndex].extract()
        except:
            jobType = ''
        try:
            jobLocation = response.css('h2.subtitle::text').extract_first()
        except:
            jobLocation = ''
        try:
            salaryIndex = response.css('section.summary-section dt.key::text').extract().index('Salary')
            salary = response.css('section.summary-section dd.value::text')[salaryIndex].extract()
        except:
            salary = ''
        try:
            educationLevelIndex = response.css('section.summary-section dt.key::text').extract().index('Education level')
            educationLevel = response.css('section.summary-section dd.value::text')[educationLevelIndex].extract()
        except:
            educationLevel = ''
        try:
            careerLevelIndex = response.css('section.summary-section dt.key::text').extract().index('Career level')
            careerLevel = response.css('section.summary-section dd.value::text')[careerLevelIndex].extract()
        except:
            careerLevel = ''

        try:
            descriptions = response.xpath("//div[@id='JobDescription']//text()").extract()
            description = ''
            for des in descriptions:
                description += des
            # descriptions = response.css('div.details-content span p::text').extract()
            # description = ''
            # for des in descriptions:
            #     description += des
            # try:
            #     descriptions2 =  response.css('div.details-content ul li::text').extract()
            #     for des in descriptions:
            #         description += des
            # except:
            #     pass

        except:
            description = ''

        yield {
            'jobUrl' : jobUrl,
            'jobTitle': jobTitle ,
            'jobType' : jobType,
            'jobLocation' : jobLocation,
            'salary' : salary,
            'educationLevel' : educationLevel,
            'careerLevel' : careerLevel,
            'description' : description,


        }

#scrapy crawl monster -o monster.json -a start_url="https://www.monster.com/jobs/search/?q=data-scientist&where=New-York__2C-NY#"

#scrapy crawl monster -o monster.csv -t csv -a start_url="https://www.monster.com/jobs/search/?q=data-scientist&where=New-York__2C-NY"