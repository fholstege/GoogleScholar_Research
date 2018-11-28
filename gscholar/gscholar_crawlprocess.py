
"""
 This starts an crawling instance for a gsspider
 usage: python3 gscholar_crawlprocess.py subject N_request

"""

# import necessary libraries 
import time
import os
import sys

profiles_perCrawl = 20

# first argument passed on: subject to scrape 
subject = sys.argv[1]

# second argument passed on: N of professors to acquire
N_request = int(sys.argv[2])

# check if N_request is multiplicate of N per profiles 
if N_request % profiles_perCrawl != 0:
	print("N_request argument always needs to be a multiplicate of ", str(profiles_perCrawl))
	exit()

# get N of spider instances that ought to be created
N_spider_instances = N_request / profiles_perCrawl

# count how many spiders currently created
first_instance = True

# loop through spider instances
for instance in range(int(N_spider_instances)):

	print(N_spider_instances)
	print(profiles_perCrawl)

	print("Current first instance: ", first_instance)
	cmd_str = "scrapy crawl gsspider -a subject=" + subject + " -a N_request=" + str(profiles_perCrawl) + " -a new_instance=" + str(first_instance)
	print(cmd_str)
	spider_instance = os.system(cmd_str)
	time.sleep(3)

	# change: no longer first instance
	if first_instance:
		first_instance = False

