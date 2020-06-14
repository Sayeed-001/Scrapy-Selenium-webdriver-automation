
# -*- coding: utf-8 -*-
import logging

from time import sleep

from internshala_crawl import paramaters
from internshala_crawl.items import InternshalaCrawlItem, validate_field

from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger


class InternshalaSpider(Spider):
	name = 'internshala'
	allowed_domains = ['internshala.com']

	def __init__(self):
		# configure Chrome Webdriver
		# Add additional Options to the webdriver
		chrome_options = Options()
		# add the argument and make the browser Headless.
		#chrome_options.headless =True
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument("start-maximized")
		chrome_options.add_argument("--disable-extensions")

		seleniumLogger.setLevel(logging.WARNING)

		self.driver = webdriver.Chrome(options=chrome_options)
		self.driver.implicitly_wait(10)
		
	
	def start_requests(self):
		wait = WebDriverWait(self.driver, 20) 
		# open internshala.com login page
		self.driver.get(paramaters.url)
		
		# Click on login tab
		login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='nav-item']/button")))
		login_button.click()
		
		# Insert username in login pop up
		user_email = self.driver.find_element_by_id('modal_email')
		user_email.send_keys(paramaters.internshala_user)
		sleep(2)
		
		# Insert password on login
		user_password = self.driver.find_element_by_id('modal_password')
		user_password.send_keys(paramaters.user_password)
		sleep(2)
		
		# Click to sign in
		sign_in_button = self.driver.find_element_by_id('modal_login_submit')
		sign_in_button.click()
		sleep(3)
		self.logger.info("User Successfully Login.")
	
		#Online_trainng_page = self.driver.find_element_by_xpath('//*[@id="dropdown"]/ul/li[2]/a')
		#Online_trainng_page.click()
		
		# Uncomment me if you already checked the preferences column in filter section on website if not pass.
		#uncheck_preferences = self.driver.find_element_by_xpath('//*[@id="matching_preference_label"]')
		#uncheck_preferences.click()

		# This gives the names of the categorys available to search a job. output of this command is given in paramaters.py file for reference 
		# available_categorys = sel.xpath('//*[@id="select_category_chosen"]/div/ul/li/text()').extract() 
		
		# selects the job type search cell 
		select_category = wait.until(EC.element_to_be_clickable((By.ID, "select_category_chosen")))
		select_category.click()
		
		# send keys used to send the search text in search field. 
		enter_category = self.driver.find_element_by_xpath('//*[@id="select_category_chosen"]/ul/li/input')
		enter_category.send_keys(paramaters.JOB_CATEGORY, Keys.RETURN)
		self.logger.info("Category Searched Successfully.")
		self.logger.info("----------Sleeping for 5 seconds.------------")
		sleep(5)

		# Selecting page source to fetch urls amd data points
		sel = Selector(text=self.driver.page_source)

		# Extracts the job urls available on the webpage
		urls = sel.xpath('//*[@class="heading_4_5 profile"]/a/@href').extract()[:3]
		for job in urls:
			absolute_job_url = paramaters.url + job
			yield Request(absolute_job_url, callback=self.parse_intern)
			self.logger.info('Job URLs Scraped Successfully.')
		
		# Pagination
		while True:
			
			next_page_link = self.driver.find_element_by_id("navigation-forward")
			if 'disabled' in next_page_link.get_attribute('class'):
				print('No more pages to LOAD')
				self.driver.quit()
				break
			
			next_page_link.click()
			self.logger.info("Next Page Click - Wait Yaar")
			sleep(3)

			# Extracting urls from next page
			sel = Selector(text=self.driver.page_source)
			urls = sel.xpath('//*[@class="heading_4_5 profile"]/a/@href').extract()[:3]
			for job in urls:
				absolute_job_url_two = paramaters.url + job
				yield Request(absolute_job_url_two, callback=self.parse_intern)
				self.logger.info('Job URLs Scraped Successfully')
		
	def parse_intern(self, response):
		# Load items loader to isolate the scraped data points
		l = ItemLoader(item=InternshalaCrawlItem(), response=response)

		# Extracting the data points
		job_header =  response.xpath('normalize-space(//*[@id="details_container"]/div[2]/text())').extract_first()

		company_name = response.xpath('normalize-space(//*[@class="heading_6 company_name"]/a/text())').extract_first()

		start_date = response.xpath('//*[@class="start_immediately_desktop"]/text()').extract_first()

		job_location = response.xpath('//*[@class="location_link"]/text()').extract_first()

		job_duration = response.xpath('//*[@class="other_detail_item "]/div[2]/text()').extract()

		stipend = response.xpath('//*[@class="other_detail_item  stipend_container"]/div[2]/span/text()').extract_first()
	
		last_date = response.xpath('//*[@class="other_detail_item  apply_by"]/div[2]/text()').extract_first()

		intern_url = response.url

		# Validation check, if scraped item is null, then validate_field function will replace the null value with NAN.
		job_header = validate_field(job_header)
		company_name = validate_field(company_name)
		start_date = validate_field(start_date)
		job_location = validate_field(job_location)
		job_duration = validate_field(job_duration)
		stipend = validate_field(stipend)
		last_date = validate_field(last_date)
		intern_url = validate_field(intern_url)

		# Adding scraped data points to item loaders containers setup in items.py file.
		l.add_value('job_header', job_header)
		l.add_value('company_name', company_name)
		l.add_value('start_date', start_date)
		l.add_value('job_location', job_location)
		l.add_value('job_duration', job_duration)
		l.add_value('stipend', stipend)
		l.add_value('last_date', last_date)
		l.add_value('intern_url', intern_url)

		return l.load_item()