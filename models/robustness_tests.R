#bandwidth_sensitivity test, Function form test, temporal placebo test

library('RPostgreSQL')

## Loading required package: DBI

pg = dbDriver("PostgreSQL")

# Local Postgres.app database; no password by default
# Of course, you fill in your own database information here.
con = dbConnect(pg, user="postgres", password="fake",
                host="localhost", port=fakenum, dbname="gisdb")

# get part of the table
df_in = dbGetQuery(con, "select * from workzone.wzsens_output_full_table_xy;")
# summary(dtab)

library(data.table)
df_in = data.table(df_in)

#1. transform the data ----
# month dummies
for(monthi in c('01','02','03','04','05','06','07','08','09','10','11','12')){
  df_in[,paste('month_',monthi,sep='')]=0
  df_in[month==as.numeric(monthi),paste('month_',monthi,sep='')]=1
}
#year dummies
for(yeari in c(2013,2014,2015,2016,2017)){
  df_in[,paste('year_',yeari,sep='')]=0
  df_in[year==as.numeric(yeari),paste('year_',yeari,sep='')]=1
}
#nhs_ind_major
df_in[,nhs_ind_major:=0]
df_in[NHS_IND==2|NHS_IND==3|NHS_IND==4|NHS_IND==5|NHS_IND==6|NHS_IND==7|NHS_IND==8,nhs_ind_major:=1]
#new preciption
df_in[,avep_denull := avep]
df_in[is.na(avep),avep_denull:= 0]

names(df_in) = tolower(names(df_in))

#new variable
df_in$treatment_use=0
df_in[control==0,'treatment_use']<- 1
df_in$control_sq = df_in$control*df_in$control

df_in$control_negative = df_in$control
df_in[control>0,'control_negative'] = 0 

df_in$control_positive = df_in$control
df_in[control<0,'control_positive'] = 0 

#missing variable
df_in[is.na(crash_severe_61),'crash_severe_61'] =0 

df_in$speed_61_exists = 1
df_in[df_in$wzid_new %in% unique(df_in[is.na(df_in$real_speed_61)&df_in$location=='in',"wzid_new"])$wzid_new,'speed_61_exists']=0

#new speed variable
df_in$real_m_free_61 = df_in$real_speed_61-df_in$free_speed_61
df_in$real_m_limit_61 = df_in$real_speed_61-df_in$speed_limit

#missing weather data indicator
df_in$avet_exists=1

df_in[df_in$wzid_new %in% unique(df_in[is.na(df_in$avet)&df_in$location=='in',"wzid_new"])$wzid_new,'avet_exists']=0

# df_in[is.na(df_in$avet),'avet_exists'] = 0

df_in[is.na(df_in$avep)&df_in$avet_exists==1,'ave_p'] = 0
df_in[is.na(df_in$avew)&df_in$avet_exists==1,'avew'] = 0
#1: full closure
#0: not full closure
df_in[closure==1.0,closure_type:=1]
df_in[closure==0.5,closure_type:=0]
table(df_in$closure_type)
table(df_in$closure)

#lanecounts
df_in[,lanecounts_1:=as.numeric(lanecounts==1)]
#add log
df_in[,aadt_new_log:=log(1+aadt_new)]
df_in[,duration_log:=log(1+duration)]
df_in[,num_inters_log:=log(1+num_inters)]
df_in[,netlength_log:=log(1+netlength)]
df_in <- df_in[duration > 300  & netlength > 5 & netlength <= 20000 & closure ==0.5]

#2. create detreated speed for each bandwidth----
wzid_new_list <- readRDS(file = "./outputData/wzid_new_list.rds")

detreat_slope_intercept <- function(DT) { res <- DT[!is.na(real_speed_61), 
                                                    {
                                                      ux <- mean(treatment_use)
                                                      uy <- mean(real_speed_61)
                                                      slope <- sum((treatment_use - ux) * (real_speed_61 - uy)) / sum((treatment_use - ux) ^ 2)
                                                      list(slope=slope, intercept=uy - slope * ux)
                                                    }, by=wzid_new
                                                    ]
return(res)}

