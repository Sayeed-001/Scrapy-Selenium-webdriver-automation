### Scrapy-Selenium-webdriver-automation

#### NOTE: Before execution, Register as a new user on internshala.com to access the login credentials i.e your registered username and password. To use Selenium, you'll also need Chrome's webdriver. This Program does not install chromedriver, if you required go to https://chromedriver.chromium.org/downloads check your OS and download from the link.

Make changes in PARAMATERS.PY file where you need to mention your chromedriver path, your internshala username, internshala password to attempt a login to website with your credentials and at last you have to mention the job_category which you want to search and to acquire details in csv, json or xml formats.

#### InternshalaBot
This is a Scrapy/selenium project to scrape data of internship jobs opening on website https://internshala.com. In this code of example, Selenium webdriver is used to attempt a login on a website with your login credentials and search the internship Category along scrapy framework implemented to crawl and fetch the data.

This project is only meant for educational purposes.

## Extracted data
This project extracts Internship job data, combined with the respective Company name, Job location, duration, stipend, Last date to apply for a job and extracted url for the job. The extracted data looks like this:
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
  
If you want to save the scraped data to a file, you can pass the -o option:
  $ scrapy crawl internshala -o results.csv  # Here you can change the O/P file format from csv to json or xml.
'''
