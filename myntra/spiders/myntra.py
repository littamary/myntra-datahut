import json
from json import JSONDecoder
from csv import DictWriter
import os, shutil

datafolder = os.path.join(os.getcwd(), "scrapedData")

try:
    shutil.rmtree(datafolder)
except FileNotFoundError:
    pass

os.mkdir(datafolder)

import scrapy
from scrapy import  Request

class Myntra(scrapy.Spider):
    name = "myntra"
    # scrapy starts scrapping from here
    start_urls = ["https://www.myntra.com/"]

    def parse(self, response):
        """
        	Get all sub links and call scrap_page to scrap each page
        """
        sublink_selector = response.xpath('//div[@class="desktop-navContent"]/div[@class="desktop-navLink"]/div/div/ul/li/a')
        for each in sublink_selector:
            part_url = each.css('a::attr(href)').extract_first()
            follow_url = response.urljoin(part_url) # construct url for the link to follow
            yield Request(url=follow_url, callback=self.scrap_page) # start a new request, with a callback

    def scrap_page(self, response):
        """
            this function is called after the getting response from the request created in the parse fn.
            scrapped data is stored in the directory call scrapedData in the directory myntra/spiders
        """
        script = response.xpath('/html/body/script[contains(text(),"searchData")]/text()').extract_first()
        script = script.replace("window.__myx = ", "")
        script = self.turn_to_json(script)
        decoder = JSONDecoder()
        script = decoder.raw_decode(script)[0]
        f = open(os.path.join(datafolder, response.url.replace('/','-')+".csv"), 'w')
        products_list = script["searchData"]["results"]["products"]
        fieldnames = products_list[0].keys()
        dictwriter = DictWriter(f, fieldnames=fieldnames)
        dictwriter.writeheader()
        for product in products_list:
            dictwriter.writerow(product)
        f.close()

    @staticmethod
    def turn_to_json(data):
    	"""
    	Turn data (str) to a json
    	"""
        _json = json.loads(json.dumps(data))
        return _json