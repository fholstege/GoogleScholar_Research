
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

profiles_perCrawl = 100

# get project settings
process = CrawlerProcess(get_project_settings())

# first argument passed on: subject to scrape 
subject = sys.argv[1]

# second argument passed on: N of professors to acquire
N_request = int(sys.argv[2])

# check if N_request is multiplicate of 1250
if N_request % profiles_perCrawl != 0:
	print("N_request argument always needs to be a multiplicate of ", str(profiles_perCrawl))
	exit()

# get N of spider instances that ought to be created
N_spider_instances = 3

# count how many spiders currently created
first_instance = True

print('N_spider_instances:')
print(range(N_spider_instances))

# loop through spider instances
for instance in range(N_spider_instances):

	print(instance)

	# create class of spider instance, start crawl process 
	spider_instance = gsspider_class("physics", profiles_perCrawl, True)

	# pass on same arguments of spider instance
	process.crawl(spider_instance, subject='physics', N_request=profiles_perCrawl, new_instance = first_instance)
	process.start()

	# after process.start is over, sleep for 5 minutes
	time.sleep(1)

	# change: no longer first instance
	if first_instance:
		first_instance = False