detreat_speed <- function(DT){
  DT_merge = DT
  for (bandwidth in 1:10){
    slope_intercept <- detreat_slope_intercept(DT[control >=-bandwidth & control <= bandwidth])
    setkey(slope_intercept, wzid_new);
    setkey(DT_merge, wzid_new);
    DT_merge <- merge(x=DT_merge, y=slope_intercept, by="wzid_new", all.x=TRUE,suffixes = c("",paste(".",as.character(bandwidth),sep="")))
    DT_merge[, paste('predicted_speed_',as.character(bandwidth),sep='') := slope*treatment_use+intercept]
    DT_merge[, paste('detreated_speed_',as.character(bandwidth),sep='') := real_speed_61 - get(paste('predicted_speed_',as.character(bandwidth),sep='')) ]    
  }
  
  # ori_speed = real_speed
  return(DT_merge)
  # merge
}


#note: run once, because := is reference update
df_in_ds <- detreat_speed(df_in[df_in$wzid_new %in%wzid_new_list])

#verify the correlation between speeds in df_in
# cor(df_in_ds[!is.na(detreated_speed_1),c("treatment_use","real_speed_61","predicted_speed","detreated_speed_1")])

#3. badnwidth sensitivity ----
library('tidyverse')
library('rms')
library('ggplot2')
library('ggpubr')
setwd('/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/scripts/R_code/workzone_r_2021')
source("./src/stratificationFunction.R")
library(stargazer)

ddist <- datadist(df_in_ds[wzid_new<100000000 & location=='in'])  # need both datadist and options
options(datadist='ddist')


regressions_bandwidth <- function( bandwidths = list(1,2,3,4,5,6,7,8,9,10)){
  fit_bandwidths <- list()
  for (band in bandwidths){
    fit_bandwidths<- append(fit_bandwidths,list(strati_regress( formula = paste('crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +speed_limit +   avew + avet + avep_denull  +detreated_speed_',as.character(band) ,'+month_02 +month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017',sep=""),data = df_in_ds[control >= -band & control <= band])))
  }
  stargazer(fit_bandwidths,
            column.labels=c("M = 1", "M = 2", "M = 3", "M = 4","M = 5",
                            "M = 6", "M = 7", "M = 8", "M = 9","M = 10"), model.numbers=TRUE,
            type='html',out="./tables2021/fit_bandwidths_full.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
            covariate.labels = c("Roadwork", 
                                 "Week",
                                 "Duration(s; log)",
                                 "Length (m; log)",
                                 "Weekday of week",
                                 "Daytime of day",
                                 "AADT (log)",
                                 "NHS major roads",
                                 "Number of interactions (log)",
                                 "Lane counts = 1",
                                 "Speed limit",
                                 "Average wind speed (mph)",
                                 "Average temperature (F)",
                                 "Average preciption (inch)",
                                 "Actual speed (mph)",
                                 # "Actual speed detreated 1 (A)(mph)",
                                 # "Actual speed detreated (mph)",
                                 #"Roadwork * Length (m; log)",
                                 #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                                 # "Roadwork * Duration(s; log)",
                                 # "Roadwork * Length (m; log)",
                                 # "Roadwork * Weekday of week",
                                 #"Roadwork * Daytime of day",
                                 # paste("sequence >=", as.character(i) ," hour",sep=''),
                                 # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                                 "Constant"),
            dep.var.caption  = "Work zones checking bandwidth",
            dep.var.labels   = "Crash occurrence",
            add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"),
                           c("Yearly Dummies", "Y","Y","Y","Y","Y","Y","Y","Y","Y","Y")
                           # c("bandwidths", "1","2","3","4","5","6","7","8","9","10")
                           #  c("work zone length control", "length <= 20,000",
                           #    "length <= 20,000",
                           #    "length <= 20,000",
                           #    "length <= 20,000",
                           #    "length <= 20,000"),
                           #  c("AADT control", " all ", "(0, 10,000]",
                           #    "(10,000, 20,000]",
                           #    "(20,000, ...)"
            ),
            align=TRUE,
            no.space=TRUE,
            single.row = TRUE)}
