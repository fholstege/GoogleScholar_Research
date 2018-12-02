"""
spider class that extract information of profile page on google scholar
"""


# import relevant libraries
import scrapy
import re
import html2text
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.extensions import closespider
import csv
import sys
import pandas as pd
import time


class ProfileScholarSpider(scrapy.Spider):
    name = 'prof_spider'
    
    start_urls = []
    # open csv, and add each line as a start url 
    file = open('files/master_links_GoogleScholar.csv', 'r')

    colnames = ['index','H_index','H_index_5','I_index','I_index_5','prof_insti','prof_name','tot_citations','tot_citations_5','url']
    data = pd.read_csv('files/profData.csv', names=colnames)
    scraped_urls = data.url.tolist()

    for row in file:
    	raw_row= row.split('\n')
    	split_row = raw_row[0].split(',')
    	url = split_row[1]
    	url = url.strip()

		# check if we have already scraped it, if not, let it be!
    	if not url in scraped_urls:
    		start_urls.append(url)

    def __init__(self):

	    # save all entries of profs here
	    self.prof_entries = []

	    # send signal is spider closes
	    dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):

	    name_select = 'div[id="gsc_prf_in"]::text' 
		
	    # retrieve url of professor
	    prof_url = response.url

	    # retrieve name of professor
	    prof_name = response.css(name_select).extract_first()

	    # acquire all-time indexes for professor
	    select_profstats = 'td.gsc_rsb_std::text'

	    # extract stats out of table in professor's page
	    profstats = response.css(select_profstats).extract()

	    # define property of each professor stat
	    tot_citations = profstats[0]
	    tot_citations_5 = profstats[1]
	    H_index = profstats[2]
	    H_index_5 = profstats[3]
	    I_index = profstats[4]
	    I_index_5 = profstats[5]


	    # select name of institution 
	    select_institution = "a.gsc_prf_ila::text"

	    # acquire institution of professor
	    prof_institution = response.css(select_institution).extract_first()

	    # check: if no institution, or "Homepage", enter "NA"
	    if prof_institution is None or prof_institution == "Homepage": 
		    prof_institution = "NA"

	    # entry: a dict of professor features 
	    entry = {

	    "prof_name": prof_name,
	    "prof_insti": prof_institution,
	    "tot_citations": tot_citations,
	    "tot_citations_5": tot_citations_5,
	    "H_index": H_index,
	    "H_index_5": H_index_5,
	    "I_index": I_index,
	    "I_index_5": I_index_5,
		"prof_url": prof_url

	    }

	    print(entry)

	    # add entry to list of dicts with all entries 
	    self.prof_entries.append(entry)

	    if len(self.prof_entries) % 50 == 0:
	    	raise CloseSpider('Does this work?')


    # function to write out the dataframe with professor data to csv
    def profile_to_csv(self, name_csv):

	    # create dataframe from list of dicts
	    df_prof = pd.DataFrame.from_records(self.prof_entries)

	    with open('files/profData.csv', 'a') as current_link_file:
	    	 df_prof.to_csv(current_link_file, header=False)

    # when spider closed, activate function profdata_to_csv
    def spider_closed(self, spider):

	    self.profile_to_csv("files/profData.csv")
