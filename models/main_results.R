#----read data
library('tidyverse')
library('rms')
library('ggplot2')
library('ggpubr')
setwd(
  '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/scripts/R_code/workzone_r_2021'
)
source("./src/stratificationFunction.R")
load('detreated_speed.RData')
library(stargazer)


#0. data encoding ----
print(length(unique(df[wzid_new < 100000000 &
                         location == 'in' &
                         avet_exists == 1 &
                         speed_61_exists == 1 &
                         duration > 300  &
                         netlength > 5 & netlength <= 20000 & closure == 0.5, wzid_new])))

print(summary(df[wzid_new < 100000000 &
                   location == 'in' &
                   avet_exists == 1 &
                   speed_61_exists == 1 &
                   duration > 300  &
                   netlength > 5 & netlength <= 20000 & closure == 0.5, duration]))

print(summary(df[wzid_new < 100000000 &
                   location == 'in' &
                   avet_exists == 1 &
                   speed_61_exists == 1 &
                   duration > 300  &
                   netlength > 5 & netlength <= 20000 & closure == 0.5, netlength]))

print(nrow(df[wzid_new < 100000000 &
                location == 'in' &
                avet_exists == 1 &
                speed_61_exists == 1 &
                duration > 300  &
                netlength > 5 & netlength <= 20000 & closure == 0.5]))

wzid_new_list <- unique(df[wzid_new < 100000000 &
                             location == 'in' &
                             avet_exists == 1 &
                             speed_61_exists == 1 &
                             duration > 300  &
                             netlength > 5 & netlength <= 20000 & closure == 0.5, wzid_new])
saveRDS(wzid_new_list, file = "./outputData/wzid_new_list.rds")

print(summary(df[wzid_new < 100000000 &
                   location == 'in' &
                   avet_exists == 1 &
                   speed_61_exists == 1 &
                   duration > 300  &
                   netlength > 5 & netlength <= 20000 & closure == 0.5 & control!=0, crash_61]))

print(summary(df[wzid_new < 100000000 &
                   location == 'in' &
                   avet_exists == 1 &
                   speed_61_exists == 1 &
                   duration > 300  &
                   netlength > 5 & netlength <= 20000 & closure == 0.5 & control ==0, crash_61]))

##1. visualization of crash log odds in various weeks ----
#logit(crash)~ control

d1 <- df[wzid_new < 100000000 &
           location == 'in' &
           avet_exists == 1 &
           speed_61_exists == 1 &
           duration > 300  &
           netlength > 5  & netlength <= 20000 & closure == 0.5] %>%
  select(control, crash_61) %>%
  group_by(control) %>%
  summarise(
    prop := mean(crash_61),
    sd := sd(crash_61),
    logodds := log(mean(crash_61) / (1 - mean(crash_61))),
    crash_counts := sum(crash_61),
    logodds_sd := sqrt(1 / sum(crash_61) + 1 / (n() - sum(crash_61)))
  ) %>%
  select(control, prop, sd, logodds, logodds_sd, crash_counts) %>%
  ggplot(aes(x = control, y = logodds, label = crash_counts)) +
  # geom_line()+
  geom_point() +
  # geom_text(hjust=0, vjust=2)+
  geom_errorbar(aes(ymin = logodds - logodds_sd, ymax = logodds + logodds_sd),
                width = .1) +
  # ggtitle("Work zones occurred in year 2015&2016&2017") +
  xlab("Week") + ylab("Average crash occurrence (log odds)") +
  geom_vline(xintercept = 0,
             linetype = "dashed",
             color = "red") + theme_minimal()
ggsave(
  "./figs2021/crash_control.png",
  width = 20,
  height = 15,
  units = "cm"
)

###1.2 chi-square test ----
chisq.test(rbind(table(df[wzid_new < 100000000 &
                            location == 'in' &
                            avet_exists == 1 &
                            speed_61_exists == 1 &
                            duration > 300  &
                            netlength > 5  & netlength <= 20000 & closure == 0.5 &
                            control == 0, 'crash_61']),
                 table(df[wzid_new < 100000000 &
                            location == 'in' &
                            avet_exists == 1 &
                            speed_61_exists == 1 &
                            duration > 300  &
                            netlength > 5  & netlength <= 20000 & closure == 0.5 &
                            control != 0, 'crash_61'])))

##2. regression results output ----

##2.1 wz detreated speed ----
formula_base <-
  "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_speed <- list()

