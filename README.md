# Work zone safety study

The code in this project is finished in three step:

1. Use Python to perform map-matching on work zones and crashes. Save the output as separate files.
2. Export separate files into Sqlite3 and PostgreSQL databases. Then use SQL and use Python to do data fusion.
3. Using R, import the processed data and do the major model analysis.
4. Some robustness tests require new data sets (spatial robustness tests and bandwidth sensitivity tests), so some wrapped code are created in `datavariation/wzsafety` to quickly produce required new data set with configure files `wzspatial.yaml` and `wzsens.yaml`.
5. Most model analysis are finished in R, while `./models/rebust_firth_20200823.do` is executed in Stata.
## Data processing

These codes are stored at `./datapreprocessing`.

### Map-matching

1. Using the work zone data (from [PennDOT Road Condition Reporting System](https://www.penndot.gov/Doing-Business/OnlineServices/Pages/Developer-Resources-DocumentationAPI.aspx)) and roadway network data (from [PennDOT Open Share, PennShare](https://data-pennshare.opendata.arcgis.com/datasets/rmsseg-state-roads)), run map-matching algorithms in `./datapreprocessing/map-matching-workzone-within.py`. This step will identify area of work zones on the PennShare map.
2. Run `./datapreprocessing/map-matching-workzone-all-files-to-db.py`. This step will identify the upstream and downstream area of work zones on the PennShare map. The results will save in a Sqlite3 database (`wz_loc.db`).
3. Using the [PennDOT crash data](https://pennshare.maps.arcgis.com/apps/webappviewer/index.html?id=8fdbf046e36e41649bbfd9d7dd7c7e7e), run `./datapreprocessing/map-matching-crash.py`. This step will identify the locations of crashes, stored in separate files.
4. Run `./datapreprocessing/crash-files-to-db.py`. This step will convert the location of crashes into a Sqlite3 database (`crash_db.db`).

### Other work zone information to database

1. Run `./datapreprocessing/workzone-info-to-db-step-1.py`. This step stored the general information of work zones in to `output_wz.db`.
2. Run `./datapreprocessing/helpful-files-to-db.py`. This step will store the speed limit data into `wz_loc.db`, and Traffic Message Channel
segments (TMC segments) data to `PennMultiId.db`.

### Data fusion

1. Run `./datapreprocessing/crash_match.py` for matching crash information.
2. Run `./datapreprocessing/weather_match.py` for matching weather information.
3. Run `./datapreprocessing/speed_match.py` for matching speed information.
4. Run `./datapreprocessing/wzinfo.py` for matching work zone information.
5. Run `./datapreprocessing/wz_output.py` for fully matched work zone data.
6. Run `./datapreprocessing/select_non_sequential_15.py` for selecting work zones whose previous six and after six weeks has no work zones.
7. The final data set is queried by `./datapreprocessing/output15_non_sequential.sql`

## Produce data for sensitivity analysis

1. Run `./datavariation/wzsafety/wz_sensitivity.py` using the configuration file `./datavariation/wzsens.yaml`

## Produce data for spatial robustness tests

1. Run `./datavariation/wzsafety/wzspatial.py` using the configuration file `./datavariation/wzspatial.yaml`

## Analysis models

1. The main results are given by running `./models/main_results.R`.
2. The visualization of the main results are given by running `./models/main_results_visualization.R`
3. Run `./models/robustness_tests.R` to obtain the results of bandwidth_sensitivity test, Function form test, and temporal placebo test.
4. Run `./models/robustness_tests_crashlocation.R` to obtain the results of spatial placebo test.
5. Run `./models/sensitivity_test.R` to obtain the results of sensitivity test.
6. Run `./models/rebust_firth_20200823.do` to obtain the results of Firth logistics regression.
