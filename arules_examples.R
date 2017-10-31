# EXAMPLES WITH 'ARULES' PACKAGE

library(arules)
library(titanic)
library(dplyr)

# load data ----
df <- titanic::titanic_train

# preprocess
df2 <-
  df %>%   
  select(Survived, Pclass, Sex, Embarked, SibSp, Age) %>%
  mutate(SibSp = as.numeric(SibSp))

# discretize age
cuts_age <- discretize(df2$Age, method = "cluster", categories = 4, 
                       onlycuts = T)
df2$Age <- cut(x = df2$Age, breaks = cuts_age, right = F)
# discretize siblings
cuts_sibsp <- discretize(df2$SibSp, method = "frequency", categories = 4, 
                         onlycuts = T)
df2$SibSp <- cut(x = df2$SibSp, breaks = cuts_sibsp, right = F)
# all columns to factors
df2 <- 
  df2 %>%
  mutate_all(funs(factor(.)))

# apriori
rules <- apriori(df2, 
                parameter = list(supp = 0.05, 
                                 conf = 0.9, 
                                 target = "rules",
                                 maxlen = 3))
inspect(sort(rules, by = 'confidence'))

