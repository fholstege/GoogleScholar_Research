
"""
 This starts an crawling instance for a gsspider
 usage: python3 gscholar_crawlprocess.py subject N_request

"""

# import necessary libraries 
from gscholar.spiders.gsspider import gsspider_class
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys
import time

print(sys.argv)

# get project settings
process = CrawlerProcess(get_project_settings())

# first argument passed on: subject to scrape 
subject = sys.argv[1]

# second argument passed on: N of professors to acquire
N_request = int(sys.argv[2])

# check if N_request is multiplicate of 1250
if N_request % 1250 != 0:
	print("N_request argument always needs to be a multiplicate of 1250")
	exit()

# get N of spider instances that ought to be created
N_spider_instances = N_request // 1250

# count how many spiders currently created
count_spider_instance = 0
first_instance = True

# loop through spider instances
for instance in range(N_spider_instances):

	# indicate to user how many spider instances used
	print("Current N of spider instances: ", count_spider_instance)
	count_spider_instance =+ 1

	# create class of spider instance, start crawl process 
	spider_instance = gsspider_class("physics", 1250, True)

	# pass on same arguments of spider instance
	process.crawl(spider_instance, subject='physics', N_request=1250, new_instance = first_instance)
	# don't stop process after crawl
	process.start( stop_after_crawl=False)

	# after process.start is over, sleep for 5 minutes
	sleep(300)

	# change: no longer first instance
	if first_instance:
		first_instance = False
