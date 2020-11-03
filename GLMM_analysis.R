library(lme4)


mydata <- read.csv("FullData_0805_NEW.csv", header = TRUE)

df <- data.frame(mydata)

### TO DO THE STATISTICS SEPRATELY FOR SPECIFIC GENERATIONS, USE THIS CODE
df_clean= df[df$Gen_cat %in% c(0,1,2,3,4,5),]
gmm <- glmer(GFP_cat ~ Gen_cat*Treatment + (1 |Rep),
                       data = df_clean, family = binomial(link = "logit"))  
summary(gmm)
drop1(gmm,scope=c("Treatment"),test="Chisq")
####


## TO DO THE STATISTICS FOR ALL GENERATIONS, USE THIS CODE
gmm <- glmer(GFP_cat ~ Gen_cat*Treatment +(1|Rep),
                       data = df, family = binomial(link = "logit"))
             #control=glmerControl(optimizer="bobyqa",optCtrl=list(maxfun=2e5)))  
summary(gmm)
drop1(gmm,scope=c("Treatment"),test="Chisq")
###





