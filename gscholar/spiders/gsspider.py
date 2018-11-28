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
import csv

# create spider class
class gsspider_class(scrapy.Spider):
	
	# name spider
	name = "gscholar"

	def __init__(self, subject, N_request, new_instance):
		"""
		when spider class is initialized, define the paramters
		"""

		# define label sought after, and base link for searched
		self.curr_subj = subject
		self.link_base = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
		
		# number of current professors, and maximum number of professors
		self.curr_N_prof = 10
		self.max_prof = N_request

		# placeholder for dataframe with professor data
		self.link_entries = []
		self.current_page = ""

		# acquire signal when spider is closed
		dispatcher.connect(self.spider_closed, signals.spider_closed)

		# placeholder for start url
		base_url = ""

		# check if new instance (no links in master file)
		if new_instance == True:
			base_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3A" + self.curr_subj + "&btnG="
		else:
			# load the csv where the current link is saved
			with open('gscholar/files/current_link_GoogleScholar.csv', "r") as f:
				reader = csv.reader(f)

				for row in reader:
					base_url = row

		self.start_urls = base_url


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

		# select the next page
		next_page_select = 'button[aria-label="Next"]::attr(onclick)'
		next_page = response.css(next_page_select).extract_first()


		# if there is a next page, and the max of professors searched has not been reached, go to next page
		if next_page and self.curr_N_prof < self.max_prof:

			print("CURRENT N PROF: ", self.curr_N_prof, "MAX PROF: ", self.max_prof)

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

			self.current_page = nextpage_link

	    	# send scrapy to next link, with callback to parse method 
			yield scrapy.Request(nextpage_link, callback=self.parse, dont_filter=True)

	# when spider closed, activate function profdata_to_csv
	def spider_closed(self, spider):

		# current df with all the profs gathered this session
		df_profs = pd.DataFrame({"links": self.link_entries})
		# write out all the gathered links to the master file 
		master_link_file = 'gscholar/files/master_links_GoogleScholar.csv'
		df_profs.to_csv(master_link_file, header=False, mode = 'a')

		#write out last link to the other file
		with open('gscholar/files/current_link_GoogleScholar.csv', 'w') as current_link_file:
			 writer = csv.writer(current_link_file)
			 writer.writerow([self.current_page])



