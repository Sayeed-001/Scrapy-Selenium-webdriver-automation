# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Inserting data to MYSQL database directly.
import MySQLdb
from scrapy.exceptions import NotConfigured

import re

class InternshalaCrawlPipeline:
	def __init__(self, db, user, passwd, host, port):
		# Initializing the MySQL database connection, check settings.py file
		self.db = db
		self.user = user
		self.passwd = passwd
		self.port = port
		self.host = host
		

	@classmethod
	def from_crawler(cls, crawler):
		# fetching MySQL settings from settings.py file
		db_settings = crawler.settings.getdict("DB_SETTINGS")
		
		if not db_settings:
			raise NotConfigured
		
		db = db_settings['db']
		user = db_settings['user']
		passwd = db_settings['passwd']
		host = db_settings['host']
		port = db_settings['port']
		return cls(db, user, passwd, host, port)

	def open_spider(self, spider):
		# Connecting to the MySQL database server 
		self.conn = MySQLdb.connect(db=self.db,
							   user=self.user,
							   passwd=self.passwd,
							   host=self.host,
							   port=self.port,
							   charset='utf8', use_unicode=True)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if item['job_duration']:
			item['job_duration'] = ' '.join(item['job_duration']).strip()
			item['job_duration'] = re.sub("s+","", item['job_duration'])

		# Inserting scrapped data points to MySQL database directly table name is jobs_tb.
		sql = "INSERT INTO jobs_tb(JobHeader, CompanyName, StartDate, JobLocation, JobDuration, Stipend, LastDate, InternUrl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		
		self.cursor.execute(sql,
							(
								item.get("job_header"),
								item.get("company_name"),
								item.get("start_date"),
								item.get("job_location"),
								item.get("job_duration"),
								item.get("stipend"),
								item.get("last_date"),
								item.get("intern_url"),

							)
							)
		self.conn.commit()
		return item