results_speed <-
  append(results_speed, list(
    strati_regress(
      formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
      daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +
      speed_limit +   avew + avet + avep_denull  +real_speed_61+month_02 +
      month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
      month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 & netlength <= 20000 & closure == 0.5]
    )
  ))
results_speed <-
  append(results_speed, list(strati_regress(formula = formula_base,
                                            data = df[wzid_new < 100000000 &
                                                        location == 'in' &
                                                        avet_exists == 1 &
                                                        speed_61_exists == 1 &
                                                        duration > 300  &
                                                        netlength > 5 & netlength <= 20000 & closure == 0.5])))

saveRDS(results_speed, file = "./outputData/results_speed.rds")

stargazer(
  results_speed[2],
  type = 'html',
  out = "./tables2021/wz_detreatspeed.html",
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
    "Constant"
  ),
  dep.var.caption  = "All work zones",
  dep.var.labels   = "Crash occurrence",
  add.lines = list(
    c("Monthly Dummies", "Y", "Y", "Y", "Y"),
    c("Yearly Dummies", "Y", "Y", "Y", "Y")
    #  c("work zone length control", "length <= 20,000",
    #    "length <= 20,000",
    #    "length <= 20,000",
    #    "length <= 20,000",
    #    "length <= 20,000"),
    #  c("AADT control", " all ", "(0, 10,000]",
    #    "(10,000, 20,000]",
    #    "(20,000, ...)"
  ),
  align = TRUE,
  no.space = TRUE,
  single.row = TRUE
)

#3. effect modification of roadway characteristics -----
##3.1 wz classified by AADT ----

formula_base <-
  "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_aadt <- list()

results_aadt <-
  append(results_aadt, list(strati_regress(formula = formula_base,
                                           data = df[wzid_new < 100000000 &
                                                       location == 'in' &
                                                       avet_exists == 1 &
                                                       speed_61_exists == 1 &
                                                       duration > 300  &
                                                       netlength > 5 & netlength <= 20000 & closure == 0.5])))

results_aadt <-
  append(results_aadt, list(strati_regress(formula = formula_base,
                                           data = df[wzid_new < 100000000 &
                                                       location == 'in' &
                                                       avet_exists == 1 &
                                                       speed_61_exists == 1 &
                                                       duration > 300  &
                                                       netlength > 5 &
                                                       netlength <= 20000 & aadt_new <= 10000 & closure == 0.5])))


results_aadt <-
  append(results_aadt, list(strati_regress(formula = formula_base,
                                           data = df[wzid_new < 100000000 &
                                                       location == 'in' &
                                                       avet_exists == 1 &
                                                       speed_61_exists == 1 &
                                                       duration > 300  &
                                                       netlength > 5 &
                                                       netlength <= 20000 &
                                                       aadt_new > 10000 & aadt_new <= 20000 & closure == 0.5])))

results_aadt <-
  append(results_aadt, list(
    strati_regress(
      formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
      daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
      speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
      month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
      month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 & aadt_new > 20000 & closure == 0.5]
    )
  ))

saveRDS(results_aadt, file = "./outputData/results_aadt.rds")

stargazer(
  results_aadt[1],
  results_aadt[2],
  results_aadt[3],
  results_aadt[4],
  column.labels = c(
    "AADT = all",
    "0 < AADT <= 10,000",
    "10,000 < AADT <= 20,000",
    "AADT > 20,000"
  ),
  model.numbers = TRUE,
  type = 'html',
  out = "./tables2021/wzaadt.html",
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
    "Constant"
  ),
  dep.var.caption  = "All work zones",
  dep.var.labels   = "Crash occurrence",
  add.lines = list(
    c("Monthly Dummies", "Y", "Y", "Y", "Y"),
    c("Yearly Dummies", "Y", "Y", "Y", "Y")
    #  c("work zone length control", "length <= 20,000",
    #    "length <= 20,000",
    #    "length <= 20,000",
    #    "length <= 20,000",
    #    "length <= 20,000"),
    # c("AADT control", " all ", "(0, 10,000]",
    # "(10,000, 20,000]",
    # "(20,000, ...)")
  ),
  align = TRUE,
  no.space = TRUE,
  single.row = TRUE
)

# 4. stratification of deployment configurations on different roadways with various aadt---------
#4.1 subset regression; netlength boundaries: 3000 meters-------
formula_base <-
  "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_aadt_length <- list()

results_aadt_length <-
  append(results_aadt_length, list(strati_regress(formula = formula_base,
                                                  data = df[wzid_new < 100000000 &
                                                              location == 'in' &
                                                              avet_exists == 1 &
                                                              speed_61_exists == 1 &
                                                              duration > 300  &
                                                              netlength > 5 &
                                                              netlength <= 20000 & netlength <= 3000 & closure == 0.5])))

