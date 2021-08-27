# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle
# import gc
# from sqlalchemy import create_engine
# import sqlite3
# from sqlalchemy import Column, Integer, String, ForeignKey, Float
# from _datetime import time

from .utils import read_config
from .utils import create_pseudo_wz
from .utils import create_pseudo_wz_divided
from .utils import extract_crash_info
from .utils import extract_speed_info
from .utils import extract_speed_info_wzsens
from .utils import extract_weather_info
from .utils import extract_speedlimit_AADT_info
from .utils import join_feature_tables
from .utils import extract_numofinters_info
from .utils import extract_weather_info_wzsens
# from .prep import extract_pseudo_wz
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)


def main():
    log.info("Start!")
    config = read_config(file_name='wzsens.yaml')
    # # create pseudo wzs
    # create_pseudo_wz('wzsafety/queries/wzsens_create_wz.sql.tmpl', config)
    log.info("Done create pseudo wzs!")
    # # create pseduo wz divided
    # create_pseudo_wz_divided('wzsafety/queries/wzsens_create_wz_divided.sql.tmpl', config)
    log.info("Done create pseudo wz divided!")
    # # extract crash info
    # extract_crash_info('wzsafety/queries/wzsens_extract_crash_info.sql.tmpl', config)
    log.info("Done extract crash infos!")
    # extract speed info
    # extract_speed_info_wzsens(pseudo_info_query_loc = 'wzsafety/queries/wzsens_create_pseudo_wz_divided_info_for_speed.sql.tmpl',
    # sqlite_join_query_loc = 'wzsafety/queries/wzsens_extract_speed_info.sql.tmpl',
    # config = config)
    log.info("Done extract speed infos!")
    # extract weather info
    # extract_weather_info_wzsens(pseudo_info_query_loc = 'wzsafety/queries/wzsens_create_pseudo_wz_divided_info_for_weather.sql.tmpl',
    # sqlite_weather_join_query_loc = 'wzsafety/queries/wzsens_extract_weather_info.sql.tmpl', config = config)
    log.info("Done extract weather infos!")
    # matching AADT and Speed_limit information
    # extract_speedlimit_AADT_info(query_loc = 'wzsafety/queries/extract_speedlimit_AADT_info.sql.tmpl', config = config)
    log.info("Done extract speed_limit and aadt infos!")
    # extract num_of_inters_info
    # extract_numofinters_info(query_loc = 'wzsafety/queries/extract_numberofinters_info.sql.tmpl', config = config)
    log.info("Done extract numberofinters tables!")
    # join all features together
    join_feature_tables(query_loc='wzsafety/queries/wzsens_join_pseudo_wz.sql.tmpl', config=config)
    log.info("Done join feature tables!")


if __name__ == '__main__':
    main()
