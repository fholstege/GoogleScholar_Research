from genderize import Genderize
import pandas as pd
from nameparser import HumanName

# read csv with names of the profs
profdata = pd.read_csv('files/profData_physics_economics_philo.csv')

# get the names of profs
names_profs = profdata['name']

# create list of all the names of profs
ls_names_profs = names_profs.tolist()

# placeholder: here we store names per batch sent to genderize.io
name_batch = []

# create two columns that are filled with None
# if no gender, value remains "None"
profdata['gender'] = None
profdata["gender_prob"] = None

count_prof = 0

# go through ALL the names
# probs you want to do a smaller amount
for name in ls_names_profs[0:20]:

	# parse the name with all its aspect
	# this DOES take into account if the name is spelled as follows: Holstege, Floris
	name_distilled = HumanName(name)

	# get attribute firstname 
	firstname = name_distilled.first

	# create a list of first names as a batch
	name_batch.append(firstname)

	# genderize.io only allows 10 per time
	if len(name_batch) == 10:

		# get the results for the batch of names
		result_batch = Genderize().get(name_batch)

		# clear batch to help with memory
		name_batch = []

		# go through all results in the batch 
		for result in result_batch:

			# the gender of the professor
			gender_prof = result["gender"]

			# if no gender found, continue to next result
			if gender_prof == None:
				continue

			# the probability that the gender is correct
			probability_gender_prof =result["probability"]

			# put gender and probability at the right index in the dataframe
			profdata.loc[count_prof,'gender'] = gender_prof
			profdata.loc[count_prof,'gender_prob'] = probability_gender_prof

			# add to counter
			count_prof = count_prof + 1


print(profdata.head(5))

			
