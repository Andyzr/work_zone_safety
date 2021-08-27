#sensitivity test

#1. read data ----
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

#select non-full closed work zones
df <- df[wzid_new < 100000000 &
     location == 'in' &
     avet_exists == 1 &
     speed_61_exists == 1 &
     duration > 300  &
     netlength > 5 & netlength <= 20000 & closure == 0.5]

#2. aadt sensitivity test ----
formula_base <-
  "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_aadt <- list()

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000]))) #(eq(1))


results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000])))#(eq(2-6))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=8000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=9000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=11000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=12000])))


results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000])))#(eq(7-15))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>8000 & aadt_new<=20000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>9000 & aadt_new<=20000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>11000 & aadt_new<=20000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>12000 & aadt_new<=20000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=18000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=19000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=21000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = formula_base,
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=22000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
                                                         daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
                                                         speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                         month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                         month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000])))#(eq(16-20))


results_aadt <- append(results_aadt,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
                                                         daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
                                                         speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                         month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                         month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>18000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
                                                         daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
                                                         speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                         month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                         month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>19000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
                                                         daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
                                                         speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                         month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                         month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>21000])))

results_aadt <- append(results_aadt,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
                                                         daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
                                                         speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                         month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                         month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
                                                         data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>22000])))


stargazer(results_aadt,
          type='html',out="./tables2021/wzaadt_allsens.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
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
                               "Average preciption (inch)",
                               # "Actual speed (mph)",
                               # "Actual speed detreated 1 (A)(mph)",
                               "Actual speed detreated (mph)",
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Table",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y"),
                         #  c("work zone length control", "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000"),
                         c("AADT control", " all ", "(0, 10,000]",
                           "(10,000, 20,000]",
                           "(20,000, ...)")),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)

#3. work zone length sensitivity test---------

formula_base <- "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_aadt_length <- list()

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=3000])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=3000])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=3000])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
                                                                       speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                                       month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                                       month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=3000])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 3000])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 3000 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >3000])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >3000])))

#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=2900])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 2900 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >2900])))
#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=2800])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=2800])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=2800])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=2800])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 2800])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 2800 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >2800])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >2800])))

#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=2700])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=2700])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=2700])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=2700])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 2700])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 2700 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >2700])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >2700])))

#next sens

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=2600])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=2600])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=2600])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=2600])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 2600])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 2600 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >2600])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >2600])))

#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=3100])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=3100])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=3100])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=3100])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 3100])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 3100 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >3100])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >3100])))

#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=3200])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=3200])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=3200])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=3200])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 3200])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 3200 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >3200])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >3200])))

#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=3300])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=3300])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=3300])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=3300])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 3300])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 3300 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >3300])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >3300])))

#next sens


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength <=2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength <=2900])))


results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength <=2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength <=2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & netlength > 2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & netlength > 2900 ])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & netlength >2900])))

results_aadt_length <- append(results_aadt_length,list(strati_regress( formula = formula_base,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000 & netlength >2900])))

