"""
spider class that extract information of profile page on google scholar
usage: cd the root folder, and then run scrapy runspider scraper.py
"""


# import relevant libraries
import scrapy
import re
import html2text
import pandas as pd
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import csv
import sys


class ProfileScholarSpider(scrapy.Spider):
    name = 'pscholar'
    start_urls = []

    # open csv, and add each line as a start url 
    file = open('/Users/FlorisHolstege/Documents/Freelance/GoogleScholar_Research/gscholar/physics_formatted_linkData.csv', 'r')
    for row in file:
    	formatted = row.split('\n')
    	start_urls.append(formatted[0].strip())

    def __init__(self):

	    # save all entries of profs here
	    self.prof_entries = []
	    self.curr_subj = "physics"

	    # send signal is spider closes
	    dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):

	    name_select = 'div[id="gsc_prf_in"::text'

	    # retrieve name of professor
	    prof_name = response.css(name_select).extract_first()

	    # acquire all-time indexes for professor
	    select_profstats = 'td.gsc_rsb_std::text'

	    # extract stats out of table in professor's page
	    profstats = response.css(select_profstats).extract()

	    # define property of each professor stat
	    tot_citations = profstats[0]
	    tot_citaions_5 = profstats[1]
	    H_index = profstats[2]
	    H_index_5 = profstats[3]
	    I_index = profstats[4]
	    I_index_5 = profstats[5]


	    # select name of institution 
	    select_institution = "a.gsc_prf_ila::text"

	    # acquire institution of professor
	    prof_institution = response.css(select_institution).extract_first()

	    # check: if no institution, or "Homepage", enter "NA"
	    if prof_institution is None or prof_institution is "Homepage": 
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
	    "I_index_5": I_index_5

	    }

	    print(entry)

	    # add entry to list of dicts with all entries 
	    self.prof_entries.append(entry)

    # function to write out the dataframe with professor data to csv
    def profile_to_csv(self, name_csv):

	    # create dataframe from list of dicts
	    df_prof = pd.DataFrame.from_records(self.prof_entries)

	    # write out dataframe to csv with filename = name_csv 
	    df_prof.to_csv(name_csv)

    # when spider closed, activate function profdata_to_csv
    def spider_closed(self, spider):

	    self.profile_to_csv(self.curr_subj + "_profData.csv")
