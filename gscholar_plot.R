library(reshape2)
library(ggplot2)

# Average field 1 = 34
# Average field 2 = 19
# AVerage field 3 = 10

predict_prob_wiki = function(input_h_index, input_gender) {

return(predict(gscholar_fit3b, newdata = data.frame('gender' = input_gender,'h.index' = input_h_index, field = 2), 
               type = 'response'))
  
}
female_prob = sapply(X = 1:50, FUN = predict_prob_wiki, input_gender = 'female')

male_prob = sapply(X = 1:50, FUN = predict_prob_wiki, input_gender = 'male')

for(i in c(34,19,10)) {
print( female_prob[i] / male_prob[i] )
}

gender_probs = as.data.frame(cbind(1:50, female_prob, male_prob))

gender_probs_melt = melt(gender_probs, measure.vars = c('female_prob','male_prob'))

ggplot(gender_probs_melt, aes(x = V1, y = value, group = variable, color = variable)) + geom_line(size = 2) + theme_bw() + xlab('h-index') + scale_color_brewer(palette="Accent") + ylab('Probability of Wikipedia Page') +
  theme(legend.position="bottom")

ggsave(filename = 'wikipediaprob-philo.pdf', device = 'pdf', width = 6, height = 5)
