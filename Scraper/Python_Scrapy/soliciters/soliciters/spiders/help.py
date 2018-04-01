response.css('div.according-group section')


phn number

s = response.css('div.accordion-group section')[0].css('dl')[0].css('dt').extract()
s.index('<dt>Tel:</dt>')
response.css('div.accordion-group section')[0].css('dl')[0].css('dd')[2].extract()


msil

s = response.css('div.accordion-group section')[0].css('dl')[0].css('dt').extract()
s.index('<dt id="Email">Email: </dt>')
response.css('div.accordion-group section')[0].css('dl')[0].css('dd.slidingDiv a::text').extract()


web


s = response.css('div.accordion-group section')[0].css('dl')[0].css('dt').extract()
s.index('<dt>Web:</dt>')
response.css('div.accordion-group section')[0].css('dl')[0].css('dd')[5].css('dd a::text').extract_first()


head/branch office
response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('em::text').extract_first()

address

response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[0].extract()
response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[1].extract()
response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[2].extract()
response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[3].extract()
response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[4].extract()
zip
response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[(response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text').extract().index('\r\n                '))-2].extract()


response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[(response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text').extract().index('England\r\n\r\n                '))].extract()

response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[0:((response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text').extract().index('\r\n                '))-1)].extract()
without coutry

response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[0:((response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text').extract().index('\r\n                '))-1)].extract()

only country

response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text')[(response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text').extract().index('\r\n                '))-1].extract()

address final

response.css('div.accordion-group section')[0].xpath("//div[@id='main-details-accordion']/dl")[1].css('dd.feature::text').extract()


area of practise in this branch


for li in response.css('div.accordion-group section')[1].xpath("//div[@id='branch-areas-of-practice-accordion']/ul/li"):
    if(li.css('ul')):
        print li.css('ul li').extract_first()


area of practise in this organizartion

for li in response.css('div.accordion-group section')[2].xpath("//div[@id='areas-of-practice-accordion']/ul/li"):
    if(li.css('ul')):
        print li.css('ul li').extract_first()


people,structure
for li in response.css('div.accordion-group section')[3].xpath("//div[@id='people-and-structure-accordion']/div")[0].css('ul li'):
   ....:     print(li.css('a::attr(href)').extract())



next page in people list

response.css('div.search-results-controls div.pagination li.next a::attr(href)').extract_first()


every people go through
for section in response.css('div.items section'):
    print(section.css('header h2 a::attr(href)').extract_first())


people name 
response.xpath("//div[@id='main-content']/article/header/h1/text()").extract_first()exit()

people email

a = response.css('div.panel-half dl')[0].css('dt').extract()
a.index('<dt id="Email">Email: </dt>')
response.css('div.panel-half dl')[0].css('dd.slidingDiv a::text').extract_first()













