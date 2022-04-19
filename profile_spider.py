# -*- coding: utf-8 -*-
import os
import re
import json

import scrapy
import ijson


HANDLE_HTTP_STATUSES = [403, 404]

here = os.path.dirname(os.path.abspath(__file__))
companies_file = os.path.join(here, 'out', 'webdev.json')
companies = ijson.items(open(companies_file), 'item')


class ProfileSpider(scrapy.Spider):
    name = 'profile'
    start_urls = (company['url'] for company in companies)
    handle_httpstatus_list = HANDLE_HTTP_STATUSES

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',  # don't stop scraping when url wad duped
    }

    def parse(self, response):
        if response.status in HANDLE_HTTP_STATUSES:
            return


       
        
        

        yield {
            'Company name': response.css('h1.header-company--title a.website-link__item::text').get().strip(),
            'Location': response.css('span.location-name::text').get().strip(),
            'Website': response.css('a.website-link__item::attr(href)').get(),
            'Contact': response.css('a.contact.phone_icon::text').get().strip(),
            'Review Count':  response.css('a.reviews-link.sg-rating__reviews::text').get().strip().replace(' ','').replace('\n' ,''),
            'Rating':  response.css('div.rating-reviews span::text').get().strip(),
            'Min. Project Size': response.css('div.col-md-3 span::text')[0].getall(),
            'Avg.Hourly Rate' : response.css('div.col-md-3 span::text')[1].getall(),
            'Employees': response.css('div.col-md-3 span::text')[2].getall(),
            # 'Founded date':
            #     'Undisclosed' if response.css('div.field-name-field-pp-year-founded').css('.undisclosed')
            #     else response.css('div.field-name-field-pp-year-founded div.field-item::text').get(),
           
        }
