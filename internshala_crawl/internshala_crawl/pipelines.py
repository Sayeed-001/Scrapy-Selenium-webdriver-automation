# -*- coding: utf-8 -*-

# Define your item pipelines here
# Create New Sqlite database and stored the scraped items in databse.
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from sqlite3 import Error
import re

class InternshalaCrawlPipeline:
	def __init__(self):
		self.create_connection()
		self.create_table()

	# New connection with database
	def create_connection(self):
		try:

			self.conn = sqlite3.connect('datajobs.db')
			print("Connection is established: Database is created in memory.")
		
		except Error:

			print(error)

		self.curr = self.conn.cursor()

	# Create a new in table in database
	def create_table(self):
		self.curr.execute("""DROP TABLE IF EXISTS jobs_tb""") # Drops the table if already exists
		# Create a new table after drop
		self.curr.execute("""create table jobs_tb(
						JobHeader text,
						CompanyName text,
						StartDate text,
						JobLocation text,
						JobDuration real,
						Stipend real,
						LastDate text,
						InternUrl	
					)""")

	# Item processing
	def process_item(self, item, spider):
		
		self.store_db(item)  
		
		if item['job_duration']:
			item['job_duration'] = ' '.join(item['job_duration']).strip()
			item['job_duration'] = re.sub("s+","", item['job_duration'])

		return item

	# Storing the scraped data points to sqlite database table
	def store_db(self, item):
		self.curr.execute("""insert into jobs_tb(JobHeader, CompanyName, StartDate, JobLocation,
						 JobDuration, Stipend, LastDate, InternUrl) values(?,?,?,?,?,?,?,?) """, 
						(
							str(item['job_header']),
							str(item['company_name']),
							str(item['start_date']),
							str(item['job_location']),
							str(item['job_duration']),
							str(item['stipend']),
							str(item['last_date']),
							str(item['intern_url']),
						))

		self.conn.commit()