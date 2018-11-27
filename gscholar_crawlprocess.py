
"""
 This starts an crawling instance for a gsspider
 usage: python3 gscholar_crawlprocess.py subject N_request

"""

# import necessary libraries 
from gscholar.spiders.gsspider import gsspider_class
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys

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


N_spider_instances = N_request // 1250

for instance in range(N_spider_instances):

	spider_instance = gsspider_class("physics", 1250, True)
	process.crawl(spider_instance, subject='physics', N_request=100, new_instance = True)
	process.start()