results_aadt_length <-
  append(results_aadt_length, list(strati_regress(formula = formula_base,
                                                  data = df[wzid_new < 100000000 &
                                                              location == 'in' &
                                                              avet_exists == 1 &
                                                              speed_61_exists == 1 &
                                                              duration > 300  &
                                                              netlength > 5 &
                                                              netlength <= 20000 & netlength > 3000 & closure == 0.5])))

results_aadt_length <-
  append(results_aadt_length, list(strati_regress(formula = formula_base,
                                                  data = df[wzid_new < 100000000 &
                                                              location == 'in' &
                                                              avet_exists == 1 &
                                                              speed_61_exists == 1 &
                                                              duration > 300  &
                                                              netlength > 5 &
                                                              netlength <= 20000 &
                                                              aadt_new <= 10000 & netlength <= 3000 & closure == 0.5])))

results_aadt_length <-
  append(results_aadt_length, list(
    strati_regress(
      formula = formula_base,
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 &
                  aadt_new <= 10000 & netlength > 3000 & closure == 0.5]
    )
  ))


results_aadt_length <-
  append(results_aadt_length, list(
    strati_regress(
      formula = formula_base,
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 &
                  aadt_new > 10000 &
                  aadt_new <= 20000 & netlength <= 3000 & closure == 0.5]
    )
  ))

results_aadt_length <-
  append(results_aadt_length, list(strati_regress(formula = formula_base,
                                                  data = df[wzid_new < 100000000 &
                                                              location == 'in' &
                                                              avet_exists == 1 &
                                                              speed_61_exists == 1 &
                                                              duration > 300  &
                                                              netlength > 5 &
                                                              netlength <= 20000 &
                                                              aadt_new > 10000 &
                                                              aadt_new <= 20000 & netlength > 3000 & closure == 0.5])))

results_aadt_length <-
  append(results_aadt_length, list(
    strati_regress(
      formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +
daytimeofday +   aadt_new_log  + num_inters_log + 
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 &
                  aadt_new > 20000 & netlength <= 3000 & closure == 0.5]
    )
  ))

results_aadt_length <-
  append(results_aadt_length, list(
    strati_regress(
      formula = formula_base,
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 &
                  aadt_new > 20000 & netlength > 3000 & closure == 0.5]
    )
  ))

saveRDS(results_aadt_length, file = "./outputData/results_aadt_length.rds")

stargazer(
  results_aadt_length[1],
  results_aadt_length[3],
  results_aadt_length[5],
  results_aadt_length[7],
  column.labels = c(
    "AADT = all",
    "0 < AADT <= 10,000",
    "10,000 < AADT <= 20,000",
    "AADT > 20,000"
  ),
  model.numbers = TRUE,
  type = 'html',
  out = "./tables2021/wzaadt_length_short.html",
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
    "Constant"
  ),
  dep.var.caption  = "Work zone length <= 3,000 meters",
  dep.var.labels   = "Crash occurrence",
  add.lines = list(
    c("Monthly Dummies", "Y", "Y", "Y", "Y"),
    c("Yearly Dummies", "Y", "Y", "Y", "Y")
  ),
  # c("work zone length control", "<= 2,000","> 2,000","<= 2,000","> 2,000"),
  # c("AADT control", " all ", " all ", "(0, 10,000]","(0, 10,000]",
  #   "(10,000, 20,000]",
  #   "(20,000, ...)")
  #                         ),
  align = TRUE,
  no.space = TRUE,
  single.row = TRUE
)


stargazer(
  results_aadt_length[2],
  results_aadt_length[4],
  results_aadt_length[6],
  results_aadt_length[8],
  column.labels = c(
    "AADT = all",
    "0 < AADT <= 10,000",
    "10,000 < AADT <= 20,000",
    "AADT > 20,000"
  ),
  model.numbers = TRUE,
  type = 'html',
  out = "./tables2021/wzaadt_length_long.html",
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
    "Constant"
  ),
  dep.var.caption  = "Work zone length > 3,000 meters",
  dep.var.labels   = "Crash occurrence",
  add.lines = list(
    c("Monthly Dummies", "Y", "Y", "Y", "Y"),
    c("Yearly Dummies", "Y", "Y", "Y", "Y")
  ),
  # c("work zone length control", "<= 2,000","> 2,000","<= 2,000","> 2,000",
  #   "length <= 20,000",
  #   "length <= 20,000",
  #   "length <= 20,000",
  #   "length <= 20,000"),
  # c("AADT control",
  #   "(10,000, 20,000]","(10,000, 20,000]",
  #   "(20,000, ...)", "(20,000, ...)")),
  align = TRUE,
  no.space = TRUE,
  single.row = TRUE
)