regressions_bandwidth(bandwidths=list(1,2,3,4,5,6,7,8,9,10))

d1 <- df_in_ds %>% 
  select(control,crash_61)%>%
  group_by(control) %>%
  summarise(prop := mean(crash_61),sd :=sd(crash_61),
            logodds:=log(mean(crash_61)/(1-mean(crash_61))),
            crash_counts:=sum(crash_61),
            logodds_sd := sqrt(1/sum(crash_61)+1/(n()-sum(crash_61)))) %>%
  select(control,prop,sd,logodds,logodds_sd,crash_counts) %>%
  ggplot(aes(x = control, y = logodds,label = crash_counts)) + 
  # geom_line()+
  geom_point()+
  # geom_text(hjust=0, vjust=2)+
  geom_errorbar(aes(ymin=logodds-logodds_sd, ymax=logodds+logodds_sd), width=.1)+
  # ggtitle("Work zones occurred in year 2015&2016&2017") +
  xlab("Week") + ylab("Average crash occurrence (log odds)")+
  geom_vline(xintercept=0, linetype="dashed", color = "red")+theme_minimal()
ggsave("./figs2021/crash_control_second.png",width = 20, height = 15, units = "cm")

#3. Function form sensitivity

compare_AIC <-
  function(bandwidths = list(1, 2, 3, 4, 5, 6)) {
    AICs = data.frame(Bandwith = numeric(length(bandwidths)), 
                      AIC_linear = numeric(length(bandwidths)),
                      AIC_quadaric =  numeric(length(bandwidths)),
                      AIC_delta = numeric(length(bandwidths)))
    
    for (bandwidth_i in 1:length(bandwidths)) {
      bandwidth <- bandwidths[[bandwidth_i]] 
      print(bandwidth)
      
      fit_model_1 <- strati_regress(formula = paste('crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +speed_limit +   avew + avet + avep_denull  +detreated_speed_',as.character(bandwidth) ,'+month_02 +month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017',sep=""),
                                    data = df_in_ds[ control <= bandwidth & control >= -bandwidth])
      fit_model_2 <- strati_regress(formula = paste('crash_61 ~ treatment_use + control + control_sq + duration_log + netlength_log + weekdayofweek +daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +speed_limit +   avew + avet + avep_denull  +detreated_speed_',as.character(bandwidth) ,'+month_02 +month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017',sep=""),
                                    data = df_in_ds[control <= bandwidth & control >= -bandwidth])
      
      # print(lrtest(fit_model_1, fit_model_2))
      # print(AIC(fit_model_1))
      # print(AIC(fit_model_2))
      AICs$Bandwith[bandwidth_i] <- bandwidth
      AICs$AIC_linear[bandwidth_i] <-  AIC(fit_model_1)
      AICs$AIC_quadaric[bandwidth_i] <-  AIC(fit_model_2)
    }
    AICs$AIC_delta <- AICs$AIC_linear-AICs$AIC_quadaric
    return (AICs)
  }

AICs_7_10 <- compare_AIC(bandwidths = list(7, 8, 9, 10))
print(htmlTable::htmlTable(htmlTable::txtRound(AICs_7_10,2,excl.cols=1),rnames=FALSE),type='html',file="./tables2021/AIC_7_10_detreated.html")

AICs_7_10 <- compare_AIC(bandwidths = list(2,3,4,5,6,7, 8, 9, 10))
print(htmlTable::htmlTable(htmlTable::txtRound(AICs_7_10,2,excl.cols=1),rnames=FALSE),type='html',file="./tables2021/AIC_2_10_newdata_detreated.html")

