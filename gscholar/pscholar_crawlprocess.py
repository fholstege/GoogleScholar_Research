import time
import os
import sys
import pandas as pd
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from spiders.profspider import profspider

# define max number of links per crawl
N_links_perCrawl = 500

# read the file with links
file_withlinks = pd.read_csv('files/master_links_GoogleScholar.csv', sep=',')
print(file_withlinks.iloc[:,1])
 
# list with links 
links_to_crawl = file_withlinks.iloc[:,1].tolist()

# the total N of links 
N_links = len(links_to_crawl) 

# total of crawls 
N_crawls = int(N_links/ N_links_perCrawl)

# configure logging, instigate runner
configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
	for i in range(N_crawls):

		firstrow = i * N_links_perCrawl
		lastrow = (i + 1) * N_links_perCrawl
		links_curr_crawl = links_to_crawl[firstrow:lastrow]

		yield runner.crawl(profspider, links=links_curr_crawl)
		print("Scraper paused")
		time.sleep(300)
	
	reactor.stop()

crawl()
reactor.run()

		