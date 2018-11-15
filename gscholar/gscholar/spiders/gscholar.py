"""
spider class that extracts links of google scholar profiles
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
	name = "gscholar"

	# define start url
	start_urls = ["https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3Aphysics&btnG="]

	def __init__(self):
		"""
		when spider class is initialized, define the paramters
		"""

		# define label sought after, and base link for searched
		self.curr_subj = "physics"
		self.link_base = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
		
		# number of current professors, and maximum number of professors
		self.curr_N_prof = 10
		self.max_prof = 100000

		# placeholder for dataframe with professor data
		self.link_entries = []

		# acquire signal when spider is closed
		dispatcher.connect(self.spider_closed, signals.spider_closed)


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

		    # entry to dataset with links

		    self.link_entries.append(link_profile)

		    print("LINK FOUND: ", link_profile)

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
			nextpage_link = self.link_base + "label:"+self.curr_subj +"&after_author="+ nextpage_code + "&astart=" + str(self.curr_N_prof)

	    	# send scrapy to next link, with callback to parse method 
			yield scrapy.Request(nextpage_link, callback=self.parse, dont_filter=True)

	# function to write out the dataframe with professor data to csv
	def profdata_to_csv(self, name_csv):

		# create dataframe from list of dicts
		df_profs = pd.DataFrame.from_records(self.link_entries)

		# write out dataframe to csv with filename = name_csv 
		df_profs.to_csv(name_csv)

	# when spider closed, activate function profdata_to_csv
	def spider_closed(self, spider):

		self.profdata_to_csv(self.curr_subj + "_linkData.csv")








	