#4. temporal sensitivity test ----

detreat_slope_intercept_temporal <-
  function(DT, indicator = 'treatment_use_1before') {
    res <- DT[!is.na(real_speed_61),
              {
                ux <- mean(get(indicator))
                uy <-
                  mean(real_speed_61)
                slope <-
                  sum((get(indicator) - ux) * (real_speed_61 - uy)) / sum((get(indicator)  - ux) ^ 2)
                list(slope =
                       slope, intercept = uy - slope * ux)
              }, by =
                wzid_new]
    return(res)
  }


encode_temporal <- function(DT, names_l, treat_l) {
  #1. make new treatment variable to represent one week before and one week after the roadwork
  DT_merge <-
    DT[, 'treatment_use_1before' := as.numeric(control == -1)]
  DT_merge <-
    DT_merge[, 'treatment_use_1after' := as.numeric(control == 1)]
  
  
  #2. detreat process of actual observed speed
  for (treat_i in list(1, 2)) {
    treat <- treat_l[[treat_i]]
    name <- names_l[[treat_i]]
    
    slope_intercept <-
      detreat_slope_intercept_temporal(DT_merge[control >= treat - 6 &
                                                  control <= treat + 6], name)
    setkey(slope_intercept, wzid_new)
    
    setkey(DT_merge, wzid_new)
    
    DT_merge <-
      merge(
        x = DT_merge,
        y = slope_intercept,
        by = "wzid_new",
        all.x = TRUE,
        suffixes = c("", paste(".", as.character(name), sep = ""))
      )
    DT_merge[, paste('predicted_speed_', as.character(name), sep = '') := slope *
               treatment_use_1before + intercept]
    DT_merge[, paste('detreated_speed_', as.character(name), sep = '') := real_speed_61 - get(paste('predicted_speed_', as.character(name), sep =
                                                                                                      ''))]
  }
  return(DT_merge)
}

names_l <- list('treatment_use_1before', 'treatment_use_1after')
treat_l <- list(-1, 1)


df_temporal <- encode_temporal(df_in[df_in$wzid_new %in%wzid_new_list],names_l,treat_l)

regress_temporal <- function(DT = df_temporal, formula_base = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek + daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 + speed_limit +   avew + avet + avep_denull  +real_speed_61+month_02 + month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 + month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",names_l = names_l){
  #3. regression models for the placebo tests of temporal trends
  result_temporal <- list()
  for (name_i in names_l) {
    formula_i = gsub("treatment_use",name_i,formula_base)
    formula_i = gsub("real_speed_61",paste('detreated_speed_',as.character(name_i),sep=''),formula_i)
    # change the bandwidth of the DT as the same of placebo setting
    if (name_i == "treatment_use_1before") {
      DT_i = DT[control>= -1-6 & control <= -1+6]
    }else{
      DT_i = DT[control>= 1-6 & control <= 1+6]
    }
    
    result_temporal <- append(result_temporal,list(strati_regress( formula = formula_i ,
                                                                   data = DT_i)))
  }
  
  return (result_temporal)
}
result_temporal <- regress_temporal(DT = df_temporal, formula_base = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek + daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 + speed_limit +   avew + avet + avep_denull  +real_speed_61+month_02 + month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 + month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017", names_l = names_l)


stargazer(result_temporal,
          column.labels=c("One week before the roadwork", "One week after the roadwork"), model.numbers=TRUE,
          type='html',out="./tables2021/wzsens_temporal.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
          covariate.labels = c("Placebo: Roadwork - 1 week before",
                               "Placebo: Roadwork - 1 week after", 
                               "WeekN",
                               "Duration(s; log)",
                               "Length (m; log)",
                               "Weekday of week",
                               "Daytime of day",
                               "AADT (log)",
                               "NHS major roads",
                               "Number of interactions (log)",
                               "Lane counts = 1",
                               "Speed limit",
                               "Average wind speed (mph)",
                               "Average temperature (F)",
                               "Average preciption (inch)",
                               # "Actual speed (mph)",
                               # "Actual speed detreated 1 (A)(mph)",
                               "Actual speed detreated (mph) - 1 week before",
                               "Actual speed detreated (mph) - 1 week after",
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Temporal placebo",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y")
                         # c("Placebo week", "1 week before",
                           # "1 week after")
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000"),
                         #  c("AADT control", " all ", "(0, 10,000]",
                         #    "(10,000, 20,000]",
                         #    "(20,000, ...)"
          ),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)