stargazer(results_aadt_length,
          column.labels = c(
            "AADT = all <br> length <= 3000 m",
            "0 < AADT <= 10,000 <br> length <= 3000 m",
            "10,000 < AADT <= 20,000 <br> length <= 3000 m",
            "AADT > 20,000 <br> length <= 3000 m",
            "AADT = all <br> length > 3000 m",
            "0 < AADT <= 10,000 <br> length > 3000 m",
            "10,000 < AADT <= 20,000 <br> length > 3000 m",
            "AADT > 20,000 <br> length > 3000 m",
            "AADT = all <br> length <= 2900 m",
            "0 < AADT <= 10,000 <br> length <= 2900 m",
            "10,000 < AADT <= 20,000 <br> length <= 2900 m",
            "AADT > 20,000 <br> length <= 2900 m",
            "AADT = all <br> length > 2900 m",
            "0 < AADT <= 10,000 <br> length > 2900 m",
            "10,000 < AADT <= 20,000 <br> length > 2900 m",
            "AADT > 20,000 <br> length > 2900 m",
            "AADT = all <br> length <= 2800 m",
            "0 < AADT <= 10,000 <br> length <= 2800 m",
            "10,000 < AADT <= 20,000 <br> length <= 2800 m",
            "AADT > 20,000 <br> length <= 2800 m",
            "AADT = all <br> length > 2800 m",
            "0 < AADT <= 10,000 <br> length > 2800 m",
            "10,000 < AADT <= 20,000 <br> length > 2800 m",
            "AADT > 20,000 <br> length > 2800 m",
            "AADT = all <br> length <= 2700 m",
            "0 < AADT <= 10,000 <br> length <= 2700 m",
            "10,000 < AADT <= 20,000 <br> length <= 2700 m",
            "AADT > 20,000 <br> length <= 2700 m",
            "AADT = all <br> length > 2700 m",
            "0 < AADT <= 10,000 <br> length > 2700 m",
            "10,000 < AADT <= 20,000 <br> length > 2700 m",
            "AADT > 20,000 <br> length > 2700 m",
            "AADT = all <br> length <= 2600 m",
            "0 < AADT <= 10,000 <br> length <= 2600 m",
            "10,000 < AADT <= 20,000 <br> length <= 2600 m",
            "AADT > 20,000 <br> length <= 2600 m",
            "AADT = all <br> length > 2600 m",
            "0 < AADT <= 10,000 <br> length > 2600 m",
            "10,000 < AADT <= 20,000 <br> length > 2600 m",
            "AADT > 20,000 <br> length > 2600 m",
            "AADT = all <br> length <= 3100 m",
            "0 < AADT <= 10,000 <br> length <= 3100 m",
            "10,000 < AADT <= 20,000 <br> length <= 3100 m",
            "AADT > 20,000 <br> length <= 3100 m",
            "AADT = all <br> length > 3100 m",
            "0 < AADT <= 10,000 <br> length > 3100 m",
            "10,000 < AADT <= 20,000 <br> length > 3100 m",
            "AADT > 20,000 <br> length > 3100 m",
            "AADT = all <br> length <= 3200 m",
            "0 < AADT <= 10,000 <br> length <= 3200 m",
            "10,000 < AADT <= 20,000 <br> length <= 3200 m",
            "AADT > 20,000 <br> length <= 3200 m",
            "AADT = all <br> length > 3200 m",
            "0 < AADT <= 10,000 <br> length> 3200 m",
            "10,000 < AADT <= 20,000 <br> length > 3200 m",
            "AADT > 20,000 <br> length > 3200 m",
            "AADT = all <br> length <= 3300 m",
            "0 < AADT <= 10,000 <br> length <= 3300 m",
            "10,000 < AADT <= 20,000 <br> length <= 3300 m",
            "AADT > 20,000 <br> length <= 3300 m",
            "AADT = all <br> length > 3300 m",
            "0 < AADT <= 10,000 <br> length> 3300 m",
            "10,000 < AADT <= 20,000 <br> length > 3300 m",
            "AADT > 20,000 <br> length > 3300 m",
            "AADT = all <br> length <= 3400 m",
            "0 < AADT <= 10,000 <br> length <= 3400 m",
            "10,000 < AADT <= 20,000 <br> length <= 3400 m",
            "AADT > 20,000 <br> length <= 3400 m",
            "AADT = all <br> length > 3400 m",
            "0 < AADT <= 10,000 <br> length > 3400 m",
            "10,000 < AADT <= 20,000 <br> length > 3400 m",
            "AADT > 20,000 <br> length > 3400 m"
            ),
          model.numbers = TRUE,
          
          type='html',out="./tables2021/wzaadt_length_sens.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
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
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Table",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y")),
                         # c("work zone length control", "<= 2,000","> 2,000","<= 2,000","> 2,000"),
                         # c("AADT control", " all ", " all ", "(0, 10,000]","(0, 10,000]",
                           # "(10,000, 20,000]",
                           # "(20,000, ...)")),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)

#4. find nighttime AADT /in (0,1000] regression ----
results_aadt_daytime = list()
results_aadt_daytime <- append(results_aadt_daytime,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +   aadt_new_log  + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet   +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09+ year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0 & netlength > 0  & daytimeofday==0 & aadt_new<10000])))

