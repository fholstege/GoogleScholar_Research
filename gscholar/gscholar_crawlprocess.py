
"""
 This starts an crawling instance for a gsspider
 usage: python3 gscholar_crawlprocess.py subject N_prof_total N_per_crawl label
 N_per_crawl cannot exceed 1000
 use label = True if label used, if False the general term is used 

"""

# import necessary libraries 
import time
import os
import sys


# first argument passed on: subject to scrape 
subject = sys.argv[1]

# second argument passed on: N of professors to acquire
N_request = int(sys.argv[2])

# third argument passed on: N of professors per crawl
profiles_perCrawl = int(sys.argv[3])

# fourth argument passed on: use label or not
label_check = str(sys.argv[4])

# check if N_request is multiplicate of N per profiles 
if N_request % profiles_perCrawl != 0:
	print("N_request argument always needs to be a multiplicate of ", str(profiles_perCrawl))
	exit()

# check if N_per_crawl is below or equal to 1000
if profiles_perCrawl > 1000:
	print("N_per_crawl argument cannot exceed 1000 for performance reasons")
	exit()

# get N of spider instances that ought to be created
N_spider_instances = N_request / profiles_perCrawl

# count how many spiders currently created
first_instance = True

# loop through spider instances
for instance in range(int(N_spider_instances)):

	cmd_str = "scrapy crawl gsspider -a subject=" + subject + " -a N_request=" + str(profiles_perCrawl) + " -a new_instance=" + str(first_instance) + " -a label=" + label_check
	spider_instance = os.system(cmd_str)
	time.sleep(3)

	# change: no longer first instance
	if first_instance:
		first_instance = False