#5. spatial placebo test ----
#delete all variables
rm(list = ls())
# Create a connection to the database
library('RPostgreSQL')

## Loading required package: DBI

pg = dbDriver("PostgreSQL")

# Local Postgres.app database; no password by default
# Of course, you fill in your own database information here.
#ssh -N -L fakeport:127.0.0.1:fakeport -i U:/id_rsa fakename@fakeip
con = dbConnect(pg, user="fakename", password="fakepassword",
                host="localhost", port=fakeport, dbname="gisdb")

# get part of the table
df_spa = dbGetQuery(con, "select * from workzone.wzspatial_output_full_table_v2;")
# summary(dtab)

library(data.table)
df_spa = data.table(df_spa)

###transform the data
# month dummies
for(monthi in c('01','02','03','04','05','06','07','08','09','10','11','12')){
  df_spa[,paste('month_',monthi,sep='')]=0
  df_spa[month==as.numeric(monthi),paste('month_',monthi,sep='')]=1
}
#year dummies
for(yeari in c(2013,2014,2015,2016,2017)){
  df_spa[,paste('year_',yeari,sep='')]=0
  df_spa[year==as.numeric(yeari),paste('year_',yeari,sep='')]=1
}

names(df_spa) = tolower(names(df_spa))

#nhs_ind_major
df_spa[,nhs_ind_major:=0]
df_spa[ nhs_ind==2| nhs_ind==3| nhs_ind==4| nhs_ind==5| nhs_ind==6| nhs_ind==7| nhs_ind==8,nhs_ind_major:=1]
#new preciption
df_spa[,avep_denull := avep]
df_spa[is.na(avep),avep_denull:= 0]


#new variable
df_spa$treatment_use=0
df_spa[control==0,'treatment_use']<- 1
# df_spa$control_sq = df_spa$control*df_spa$control
# 
# df_spa$control_negative = df_spa$control
# df_spa[control>0,'control_negative'] = 0 
# 
# df_spa$control_positive = df_spa$control
# df_spa[control<0,'control_positive'] = 0 

#missing variable
# df_spa[is.na(crash_severe_61),'crash_severe_61'] =0 

df_spa$speed_61_exists = 1
df_spa[df_spa$wzid_new %in% unique(df_spa[is.na(df_spa$real_speed_61)&df_spa$location=='in',"wzid_new"])$wzid_new,'speed_61_exists']=0

#new speed variable
# df_spa$real_m_free_61 = df_spa$real_speed_61-df_spa$free_speed_61
# df_spa$real_m_limit_61 = df_spa$real_speed_61-df_spa$speed_limit

#missing weather data indicator
df_spa$avet_exists=1

df_spa[df_spa$wzid_new %in% unique(df_spa[is.na(df_spa$avet)&df_spa$location=='in',"wzid_new"])$wzid_new,'avet_exists']=0

# df_spa[is.na(df_spa$avet),'avet_exists'] = 0

# df_spa[is.na(df_spa$avep)&df_spa$avet_exists==1,'ave_p'] = 0
df_spa[is.na(df_spa$avew)&df_spa$avet_exists==1,'avew'] = 0
#1: full closure
#0: not full closure
df_spa[closure==1.0,closure_type:=1]
df_spa[closure==0.5,closure_type:=0]
table(df_spa$closure_type)
table(df_spa$closure)

