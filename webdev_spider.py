# -*- coding: utf-8 -*-
import scrapy

BASE_URL = 'https://clutch.co'


class WebDevSpider(scrapy.Spider):
    name = 'webdev'
    webdev_base_url = 'https://clutch.co/web-developers?page=%s'
    start_urls = [webdev_base_url % 0]

    def parse(self, response):
        for company in response.css('h3.company_info'):
            yield {
                'name': company.xpath('a/text()').get().strip(),
                'url': BASE_URL + company.xpath('a/@href').get(),
                
            }
            # div.col-md-3 provider-info__details

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(BASE_URL + next_page, self.parse)
