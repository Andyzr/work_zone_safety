clear all
cd D:/zhuoran1/AAP
use wzs_output14_17_20200823.dta

set more off
set matsize 1000
**************label data********
label variable crash_61 "Crash occurrence"
label variable crash_severe_61 "Severe crash occurrence"
label variable treatment_use   "Roadwork" 
label variable control   "WeekN" 
label variable avew   "Average wind speed (mph)" 
label variable avet   "Average temperature (F)" 
label variable avep_denull   "Average preciption (inch)" 
label variable real_speed_61   "Actual speed (mph)" 
label variable nhs_ind_major "NHS major roads"
label variable num_inters_log "# of intersections (log)"
label variable aadt_new_log    "AADT (log)"
label variable lanecounts_1    "Lane counts = 1"
label variable speed_limit  "Speed limit"
label variable duration_log "Duration(s; log)"
label variable netlength_log "Length (m; log)"
label variable weekdayofweek "Weekday of week"
label variable daytimeofday "Daytime of day"
label variable treatment_use_closure_type "WeekN X Closure type"
label variable treatment_use_sequence_num "WeekN X Sequence"

// adopath ++ "U:\WorkZone\"

***1. all set *****
/* eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek daytimeofday aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 


esttab  using "//tsclient/C/Users/zhang/Box\ Sync/Workzone\ (zhuoran1@andrew.cmu.edu)/Paper_2019/tables/wz_effect_firth_real_speed_61_oris.rtf",compress indicate("Monthly dummies = *month_*" "Yearly dummies = *year_*" ) scalars(ll chi2) varwidth(45)  nobaselevels interaction(" X ") label replace */

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek daytimeofday aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 300 & netlength > 5 & netlength<=20000 & closure ==0.5
esttab using output/wz_effect_firth_detreated.rtf,compress indicate("Monthly dummies = *month_*" "Yearly dummies = *year_*" ) scalars(ll chi2) varwidth(45)  nobaselevels interaction(" X ") label replace wide se r2 star(* 0.10 ** 0.05 *** 0.01)
/* *********************2. robustness tests - daytimeofday*******************
eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & daytimeofday ==0

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 & daytimeofday ==1

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new>20000  & daytimeofday ==0

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new>20000  & daytimeofday ==1

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new<10000  & daytimeofday ==0

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new<10000  & daytimeofday ==1

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & daytimeofday ==0

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek  aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & daytimeofday ==1

esttab est1 est2 est3 est4 est5 est6 est7 est8 using output/wz_daytime.rtf,compress indicate("Monthly dummies = *month_*" "Yearly dummies = *year_*" ) scalars(ll chi2) varwidth(45)  nobaselevels interaction(" X ") label replace wide se r2 star(* 0.10 ** 0.05 *** 0.01)

*********************2. robustness tests - aadt_new*******************
eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek daytimeofday aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new<=10000

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek daytimeofday aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new>10000 & aadt_new<=20000 

eststo: firthlogit crash_61  treatment_use   control duration_log  netlength_log weekdayofweek daytimeofday aadt_new_log nhs_ind_major  num_inters_log  lanecounts_1 speed_limit    avew avet avep_denull real_speed_61_detreat_ind  month_02 month_03 month_04 month_05 month_06 month_07 month_08 month_09 month_10 month_11 month_12 year_2014 year_2016 year_2017 if location=="in" & wzid_new < 100000000 & avet_exists==1 &  speed_61_exists==1 & duration > 0 & netlength > 0 & netlength<=20000 & aadt_new>20000  

esttab est9 est10 est11 using output/wz_aadt.rtf,compress indicate("Monthly dummies = *month_*" "Yearly dummies = *year_*" ) scalars(ll chi2) varwidth(45)  nobaselevels interaction(" X ") label replace wide se r2 star(* 0.10 ** 0.05 *** 0.01) */
