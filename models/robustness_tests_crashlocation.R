#robustness test: crash location
#0. import libraries ----
library('tidyverse')
library('rms')
library('ggplot2')
library('ggpubr')
setwd(
  '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/scripts/R_code/workzone_r_2021'
)
source("./src/stratificationFunction.R")
load('detreated_speed.RData')
library('stargazer')
library('data.table')


#1. obtain detreated speed on these periods -----

detreat_slope_intercept <- function(DT) { res <- DT[!is.na(real_speed_61), 
                                                    {
                                                      ux <- mean(treatment_use)
                                                      uy <- mean(real_speed_61)
                                                      slope <- sum((treatment_use - ux) * (real_speed_61 - uy)) / sum((treatment_use - ux) ^ 2)
                                                      list(slope=slope, intercept=uy - slope * ux)
                                                    }, by=wzid_new
                                                    ]
return(res)}

detreat_slope_intercept_518 <- function(DT) { res <- DT[!is.na(real_speed_518), 
                                                        {
                                                          ux <- mean(treatment_use)
                                                          uy <- mean(real_speed_518)
                                                          slope <- sum((treatment_use - ux) * (real_speed_518 - uy)) / sum((treatment_use - ux) ^ 2)
                                                          list(slope=slope, intercept=uy - slope * ux)
                                                        }, by=wzid_new
                                                        ]
return(res)}

detreat_speed <- function(DT){
  DT_merge = DT
  for (location_i in list('up','down','bi_in')){
    slope_intercept <- detreat_slope_intercept(DT[location == location_i])
    setkey(slope_intercept, wzid_new);
    setkey(DT_merge, wzid_new);
    DT_merge <- merge(x=DT_merge, y=slope_intercept, by="wzid_new", all.x=TRUE,suffixes = c("",paste(".",as.character(location_i),"_61",sep="")))
    DT_merge[, paste('predicted_speed_',as.character(location_i),"_61",sep='') := slope*treatment_use+intercept]
    DT_merge[, paste('detreated_speed_',as.character(location_i),"_61",sep='') := real_speed_61 - get(paste('predicted_speed_',as.character(location_i),"_61",sep='')) ]    
  }
  
  for (location_i in list('up','down','bi_in')){
    slope_intercept <- detreat_slope_intercept_518(DT[location == location_i])
    setkey(slope_intercept, wzid_new);
    setkey(DT_merge, wzid_new);
    DT_merge <- merge(x=DT_merge, y=slope_intercept, by="wzid_new", all.x=TRUE,suffixes = c("",paste(".",as.character(location_i),"_518",sep="")))
    DT_merge[, paste('predicted_speed_',as.character(location_i),"_518",sep='') := slope*treatment_use+intercept]
    DT_merge[, paste('detreated_speed_',as.character(location_i),"_518",sep='') := real_speed_61 - get(paste('predicted_speed_',as.character(location_i),"_518",sep='')) ]    
  }
  
  
  # ori_speed = real_speed
  return(DT_merge)
  # merge
}

#2. modify data sets ----
#select non-full closed work zones
df <- df[wzid_new < 100000000 &
           avet_exists == 1 &
           speed_61_exists == 1 &
           duration > 300  &
           netlength > 5 & netlength <= 20000 & closure == 0.5]

df_ds <- detreat_speed(df)

#3. run regresions ----
formula_base <- "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_location <- list()

for (location_i in list('up','down')) {
  formula_i = gsub("real_speed_61_detreat_ind",paste("detreated_speed_",as.character(location_i),"_61",sep=""),formula_base)
  results_location <- append(results_location,list(strati_regress( formula = formula_i,
                                                                   data = df_ds[wzid_new < 100000000 &location == location_i & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & up_exists ==1])))
  
  formula_i = gsub("real_speed_61_detreat_ind",paste("detreated_speed_",as.character(location_i),"_518",sep=""),formula_base)
  formula_i = gsub("crash_61","crash_518",formula_i)
  
  results_location <- append(results_location,list(strati_regress( formula = formula_i,
                                                                   data = df_ds[wzid_new < 100000000 &location == location_i & avet_exists == 1 & speed_518_exists ==1 & duration > 0& netlength > 0 & netlength<=20000  & up_exists ==1])))
  
  
}


stargazer(results_location,
          column.labels = c(
            "upstream 61 meters",
            "upstream 518 meters",
            "downstream 61 meters",
            "downstream 518 meters"
          ),
          model.numbers = TRUE,
          type='html',out="./tables2021/wzsens_crashlocation.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
          covariate.labels = c("Roadwork", 
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
                               "Average precipitation (inch)",
                               # "Actual speed (mph)",
                               # "Actual speed detreated 1 (A)(mph)",
                               "Actual speed detreated (mph) - up 61m",
                               "Actual speed detreated (mph) - up 518m",
                               "Actual speed detreated (mph) - down 61m",
                               "Actual speed detreated (mph) - down 518m",
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Relative location of work zone",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y")
                         #  c("work zone length control", "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000"),
                         # c("Crash location", "up ", "up",
                         #   "down",
                         #   "down")
          ),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)

for (location_i in list('bi_in')) {
  formula_i = gsub("real_speed_61_detreat_ind",paste("detreated_speed_",as.character(location_i),"_61",sep=""),formula_base)
  formula_i  = gsub("+ nhs_ind_major","",formula_i)
  results_location <- append(results_location,list(strati_regress( formula = formula_i,
                                                                   data = df_ds[wzid_new < 100000000 &location == location_i & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & up_exists ==1])))
  
  formula_i = gsub("real_speed_61_detreat_ind",paste("detreated_speed_",as.character(location_i),"_518",sep=""),formula_base)
  formula_i = gsub("crash_61","crash_518",formula_i)
  formula_i  = gsub("+ nhs_ind_major","",formula_i)
  results_location <- append(results_location,list(strati_regress( formula = formula_i,
                                                                   data = df_ds[wzid_new < 100000000 &location == location_i & avet_exists == 1 & speed_518_exists ==1 & duration > 0& netlength > 0 & netlength<=20000  & up_exists ==1])))
  
  
}

stargazer(results_location[5],results_location[6],
          type='html',out="./tables2021/wzsens_crashlocation_biin.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
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
                               "Actual speed detreated (mph) - bi-in 61m",
                               "Actual speed detreated (mph) - bi-in 518m",
                               # "Actual speed detreated (mph) - down 61m",
                               # "Actual speed detreated (mph) - down 518m",
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Bi-in",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y")
                         #  c("work zone length control", "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000"),
          ),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)

