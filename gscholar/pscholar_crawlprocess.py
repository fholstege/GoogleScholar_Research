import time
import os
import sys
import pandas as pd
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from spiders.profspider import profspider


N_links_perCrawl = 200

file_withlinks = pd.read_csv('files/physics_links.csv', sep=',')

N_requests = len(file_withlinks['link'])

links_to_crawl = file_withlinks['link'].tolist()

N_crawls = int(N_requests / N_links_perCrawl)

configure_logging()
runner = CrawlerRunner()

first = True

@defer.inlineCallbacks

def crawl():
	for i in range(N_crawls + 1):


		firstrow = i * N_links_perCrawl
		lastrow = (i + 1) * N_links_perCrawl
		links_curr_crawl = links_to_crawl[firstrow:lastrow]

		yield runner.crawl(profspider, links=links_curr_crawl)
		print("Scraper paused")
		time.sleep(30)
	
	reactor.stop()

crawl()
reactor.run()