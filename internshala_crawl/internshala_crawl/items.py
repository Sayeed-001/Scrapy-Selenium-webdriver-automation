# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

def validate_field(field):
	if field:
		pass
	else:
		field = 'nan'
	return field

class InternshalaCrawlItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	job_header = scrapy.Field()
	company_name = scrapy.Field()
	start_date = scrapy.Field()
	job_location = scrapy.Field()
	job_duration = scrapy.Field()
	stipend = scrapy.Field()
	last_date = scrapy.Field()
	intern_url = scrapy.Field()