stargazer(
  results_aadt_daytime[1],
  column.labels = c(
    "0 < AADT <= 10,000"
  ),
  model.numbers = TRUE,
  type = 'html',
  out = "./tables2021/wzaadt_day_specialcase.html",
  omit = c(
    "month_02",
    "month_03",
    "month_04",
    "month_05",
    "month_06",
    "month_07",
    "month_08",
    "month_09",
    "month_10",
    "month_11",
    "month_12",
    "year_2014",
    "year_2016",
    "year_2017",
    "district_1",
    "district_2",
    "district_3",
    "district_4",
    "district_5",
    "district_6",
    "district_8",
    "district_9",
    "district_10",
    "district_11",
    "district_12"
  ),
  covariate.labels = c(
    "Roadwork",
    "Week",
    "Duration(s; log)",
    "Length (m; log)",
    "Weekday of week",
    #    "Daytime of day",
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
    #"Roadwork * Length (m; log)",
    #  "Absolute value of Actual speed detreated 2 (A')(mph)",
    # "Roadwork * Duration(s; log)",
    # "Roadwork * Length (m; log)",
    # "Roadwork * Weekday of week",
    #"Roadwork * Daytime of day",
    # paste("sequence >=", as.character(i) ," hour",sep=''),
    # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
    "Constant"
  ),
  dep.var.caption  = "Nighttime work zones",
  dep.var.labels   = "Crash occurrence",
  add.lines = list(
    c("Monthly Dummies", "Y", "Y", "Y", "Y"),
    c("Yearly Dummies", "Y", "Y", "Y", "Y")
  ),
  # c("work zone daytime control", "night","day","day","> 2,000",
  #   "length <= 20,000",
  #   "length <= 20,000",
  #   "length <= 20,000",
  #   "length <= 20,000"),
  # c("AADT control", " all ", " all ", "(0, 10,000]","(0, 10,000]",
  #   "(10,000, 20,000]",
  #   "(20,000, ...)")),
  align = TRUE,
  no.space = TRUE,
  single.row = TRUE
)

## 5. find the cut-off breakpoint seperating high AADT and medium/low AADT ----
fourmula_nonhs = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
                                                         daytimeofday +   aadt_new_log   + num_inters_log + lanecounts_1 +
                                                         speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
                                                         month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
                                                         month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_aadt_break = list()


results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>20000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>19000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>18000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>17000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>16000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>15000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>14000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>13000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>12000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>11000])))

results_aadt_break =  append(results_aadt_break,list(strati_regress( formula = fourmula_nonhs,data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new>10000])))

stargazer(results_aadt_break,
          column.labels = c(
            "AADT > 20,000","AADT > 19,000","AADT > 18,000","AADT > 17,000","AADT > 16,000",
            "AADT > 15,000","AADT > 14,000","AADT > 13,000","AADT > 12,000","AADT > 11,000",            "AADT > 10,000"),
          model.numbers = TRUE,
          type='html',out="./tables2021/wzaadt_breakpoint.html",omit = c("month_02","month_03","month_04","month_05","month_06","month_07","month_08","month_09","month_10","month_11","month_12","year_2014","year_2016","year_2017","district_1","district_2","district_3","district_4","district_5","district_6","district_8","district_9","district_10","district_11","district_12"),
          covariate.labels = c("Work zone presence", 
                               "Week",
                               "Duration(seconds; log)",
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
                               #"Roadwork * Length (m; log)",
                               #  "Absolute value of Actual speed detreated 2 (A')(mph)",
                               # "Roadwork * Duration(s; log)",
                               # "Roadwork * Length (m; log)",
                               # "Roadwork * Weekday of week",
                               #"Roadwork * Daytime of day",
                               # paste("sequence >=", as.character(i) ," hour",sep=''),
                               # paste("Roadwork * sequence >=", as.character(i) ," hour",sep=''),
                               "Constant"),
          dep.var.caption  = "Work zones with different AADTs",
          dep.var.labels   = "Crash occurrence",
          add.lines=list(c("Monthly Dummies", "Y","Y","Y","Y"),
                         c("Yearly Dummies", "Y","Y","Y","Y")),
                         #  c("work zone length control", "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000",
                         #    "length <= 20,000"),
                         # c("AADT control", " all ", "(0, 10,000]",
                         #   "(10,000, 20,000]",
                         #   "(20,000, ...)")),
          align=TRUE,
          no.space=TRUE,
          single.row = TRUE)
# 6. calculation of odds ratio, sec5.5 ----

exp(0.531)
exp(-8.181)
#verify whether the time of day choice of work zone deployment is not a result of crash risks

summary(df[daytimeofday == 1 & control < 0,crash_61])

chisq.test(rbind(table(df[daytimeofday == 1 & control < 0, 'crash_61']),
                 table(df[daytimeofday == 0 & control < 0, 'crash_61'])))

summary(df[daytimeofday == 0 & control < 0,crash_61])
summary(df[daytimeofday == 0 & control == 0,crash_61])
summary(df[daytimeofday == 0 & control > 0,crash_61])


summary(df[daytimeofday == 0 & control < 0 & aadt_new>10000 & aadt_new <20000,crash_61])
summary(df[daytimeofday == 0 & control == 0& aadt_new>10000 & aadt_new <20000,crash_61])
summary(df[daytimeofday == 0 & control > 0& aadt_new>10000 & aadt_new <20000,crash_61])
summary(df[daytimeofday == 0 & control != 0& aadt_new>10000 & aadt_new <20000,crash_61])

# 6.diuscussion in section 5.6 ----

