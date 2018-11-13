"""
spider class that extract information of N professors for the subject physics
usage: cd the root folder, and then run scrapy runspider scraper.py
"""


# import relevant libraries
import scrapy
import re
import html2text
import pandas as pd
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

# create spider class
class GoogleScholarSpider(scrapy.Spider):
	
	# name spider
	name = "GoogleScholar_spider"

	# define start url
	start_urls = ["https://scholar.google.nl/citations?hl=nl&view_op=search_authors&mauthors=label%3Aphysics&btnG="]

	def __init__(self):
		"""
		when spider class is initialized, define the paramters
		"""

		# define label sought after, and base link for searched
		self.curr_subj = "label:physics"
		self.link_base = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
		
		# number of current professors, and maximum number of professors
		self.curr_N_prof = 10
		self.max_prof = 10000

		# placeholder for dataframe with professor data
		self.prof_entries = []

		# acquire signal when spider is closed
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	# function to extract relevant data from a professor profile
	def parse_profile(self, response):

		# select name of professor
		name_select = 'div[id="gsc_prf_in"]::text'

		# retrieve name of professor
		prof_name = response.css(name_select).extract_first()

		# acquire all-time indexes for professor
		select_profstats = 'td.gsc_rsb_std::text'

		# extract stats out of table in professor's page
		profstats = response.css(select_profstats).extract()

		# define property of each professor stat
		# _5 means the same statistic, but only for the last five years
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

		# add entry to list of dicts with all entries 
		self.prof_entries.append(entry)

	def parse(self, response):

		# object with professor profile 
		profiles = 'div.gsc_1usr.gs_scl'

		# go through each profile 
		for profile in response.css(profiles):

	    	# the selectors for profile name, text, and link to profile 
		    name_link = 'h3 a::attr(href)'

		    # get id of professors profile 
		    prof_profile_id = profile.css(name_link).extract_first()

		    # create link to profile using id
		    link_profile = "https://scholar.google.com/" + prof_profile_id

		    yield scrapy.Request(link_profile, callback = self.parse_profile, dont_filter=True)

			# select the next page
		    next_page_select = 'button[aria-label="Next"]::attr(onclick)'
		    next_page = response.css(next_page_select).extract_first()


		# if there is a next page, and the max of professors searched has not been reached, go to next page
		if next_page and self.curr_N_prof < self.max_prof:

			# count in the added professors
			self.curr_N_prof = self.curr_N_prof + 10

			# regex pattern to uncover the code for next url
			pattern = r'.*?after_author(.*)x26astart.*' 

			# retrieve code for next url from "button@onclick" object
			match_link = re.search(pattern, next_page)

			# clean the string to form new link 
			nextpage_code = match_link.group(1)[4:-1]

			# combine base link with current subject, the code, and current N of professors
			nextpage_link = self.link_base + self.curr_subj +"&after_author="+ nextpage_code + "&astart=" + str(self.curr_N_prof)

	    	# send scrapy to next link, with callback to parse method 
			yield scrapy.Request(nextpage_link, callback=self.parse, dont_filter=True)

	# function to write out the dataframe with professor data to csv
	def profdata_to_csv(self, name_csv):

		# create dataframe from list of dicts
		df_profs = pd.DataFrame.from_records(self.prof_entries)

		# write out dataframe to csv with filename = name_csv 
		df_profs.to_csv(name_csv)

	# when spider closed, activate function profdata_to_csv
	def spider_closed(self, spider):

		self.profdata_to_csv(self.curr_subj + "_GoogleScholarData.csv")








	