#lanecounts
df_spa[,lanecounts_1:=as.numeric(lanecounts==1)]
#add log
df_spa[,aadt_new_log:=log(1+aadt_new)]
df_spa[,duration_log:=log(1+duration)]
df_spa[,num_inters_log:=log(1+num_inters)]
df_spa[,netlength_log:=log(1+netlength)]
df_spa <- df_spa[duration > 300  & netlength > 5 & netlength <= 20000 & closure ==0.5]

#2. create detreated speed for each bandwidth
wzid_new_list <- readRDS(file = "./outputData/wzid_new_list.rds")

library('tidyverse')
library('rms')
library('ggplot2')
library('ggpubr')
setwd('/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/scripts/R_code/workzone_r_2021')
source("./src/stratificationFunction.R")
library('stargazer')




# 1. detreated speed

#2. run regression
detreat_slope_intercept <- function(DT) { res <- DT[!is.na(real_speed_61), 
                                                    {
                                                      ux <- mean(treatment_use)
                                                      uy <- mean(real_speed_61)
                                                      slope <- sum((treatment_use - ux) * (real_speed_61 - uy)) / sum((treatment_use - ux) ^ 2)
                                                      list(slope=slope, intercept=uy - slope * ux)
                                                    }, by=wzid_new
                                                    ]
return(res)}

detreat_speed <- function(DT){
  DT_merge = DT
  slope_intercept <- detreat_slope_intercept(DT)
  setkey(slope_intercept, wzid_new);
  setkey(DT_merge, wzid_new);
  DT_merge <- merge(x=DT_merge, y=slope_intercept, by="wzid_new", all.x=TRUE)
  DT_merge[, 'predicted_speed' := slope*treatment_use+intercept]
  DT_merge[, 'detreated_speed' := real_speed_61 - get('predicted_speed') ]    
  
  
  # ori_speed = real_speed
  return(DT_merge)
  # merge
}

df_spa_ds <- detreat_speed(df_spa[control<=6 & control >=-6])

ddist <- datadist(df_spa_ds)  # need both datadist and options
options(datadist='ddist')

regress_spatial <- function(DT = df_spa_ds, formula_base = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek + daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 + speed_limit +   avew + avet + avep_denull  +detreated_speed+month_02 + month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 + month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"){
  result_spatial <- list()
  result_spatial <- append(result_spatial,list(strati_regress( formula = formula_base ,
                                                               data = DT)))
  
  
  return (result_spatial)
}
result_spatial <- regress_spatial(DT = df_spa_ds,formula_base = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek + daytimeofday +   aadt_new_log + num_inters_log + lanecounts_1 + speed_limit +   avew + avet + avep_denull  +detreated_speed+month_02 + month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 + month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017")


stargazer(result_spatial,
          model.numbers=FALSE,
          type='html',out="./tables2021/wzsens_spatial.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
          covariate.labels = c("Roadwork",
                               "WeekN",
                               "Duration(s; log)",
                               "Length (m; log)",
                               "Weekday of week",
                               "Daytime of day",
                               "AADT (log)",
                               # "NHS major roads",
                               "Number of interactions (log)",
                               "Lane counts = 1",
                               "Speed limit",
                               "Average wind speed (mph)",
                               "Average temperature (F)",
                               "Average preciption (inch)",
                               # "Actual speed (mph)",
                               # "Actual speed detreated 1 (A)(mph)",
                               "Actual speed detreated (mph)",
                               # "Actual speed detreated (mph) - 1 week after",
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Spatial placebo",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y")
                         # c("Placebo week", "1 week before",
                         # "1 week after")
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000"),
                         #  c("AADT control", " all ", "(0, 10,000]",
                         #    "(10,000, 20,000]",
                         #    "(20,000, ...)"
          ),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)
