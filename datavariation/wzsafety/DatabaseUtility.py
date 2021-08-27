# import mysql.connector
from sqlalchemy import create_engine
import psycopg2  # (if it is postgres/postgis)

"""example:bridge_unc = pd.read_sql("SELECT * FROM bms2.features3;",engine)
pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND table_schema='bms2';",engine)
bridge_unc.to_sql(str(i),engine_post, schema='bms2')
TIP = gpd.GeoDataFrame.from_postgis("SELECT * FROM public.transportation_improvement_projects__points;",engine_post)
"""
# engine = create_engine('mysql+mysqlconnector://fake:fakepassword@localhost:fake/fake',
#                        echo=False)

engine_post = create_engine('postgresql://postgres:fakepassword@localhost:fakeport/gisdb')

engine_post_public = create_engine('postgresql://postgres:fakepassword@localhost:fakeport/public')

# sql = "select geom, x,y,z from your_table"

# df = gpd.GeoDataFrame.from_postgis(sql, con, geom_col='geom' )
