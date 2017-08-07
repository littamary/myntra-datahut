import scrapy

class Myntra(scrapy.Spider):
    name = "myntra"
    start_urls = ["https://www.myntra.com/"]

    def parse(self, response):
        sublink_selector = response.xpath('//div[@class="desktop-navContent"]/div[@class="desktop-navLink"]/div/div/ul/li/a')
        # print(len(sublink_selector))
        for each in sublink_selector:
            print(each.css('a::attr(href)').extract_first())
        # sublinks = sublink_selector.css('a::attr(href)').extract_first()
        # print(sublinks)
