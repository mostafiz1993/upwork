require 'nokogiri'
require 'open-uri'
require 'json'
require 'rubygems'
require 'watir'
require 'csv'
require 'watir-scroll'

def task2(url)
  domain = url
  html_data = open(url).read
  nokogiriObject = Nokogiri::HTML(html_data)
  scripts = nokogiriObject.css('head script')
  for script in scripts
    if script.text.match('Shopify.shop')
      targetString =  script.text.split(';')
      shopifyStoreDomain = targetString[1].split('=')[1].tr('"', '')
      theme =  targetString[2].split('=')[1].tr('{', '').split(',')[0].split(':')[1].tr('"','')
      shopId  =  targetString[2].split('=')[1].tr('{', '').split(',')[1].split(':')[1]
      return domain,shopifyStoreDomain,theme,shopId
    end
  end
end

#a = task2('https://colourpop.com/')
#puts a


def task3(url)
  browser = Watir::Browser.new
  browser.window.resize_to(1920, 1280)
  browser.goto url
  begin
    products = browser.divs(:class => 'productblock')
    top10 = 0
    for product in products
      hyperlinkDiv =  product.div(:class => 'product-info-inner')
      puts hyperlinkDiv.a.href
      productName = product.div(:id => 'prod-title-price').text
      productPrice = product.div(:class => 'price').text
      puts productName
      puts productPrice
      if top10 == 9
        break
      end
      top10 += 1
    end
  rescue
    puts 'No product Found'
  end
end


#task3('https://colourpop.com/collections/all?sort_by=best-selling')
#

def parse_each_page_for_task1(b,output)
  rows =  b.tr(:class => 'odd').parent.trs
  rowSize = rows.size
  for i in (0..rowSize-1).step(2)
    clickArea = rows[i].td(:class => 'arial collapsible').a
    clickArea.click
    sleep(1)
    website = rows[i].td(:class => 'row_name').a.text
    rating = rows[i].span(:class => 'bold arial grey').text
    websiteVisitor =  rows[i+1].td.span(:class => 'bold arial grey').text
    sizeofdivOfRecordUpdateTime = rows[i+1].td.divs(:class => 'sval').size
    divOfRecordUpdateTime = rows[i+1].td.divs(:class => 'sval')
    recordUpdateTime =  divOfRecordUpdateTime[sizeofdivOfRecordUpdateTime-1].text
    puts website
    puts rating
    puts websiteVisitor
    puts recordUpdateTime
    clickArea.click
    write_to_csv(website,rating,websiteVisitor,recordUpdateTime,output)
    if(i%6 == 0)
      b.scroll.to [0,500+i*30]
    end
  end
  sleep(4)
  click_next_page_for_task1(b,output)

end


def click_next_page_for_task1(brow,output)
  begin
    brow.scroll.to [0,500]
    brow.a(:class => 'aqPagingSel').element(:xpath => './following-sibling::*').click
    sleep(3)
    parse_each_page_for_task1(brow,output)
  rescue
    puts 'Done'
  end
end

def write_to_csv(website,rating,websiteVisitor,recordUpdateTime,csv)
  csv << [website,rating,websiteVisitor,recordUpdateTime]
end

def task1(url)
  currentTime = DateTime.now
  csvName = 'shopify_' + currentTime.strftime("%d_%m_%Y_%H:%M:%S") + '.csv'
  output = CSV.open(csvName ,"a+",:write_headers=> true,
                    :headers => ["website","rating","websiteVisitor","recordUpdateTime"])
  browser = Watir::Browser.new
  browser.window.resize_to(1920, 1280)
  browser.goto url
  browser.scroll.to [0, 500]
  rows =  browser.tr(:class => 'odd').parent.trs
  rowSize = rows.size
  for i in (0..rowSize-1).step(2)
    clickArea = rows[i].td(:class => 'arial collapsible').a
    sleep(3)
    clickArea.click
    sleep(1)
    website = rows[i].td(:class => 'row_name').a.text
    rating = rows[i].span(:class => 'bold arial grey').text
    websiteVisitor =  rows[i+1].td.span(:class => 'bold arial grey').text
    sizeofdivOfRecordUpdateTime = rows[i+1].td.divs(:class => 'sval').size
    divOfRecordUpdateTime = rows[i+1].td.divs(:class => 'sval')
    recordUpdateTime =  divOfRecordUpdateTime[sizeofdivOfRecordUpdateTime-1].text
    puts website
    puts rating
    puts websiteVisitor
    puts recordUpdateTime
    clickArea.click
    write_to_csv(website,rating,websiteVisitor,recordUpdateTime,output)
    if(i%6 == 0)
      browser.scroll.to [0,500+i*30]
    end
  end
  sleep(3)
  click_next_page_for_task1(browser,output)
end


task1('https://myip.ms/browse/sites/1/own/376714')
