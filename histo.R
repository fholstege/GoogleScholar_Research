#2) for the appendix, could you plot the histogram of h, citation, and h5 for all the scholars in your data for the fields and gender separately (6 diagrams). 
#And then could you plot the same only for those you found on Wikipedia?
  
library(ggplot2)
ggplot(gscholar_sum, aes(x = n.citations)) + geom_histogram() + theme_bw() + facet_grid(rows = vars(gender), cols = vars(field))

ggsave(filename = 'histograms-citations.pdf', device = 'pdf', width = 10, height = 5)
