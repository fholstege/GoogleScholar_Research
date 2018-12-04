install.packages("genderizeR")
library(genderizeR)

getwd()

profdata = read.csv("profData_physicsLinks.csv", sep = ";", header = FALSE)
names(profdata) <- c("index", "H_index", "H_index_5", "I_index","I_index_5","prof_insti","prof_name", "prof_url", "tot_citations", "tot_citations_5")

profdata$prof_name[1]


findGivenNames("Hongjie Dai, NR", progress = FALSE)
