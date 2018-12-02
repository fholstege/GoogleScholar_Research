start_urls = []

# open csv, and add each line as a start url 
file = open('files/master_links_GoogleScholar.csv', 'r')

for row in file:
	formatted = row.split('\n')

	split_row = formatted[0].split(',')
	url = split_row[1]
	start_urls.append(url.strip())


print(start_urls)