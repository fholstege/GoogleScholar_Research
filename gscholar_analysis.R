library(dplyr)
library(stargazer)


# 1 = Physics
# 2 = Economics
# 3 = Philosophy
gscholar = read.csv(
  '~/Documents/oxford/PythonforSDS/GoogleScholar_Research/gscholar_complete_v2.csv',
  na.strings=c("","NA")
)

gscholar_sum = gscholar %>% filter(gender_prob > 0.9 & count_name > 10) %>% 
  select(h.index,h5.index,n.citations,field,gender,wiki_bool) %>% 
  distinct() %>% mutate(field = as.factor(field)) %>% 
  filter(complete.cases(.))
stargazer(gscholar_sum)

hist(gscholar_sum$h.index)

gscholar_fit1 = glm(data = gscholar_sum, formula = wiki_bool ~ gender + log(h.index), family = binomial(link = "logit"))

gscholar_fit2 = glm(data = gscholar_sum, formula = wiki_bool ~ gender + log(h.index) + factor(field), family = binomial(link = "logit"))

gscholar_fit3 = glm(data = gscholar_sum, formula = wiki_bool ~ gender * log(h.index), family = binomial(link = "logit"))

gscholar_fit3b = glm(data = gscholar_sum, formula = wiki_bool ~ gender * log(h.index) + factor(field), family = binomial(link = "logit"))

# Per field robustness
gscholar_fit4 = glm(data = gscholar_sum %>% filter(field == 1), formula = wiki_bool ~ gender + log(h.index), family = binomial(link = "logit"))
summary(gscholar_fit4)

gscholar_fit5 = glm(data = gscholar_sum %>% filter(field == 2), formula = wiki_bool ~ gender + log(h.index), family = binomial(link = "logit"))
summary(gscholar_fit5)

gscholar_fit6 = glm(data = gscholar_sum %>% filter(field == 3), formula = wiki_bool ~ gender + log(h.index), family = binomial(link = "logit"))
summary(gscholar_fit6)

# h.index robustness checks
gscholar_fit7 = glm(data = gscholar_sum, formula = wiki_bool ~ gender + log(h5.index + 0.1), family = binomial(link = "logit"))
summary(gscholar_fit)

gscholar_fit8 = glm(data = gscholar_sum, formula = wiki_bool ~ gender + log(n.citations + 0.1), family = binomial(link = "logit"))
summary(gscholar_fit)

mean(gscholar_sum$h.index)

predict(gscholar_fit3b, newdata = data.frame('gender' = 'male','h.index' = 24.22, field = 3), type = 'response')

stargazer(gscholar_fit1, gscholar_fit2, gscholar_fit3b )


summary(gscholar$wiki_bool)

gscholar %>% group_by(gender) %>% summarise(wikis = sum(wiki_bool == 'True', na.rm = T))

gscholar %>% na.omit() %>% group_by(field) %>% summarise(h_index_mean = mean(h.index, na.rm = T),
                                                                     h_index_median = median(h.index, na.rm = T),
                                                                     count = n(),
                                                                     perc = n() / nrow(.))



library(xtable)
xtable(
  gscholar_sum %>% group_by(field, gender ) %>% summarise(total = n(), withWikipedia = (sum(wiki_bool == 'True', na.rm = T) / n()) * 100, withoutWikipedia = (sum(wiki_bool == 'False', na.rm = T) / n() ) * 100)
  )

gscholar_fit = lm(data = gscholar[gscholar$wiki_bool == 'True',], formula = wiki_length ~ gender + factor(field))
summary(gscholar_fit)

female_h_indexes = gscholar$h_index[gscholar$gender == 'female']
male_h_indexes = gscholar$h_index[gscholar$gender == 'male']

hist(female_h_indexes)
hist(male_h_indexes)

t.test(x = female_h_indexes, y = male_h_indexes)
                                                                     