# 4.2 whether perform work zones during daytime -----
# ggarrange(deployment_visualizes[[10]],deployment_visualizes[[11]], deployment_visualizes[[12]],
#           labels = "AUTO",
#           ncol = 3, nrow = 1)
# ggsave( "//tsclient/C/Users/zhang/Box\ Sync/Workzone\ (zhuoran1@andrew.cmu.edu)/Presentations/fig/deployment_aadt_daytime.png",width = 30, height = 9, units = "cm")

# hists_aadt_deploy2 <- list()
# for (xi in c(
#   "daytimeofday" ,
#   "closure"
# )) {
#   hists_aadt_deploy2 <- append(hists_aadt_deploy2,hist_ggplot(variablename = xi,data =  df[wzid_new < 100000000 &
#                     location == 'in' &
#                     avet_exists == 1 &
#                     speed_61_exists == 1 &
#                     duration > 0  & netlength > 0 & netlength <= 20000 & aadt_new <= 10000],density = FALSE))
#   hists_aadt_deploy2 <- append(hists_aadt_deploy2,hist_ggplot(variablename = xi,data =  df[wzid_new < 100000000 &
#                     location == 'in' &
#                     avet_exists == 1 &
#                     speed_61_exists == 1 &
#                     duration > 0  & netlength > 0 & netlength <= 20000 & aadt_new > 10000 & aadt_new <= 20000 ],density = FALSE))
#   hists_aadt_deploy2 <- append(hists_aadt_deploy2,hist_ggplot(variablename = xi,data =  df[wzid_new < 100000000 &
#                     location == 'in' &
#                     avet_exists == 1 &
#                     speed_61_exists == 1 &
#                     duration > 0  & netlength > 0 & netlength <= 20000 & aadt_new > 20000],density = FALSE))
# }
# # hists_aadt_deploy2[[1]]
# # hists_aadt_deploy2[[2]]
# # hists_aadt_deploy2[[3]]
# # hists_aadt_deploy2[[4]]
# # hists_aadt_deploy2[[5]]
# # hists_aadt_deploy2[[6]]

# ggarrange(hists_aadt_deploy2[[1]],hists_aadt_deploy2[[2]], hists_aadt_deploy2[[3]],
#           labels = "AUTO",
#           ncol = 3, nrow = 1)
# ggsave( "//tsclient/C/Users/zhang/Box\ Sync/Workzone\ (zhuoran1@andrew.cmu.edu)/Presentations/fig/hist_aadt_daytime.png",width = 30, height = 9, units = "cm")



formula_day <-
  "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek  +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 +
speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017"

results_aadt_daytime <- list()

results_aadt_daytime <-
  append(results_aadt_daytime, list(strati_regress(formula = formula_day,
                                                   data = df[wzid_new < 100000000 &
                                                               location == 'in' &
                                                               avet_exists == 1 &
                                                               speed_61_exists == 1 &
                                                               duration > 300  &
                                                               netlength > 5 &
                                                               netlength <= 20000 & daytimeofday == 0 & closure == 0.5])))

results_aadt_daytime <-
  append(results_aadt_daytime, list(strati_regress(formula = formula_day,
                                                   data = df[wzid_new < 100000000 &
                                                               location == 'in' &
                                                               avet_exists == 1 &
                                                               speed_61_exists == 1 &
                                                               duration > 300  &
                                                               netlength > 5 &
                                                               netlength <= 20000 & daytimeofday == 1 & closure == 0.5])))

#not fitting to fitting --- see results_5p4_5p5_sensitivity.R

# strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +   aadt_new_log  + num_inters_log + lanecounts_1 +
# speed_limit +   avew + avet +avep_denull  +real_speed_61_detreat_ind+month_02 +
# month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
# month_10 + month_11 + month_12 + year_2016 + year_2017",data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 300  & netlength > 5 & netlength<=20000 & daytimeofday ==0 & closure ==0.5 & aadt_new<10000])

# results_aadt_daytime <- append(results_aadt_daytime,list(strati_regress( formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek  +   aadt_new_log + nhs_ind_major + num_inters_log + lanecounts_1 + speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 + month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 + month_10 + month_11 + month_12  + year_2016 + year_2017", data = df[wzid_new < 100000000 &location == 'in' & avet_exists == 1 & speed_61_exists ==1 & duration > 0& netlength > 0 & netlength<=20000 & aadt_new<=10000 & daytimeofday ==0])))

