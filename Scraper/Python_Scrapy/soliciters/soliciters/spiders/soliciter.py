import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'soliciter'

    start_urls = ['javhttp://solicitors.lawsociety.org.uk/search/results?Type=0&IncludeNlsp=True&AreaOfPractice2=AGR&Pro=True&parameters=%2C1%3BAPL%2C0%3B%2C1%3BPUB%2C0%3B%2C1%3BADV%2C0%3B%2C1%3BAGR%2C0%3B%2C1%3BAVI%2C0%3B%2C1%3BBAN%2C1%3B%2C1%3BBEN%2C0%3B%2C1%3BCHA%2C0%3B%2C1%3BCHI%2C0%3B%2C1%3BCLI%2C0%3B%2C1%3BCOL%2C1%3B%2C1%3BPCO%2C1%3B%2C1%3BCCL%2C0%3B%2C1%3BCOS%2C1%3B%2C1%3BCOM%2C1%3B%2C1%3BCON%2C1%3B%2C1%3BCSU%2C0%3B%2C1%3BCSF%2C0%3B%2C1%3BCSG%2C0%3B%2C1%3BCUT%2C0%3B%2C1%3BCTR%2C1%3B%2C1%3BPRE%2C0%3B%2C1%3BCFI%2C1%3B%2C1%3BCRD%2C0%3B%2C1%3BCRF%2C0%3B%2C1%3BCRG%2C0%3B%2C1%3BCRJ%2C0%3B%2C1%3BCRL%2C0%3B%2C1%3BCRM%2C0%3B%2C1%3BCRS%2C0%3B%2C1%3BCRO%2C1%3B%2C1%3BDEB%2C0%3B%2C1%3BDTR%2C1%3B%2C1%3BDEF%2C0%3B%2C1%3BDRC%2C0%3B%2C1%3BDRO%2C1%3B%2C1%3BEDU%2C0%3B%2C1%3BEMP%2C1%3B%2C1%3BENE%2C0%3B%2C1%3BENV%2C0%3B%2C1%3BEUN%2C0%3B%2C1%3BFDS%2C0%3B%2C1%3BFAM%2C0%3B%2C1%3BFAL%2C0%3B%2C1%3BFMC%2C0%3B%2C1%3BFME%2C0%3B%2C1%3BFML%2C0%3B%2C1%3BFPL%2C0%3B%2C1%3BFIS%2C0%3B%2C1%3BHRI%2C0%3B%2C1%3BIMA%2C0%3B%2C1%3BIML%2C0%3B%2C1%3BIMM%2C0%3B%2C1%3BIMG%2C0%3B%2C1%3BIMN%2C0%3B%2C1%3BITE%2C1%3B%2C1%3BINS%2C1%3B%2C1%3BIUR%2C1%3B%2C1%3BIPR%2C1%3B%2C1%3BJRW%2C0%3B%2C1%3BJRL%2C0%3B%2C1%3BLCO%2C1%3B%2C1%3BLRE%2C0%3B%2C1%3BPOA%2C0%3B%2C1%3BLIC%2C1%3B%2C1%3BLIV%2C0%3B%2C1%3BLIS%2C0%3B%2C1%3BLIT%2C0%3B%2C1%3BMAR%2C0%3B%2C1%3BMED%2C1%3B%2C1%3BMHE%2C0%3B%2C1%3BMHL%2C0%3B%2C1%3BMAA%2C1%3B%2C1%3BMIL%2C0%3B%2C1%3BNDI%2C0%3B%2C1%3BPEN%2C1%3B%2C1%3BPIN%2C0%3B%2C1%3BPIR%2C0%3B%2C1%3BPLA%2C0%3B%2C1%3BPRZ%2C0%3B%2C1%3BPRP%2C0%3B%2C1%3BPRT%2C0%3B%2C1%3BPRW%2C0%3B%2C1%3BPCI%2C0%3B%2C1%3BPCP%2C0%3B%2C1%3BPCT%2C0%3B%2C1%3BPCW%2C0%3B%2C1%3BPNE%2C0%3B%2C1%3BTAX%2C0%3B%2C1%3BTAC%2C1%3B%2C1%3BTAE%2C0%3B%2C1%3BTAH%2C1%3B%2C1%3BTAM%2C0%3B%2C1%3BTAP%2C0%3B%2C1%3BTAT%2C0%3B+']
    i = 1
    def parse(self, response):
        # follow links to author pages
        for section in response.xpath("//div[@id='results']/section").css('header h2 a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(section),
                                 callback=self.parse_author)
        next_page_path = response.css('div.pagination li.next a::attr(href)').extract_first()
        if next_page_path is not None:
            next_page = response.urljoin(next_page_path)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_author(self, response):

        yield {
            'name': response.xpath("//div[@id='main-content']/article/header/h1").extract_first(),
            
        }
