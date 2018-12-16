"""
spider class that extract information of profile page on google scholar
"""


# import relevant libraries
import scrapy
import re
import html2text
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import CloseSpider
import csv
import sys
import pandas as pd
import time


class profspider(scrapy.Spider):
    name = 'profspider'

    def __init__(self, links):

        self.start_urls = links

        self.prof_entries = []

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

        print("Currently adding to the list: ", entry)

        # add entry to list of dicts with all entries
        self.prof_entries.append(entry)

    # when spider closed, activate function profdata_to_csv
    def spider_closed(self, spider):

        # create dataframe from list of dicts
        df_prof = pd.DataFrame.from_records(self.prof_entries)

        print(df_prof.head(30))

        with open('files/profData_physicsLinks.csv', 'a') as current_link_file:
            df_prof.to_csv(current_link_file, header=False)

        self.prof_entries = []