results_aadt_daytime <-
  append(results_aadt_daytime, list(strati_regress(formula = formula_day,
                                                   data = df[wzid_new < 100000000 &
                                                               location == 'in' &
                                                               avet_exists == 1 &
                                                               speed_61_exists == 1 &
                                                               duration > 300  &
                                                               netlength > 5 &
                                                               netlength <= 20000 &
                                                               aadt_new <= 10000 & daytimeofday == 1 & closure == 0.5])))


results_aadt_daytime <-
  append(results_aadt_daytime, list(strati_regress(formula = formula_day,
                                                   data = df[wzid_new < 100000000 &
                                                               location == 'in' &
                                                               avet_exists == 1 &
                                                               speed_61_exists == 1 &
                                                               duration > 300  &
                                                               netlength > 5 &
                                                               netlength <= 20000 &
                                                               aadt_new > 10000 &
                                                               aadt_new <= 20000 & daytimeofday == 0 & closure == 0.5])))

results_aadt_daytime <-
  append(results_aadt_daytime, list(strati_regress(formula = formula_day,
                                                   data = df[wzid_new < 100000000 &
                                                               location == 'in' &
                                                               avet_exists == 1 &
                                                               speed_61_exists == 1 &
                                                               duration > 300  &
                                                               netlength > 5 &
                                                               netlength <= 20000 &
                                                               aadt_new > 10000 &
                                                               aadt_new <= 20000 & daytimeofday == 1 & closure == 0.5])))

results_aadt_daytime <-
  append(results_aadt_daytime, list(
    strati_regress(
      formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek  +   aadt_new_log  + num_inters_log  +
      speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
      month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
      month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 &
                  aadt_new > 20000 & daytimeofday == 0 & closure == 0.5]
    )
  ))

results_aadt_daytime <-
  append(results_aadt_daytime, list(
    strati_regress(
      formula = "crash_61 ~ treatment_use + control + duration_log + netlength_log + weekdayofweek +   aadt_new_log  + num_inters_log + lanecounts_1 +
      speed_limit +   avew + avet + avep_denull  +real_speed_61_detreat_ind+month_02 +
      month_03 + month_04 + month_05 + month_06 + month_07 + month_08 + month_09 +
      month_10 + month_11 + month_12 + year_2014 + year_2016 + year_2017",
      data = df[wzid_new < 100000000 &
                  location == 'in' &
                  avet_exists == 1 &
                  speed_61_exists == 1 &
                  duration > 300  &
                  netlength > 5 &
                  netlength <= 20000 &
                  aadt_new > 20000 & daytimeofday == 1 & closure == 0.5]
    )
  ))

saveRDS(results_aadt_daytime, file = "./outputData/results_aadt_daytime.rds")

stargazer(
  results_aadt_daytime[2],
  results_aadt_daytime[3],
  results_aadt_daytime[5],
  results_aadt_daytime[7],
  column.labels = c(
    "AADT = all",
    "0 < AADT <= 10,000",
    "10,000 < AADT <= 20,000",
    "AADT > 20,000"
  ),
  model.numbers = TRUE,
  type = 'html',
  out = "./tables2021/wzaadt_day.html",
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
    "Constant"
  ),
  dep.var.caption  = "Daytime work zones",
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


stargazer(
  results_aadt_daytime[1],
  results_aadt_daytime[4],
  results_aadt_daytime[6],
  column.labels = c("AADT = all", "10,000 < AADT <= 20,000", "AADT > 20,000"),
  model.numbers = TRUE,
  type = 'html',
  out = "./tables2021/wzaadt_night.html",
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
    "Constant"
  ),
  dep.var.caption  = "Nighttime work zones",
  dep.var.labels   = "Crash occurrence",
  add.lines = list(
    c("Monthly Dummies", "Y", "Y", "Y", "Y"),
    c("Yearly Dummies", "Y", "Y", "Y", "Y")
  ),
  # c("work zone daytime control", "night","day","night","day","> 2,000",
  #   "length <= 20,000",
  #   "length <= 20,000",
  #   "length <= 20,000",
  #   "length <= 20,000"),
  # c("AADT control",
  #   "(10,000, 20,000]","(10,000, 20,000]",
  #   "(20,000, ...)","(20,000, ...)")),
  align = TRUE,
  no.space = TRUE,
  single.row = TRUE
)
