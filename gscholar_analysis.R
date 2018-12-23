gscholar = read.csv(
  '~/Documents/oxford/PythonforSDS/GoogleScholar_Research/gscholar_complete.csv',
  na.strings=c("","NA")
)

gscholar_fit = glm(data = gscholar, formula = wiki_bool ~ gender + n.citations, family = binomial(link = "logit"))
summary(gscholar_fit)

ggplot(gscholar[complete.cases(gscholar),], aes(x = wiki_bool, y = h_index)) + geom_violin()


ggplot(gscholar[complete.cases(gscholar),], aes(x = gender, y = h_index)) + geom_boxplot() + geom_point(aes(shape = wiki_bool, color = wiki_bool, alpha = wiki_bool))



gscholar_fit = glm(data = gscholar %>% filter(field == 1), formula = wiki_bool ~ gender + h_index, family = binomial(link = "logit"))
summary(gscholar_fit)




gscholar_fit = glm(data = gscholar %>% filter(field == 2), formula = wiki_bool ~ gender + h_index, family = binomial(link = "logit"))
summary(gscholar_fit)


gscholar_fit = glm(data = gscholar %>% filter(field == 3), formula = wiki_bool ~ gender + h_index, family = binomial(link = "logit"))
summary(gscholar_fit)

summary(gscholar$wiki_bool)

gscholar %>% group_by(gender) %>% summarise(wikis = sum(wiki_bool == 'True', na.rm = T))

gscholar %>% na.omit() %>% group_by(wiki_bool, gender) %>% summarise(h_index_mean = mean(h_index, na.rm = T),
                                                                     h_index_median = median(h_index, na.rm = T),
                                                                     count = n(),
                                                                     perc = n() / nrow(.))





gscholar_fit = lm(data = gscholar[gscholar$wiki_bool == 'True',], formula = wiki_length ~ gender + factor(field))
summary(gscholar_fit)


female_h_indexes = gscholar$h_index[gscholar$gender == 'female']
male_h_indexes = gscholar$h_index[gscholar$gender == 'male']

hist(female_h_indexes)
hist(male_h_indexes)

436 / (2720 + 436)
1689 / (1689 + 10388)

t.test(x = female_h_indexes, y = male_h_indexes)
                                                                     