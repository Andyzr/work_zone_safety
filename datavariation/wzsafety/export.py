from .utils import export_shp_postgresql
from .DatabaseUtility import engine_post

from os import listdir
from os.path import isfile, join

##filenames
mypath = "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
