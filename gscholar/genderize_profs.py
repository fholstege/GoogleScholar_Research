from genderize import Genderize
import pandas as pd
from nameparser import HumanName

colnames = ["index", "H_index", "H_index_5", "I_index","I_index_5","prof_insti","prof_name", "prof_url", "tot_citations", "tot_citations_5" ]
profdata = pd.read_csv('files/profData_physicsLinks.csv', sep=';', names=colnames, encoding = "ISO-8859-1")

profdata_cleaned = profdata.drop_duplicates(subset='prof_name')

names_profs = profdata_cleaned['prof_name']
ls_names_profs = names_profs.tolist()

name_batch = []

for name in ls_names_profs:

	name_distilled = HumanName(name)

	firstname = name_distilled.first

	name_batch.append(firstname)

	if len(name_batch) == 10:

		result_batch = Genderize().get(name_batch)

		name_batch = []

		for result in result_batch:
			
			with open('results_genderize_physicsLinks.csv', 'wb') as csv_file:
				writer = csv.writer(csv_file)
				writer.writerow(result)



