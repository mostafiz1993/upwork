import scrapy
import cfscrape


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # start_urls = [
    #     'https://myip.ms/browse/sites/100/own/376714',
    #
    websiteUrl = []
    for i in range(1,3,1):
        websiteUrl.append('https://myip.ms/browse/sites/' + str(i) + '/own/376714' )
    def start_requests(self):
        urls = self.websiteUrl
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.css('tbody tr')
        for i in range(0,len(rows),2):
            yield {
                'name': rows[i].css('td.row_name a::text').extract_first(),
                'websitePopularRating' : rows[i].css('span.bold::text').extract_first(),
                'noOfVisitor' : rows[i+1].css('span.bold::text').extract_first(),
                'recordUpdateTime' : rows[i+1].css('div.sval::text')[-1].extract(),
            }
        # rows = response.css('tr.odd td.row_name a::text').extract()
        # for row in rows:
        #     yield {
        #         'name': row,
        #
        #
        #     }
