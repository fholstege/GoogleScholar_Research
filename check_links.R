links = read.csv(
  '~/Documents/oxford/PythonforSDS/GoogleScholar_Research/gscholar/files/master_links_GoogleScholar.csv', 
                 stringsAsFactors = F, 
                 header = F
  )

length(links$V2)
length(unique(links$V2))

length(links$V2) - length(unique(links$V2))