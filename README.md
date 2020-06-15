### Scrapy-Selenium-webdriver-automation

#### InternshalaBot
This is a Scrapy/selenium project to scrape data of internship jobs opening on website https://internshala.com. In this code of example, Selenium webdriver is use here to attempt a login on a website with your login credential and search the internship Category and fetch the data.

#### NOTE: Before execution, Register as a new user on internshala.com to access the login credentials i.e your registered username and password. To use Selenium, you'll also need Chrome's webdriver. This Program does not install chromedriver, if you requires, go to https://chromedriver.chromium.org/downloads check your OS and download from the link.

Make changes in PARAMATERS.PY file where you need to mention your chromedriver path, your internshala username, internshala password to attempt a login to the website with your credentials and at last you have to mention the job_category which you want to search and to acquire details in csv, json or xml formats.

## Extracted data
This project extracts Internship job data, combined with the respective rows Company name, Job location, duration, stipend, Last date to apply for a job and extracted url for the job. The extracted data looks like this:
```
{
Job Title : Market Research & Analysis Internship in Bangalore at HR Smartstorey
Company Name : HR Smartstorey
Start Date : Immediately
Job Location : Bangalore
Job Duration : 3 Month
Stipend :  3000 /month
Last Date To Apply : 30 Jun' 20
Url : https://internshala.com/internship/detail/market-research-analysis-internship-in-bangalore-at-hr-smartstorey1591093447 
}
```
### Execution of a program:
```
You can run a spider using the scrapy crawl command in a command line by moving to root directory i.e where scrapy.cfg
  $ scrapy crawl internshala
  
If you want to save the scraped data to a file, you can pass the -o argument option:
  $ scrapy crawl internshala -o results.csv  # Here you can change the O/P file format from csv to json or xml.
'''
## Configuration of databases, check pipelines.py file
SQLite database file will be generated name 'datajobs' in root folder where scrapy.cfg file. And, you can easily access SQLite databse file through online, Go to https://sqliteonline.com/ from here you can access the datajobs file.
```
## Configuration and integeration of MySQL database with this program. You will find MySQLIntegeration-Settings folder which contains two files(pipelines.py and settings.py), you need to replace the pipelines.py file and settings.py from the project folder.
