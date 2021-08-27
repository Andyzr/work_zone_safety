from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
import geopandas as gpd
import sqlite3

from .DatabaseUtility import engine_post
import re
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.linestring import LineString
import yaml
import psycopg2


# Creating SQLAlchemy's engine to use
# engine = create_engine('postgresql://username:password@host:socket/database')


def export_shp_postgresql(filename, srid_psql, schema, table_name, engine, geom_type, if_exists):
    try:
        gdf = gpd.read_file(filename=filename)
        wzid = re.findall(r'\d+', filename)[-1]
        gdf['wzid'] = wzid
        #     print(gdf['geometry'].geom_type)
        #     gdf.plot()
        gdf['geometry'] = [MultiLineString([feature]) if type(
            feature) == LineString else feature for feature in gdf['geometry']]

        gdf['geom'] = gdf['geometry'].apply(
            lambda x: WKTElement(x.wkt, srid=srid_psql))
        # drop the geometry column as it is now duplicative
        gdf = gdf.drop('geometry', 1)
        gdf.columns = [x.lower() for x in gdf.columns]
        # Use 'dtype' to specify column's type
        # For the geom column, we will use GeoAlchemy's type 'Geometry'
        gdf.to_sql(name=table_name, schema=schema, con=engine, if_exists=if_exists, index=False,
                   dtype={'geom': Geometry(geom_type, srid=srid_psql)})

        return True
    except:
        print("while process work zone file {}, meet some error".format(
            re.findall(r'\d+', filename)[-1]))
        return False


# geodataframe = gpd.GeoDataFrame(pd.DataFrame.from_csv('<your dataframe source>'))
# #... [do something with the geodataframe]

# geodataframe['geom'] = geodataframe['geometry'].apply(lambda x: WKTElement(x.wkt, srid=<your_SRID>)

# #drop the geometry column as it is now duplicative
# geodataframe.drop('geometry', 1, inplace=True)

# # Use 'dtype' to specify column's type
# # For the geom column, we will use GeoAlchemy's type 'Geometry'
# geodataframe.to_sql(table_name, engine, if_exists='append', index=False,
#                          dtype={'geom': Geometry('POINT', srid= <your_srid>)})


class PostgresqlDB:
    def __init__(self, config):
        db_host = config['db_host']
        db_database = config['db_database']
        db_port = config['db_port']
        db_user = config['db_user']

        self._db_connection = psycopg2.connect(
            host=db_host, database=db_database, user=db_user, port=db_port)
        self._db_cur = self._db_connection.cursor()
        self._db_cursor_dict = self._db_connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    def query(self, query, params):
        return self._db_cur.execute(query, params)

    def __del__(self):
        self._db_connection.close()


def read_config(file_name="config.yaml"):
    """Read configurations.
    Args:
        file_name (str): file name
    Returns:
        configs (dict): dictionary of configurations
    """
    with open(file_name, 'r') as f:
        config = yaml.safe_load(f)
    return config


def create_pseudo_wz(query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(numberofpseudowzs=config['numberofpseudowzs'])
    pgsql_cursor.execute(query)
    pgsql_connection.commit()


def create_pseudo_wz_divided(query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(closure_prop=config['closure_prop'],
                              duration_max=config['duration_max'],
                              duration_min=config['duration_min'],
                              wz_divided_interval=config['wz_divided_interval'],
                              spatial_pseudo=config['spatial_pseudo_table_name'])
    pgsql_cursor.execute(query)
    pgsql_connection.commit()


def extract_crash_info(query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_pseudo=config['spatial_pseudo_table_name'])
    pgsql_cursor.execute(query)
    pgsql_connection.commit()


def extract_speed_info(pseudo_info_query_loc, sqlite_join_query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(pseudo_info_query_loc, 'r') as f:
        query_tmpl = f.read().format(spatial_pseudo=config['spatial_pseudo_table_name'])
    query = query_tmpl
    pseudo_speed_loc_time = pd.read_sql(sql=query, con=pgsql_connection)
    output_speed_conn = sqlite3.connect(config['output_speed_db_loc'])
    output_speed_c = output_speed_conn.cursor()
    output_speed_c.execute(
        """ATTACH DATABASE '{}' as speed_db;""".format(config['speed_db_loc']))
    output_speed_conn.commit()

    # save data on sqlite db
    pseudo_speed_loc_time.to_sql(
        name=config['spatial_speed_table_name'], con=output_speed_conn, index=False, if_exists='replace')
    # create index
    output_speed_c.execute("""drop index if exists wzsensID;""")
    output_speed_conn.commit()

    output_speed_c.execute(
        """create index wzsensID on {}(series,control,sequence_num,wztime_divided_stamp_controlled);""".format(
            config['spatial_speed_table_name']))
    output_speed_conn.commit()

    # # join speed data
    with open(sqlite_join_query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_speed_table_output_name=config['spatial_speed_table_output_name'],
                              spatial_speed_table_name=config['spatial_speed_table_name'])

    output_speed_c.execute('drop table if exists {};'.format(
        config['spatial_speed_table_output_name']))
    output_speed_conn.commit()

    output_speed_c.execute(query)
    output_speed_conn.commit()
    # # export info to postgresql
    pgsql_cursor.execute('drop table if exists workzone.{};'.format(
        config['spatial_speed_table_output_name']))
    pgsql_connection.commit()

    for pdchunk in pd.read_sql(
            sql="SELECT * FROM {} where real_speed_61 is not null;".format(config['spatial_speed_table_output_name']),
            con=output_speed_conn, chunksize=5000):
        pdchunk.to_sql(name=config['spatial_speed_table_output_name'],
                       schema='workzone', con=engine_post, if_exists='append', index=False)
    output_speed_conn.close()


def extract_speed_info_wzsens(pseudo_info_query_loc, sqlite_join_query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(pseudo_info_query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl
    pseudo_speed_loc_time = pd.read_sql(sql=query, con=pgsql_connection)
    output_speed_conn = sqlite3.connect(config['output_speed_db_loc'])
    output_speed_c = output_speed_conn.cursor()
    output_speed_c.execute(
        """ATTACH DATABASE '{}' as speed_db;""".format(config['speed_db_loc']))
    output_speed_conn.commit()

    # save data on sqlite db
    pseudo_speed_loc_time.to_sql(
        name=config['spatial_speed_table_name'], con=output_speed_conn, index=False, if_exists='replace')
    # create index
    output_speed_c.execute("""drop index if exists wzsensID;""")
    output_speed_conn.commit()

    output_speed_c.execute(
        """create index wzsensID on {}(wzid,control,sequence_num,wztime_divided_stamp_controlled);""".format(
            config['spatial_speed_table_name']))
    output_speed_conn.commit()

    # # join speed data
    with open(sqlite_join_query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_speed_table_output_name=config['spatial_speed_table_output_name'],
                              spatial_speed_table_name=config['spatial_speed_table_name'])

    output_speed_c.execute('drop table if exists {};'.format(
        config['spatial_speed_table_output_name']))
    output_speed_conn.commit()

    output_speed_c.execute(query)
    output_speed_conn.commit()
    # # export info to postgresql
    pgsql_cursor.execute('drop table if exists workzone.{};'.format(
        config['spatial_speed_table_output_name']))
    pgsql_connection.commit()

    for pdchunk in pd.read_sql(
            sql="SELECT * FROM {} where real_speed_61 is not null;".format(config['spatial_speed_table_output_name']),
            con=output_speed_conn, chunksize=5000):
        pdchunk.to_sql(name=config['spatial_speed_table_output_name'],
                       schema='workzone', con=engine_post, if_exists='append', index=False)
    output_speed_conn.close()


def extract_weather_info_wzsens(pseudo_info_query_loc, sqlite_weather_join_query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    output_weather_conn = sqlite3.connect(config['output_speed_db_loc'])
    output_weather_c = output_weather_conn.cursor()

    output_weather_c.execute(
        'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/weather/weather.db" AS weather_db')
    output_weather_conn.commit()

    # new weather pseudo data
    with open(pseudo_info_query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl
    pseudo_speed_loc_time = pd.read_sql(sql=query, con=pgsql_connection)

    # save data on sqlite db
    pseudo_speed_loc_time.to_sql(
        name=config['spatial_weather_table_name'], con=output_weather_conn, index=False, if_exists='replace')
    # create index
    output_weather_c.execute("""drop index if exists wzsensID_weather;""")
    output_weather_conn.commit()

    output_weather_c.execute(
        """create index wzsensID_weather on {}(series,control,sequence_num,wztime_divided_stamp_controlled);""".format(
            config['spatial_weather_table_name']))
    output_weather_conn.commit()
    # end

    with open(sqlite_weather_join_query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_weather_table_output_name=config['spatial_weather_table_output_name'],
                              spatial_weather_table_name=config['spatial_weather_table_name'])

    output_weather_c.execute('drop table if exists {};'.format(
        config['spatial_weather_table_output_name']))
    output_weather_conn.commit()

    output_weather_c.execute(query)
    output_weather_conn.commit()

    pgsql_cursor.execute('drop table if exists workzone.{};'.format(config['spatial_weather_table_output_name']))
    pgsql_connection.commit()

    for pdchunk in pd.read_sql(
            sql="SELECT * FROM {} where AveT is not null;".format(config['spatial_weather_table_output_name']),
            con=output_weather_conn, chunksize=5000):
        pdchunk.to_sql(name=config['spatial_weather_table_output_name'],
                       schema='workzone', con=engine_post, if_exists='append', index=False)
    output_weather_conn.close()


def extract_weather_info(sqlite_weather_join_query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    output_weather_conn = sqlite3.connect(config['output_speed_db_loc'])
    output_weather_c = output_weather_conn.cursor()

    output_weather_c.execute(
        'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/weather/weather.db" AS weather_db')
    output_weather_conn.commit()

    with open(sqlite_weather_join_query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_weather_table_output_name=config['spatial_weather_table_output_name'],
                              spatial_speed_table_name=config['spatial_speed_table_name'])

    output_weather_c.execute('drop table if exists {};'.format(
        config['spatial_weather_table_output_name']))
    output_weather_conn.commit()

    output_weather_c.execute(query)
    output_weather_conn.commit()

    pgsql_cursor.execute('drop table if exists workzone.{};'.format(config['spatial_weather_table_output_name']))
    pgsql_connection.commit()

    for pdchunk in pd.read_sql(
            sql="SELECT * FROM {} where AveT is not null;".format(config['spatial_weather_table_output_name']),
            con=output_weather_conn, chunksize=5000):
        pdchunk.to_sql(name=config['spatial_weather_table_output_name'],
                       schema='workzone', con=engine_post, if_exists='append', index=False)
    output_weather_conn.close()


def extract_speedlimit_AADT_info(query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_pseudo=config['spatial_pseudo_table_name'])
    pgsql_cursor.execute(query)
    pgsql_connection.commit()
    pgsql_connection.close()


def extract_numofinters_info(query_loc, config):
    '''
    Input: 
    Action: 
    '''
    db_instance = PostgresqlDB(config)
    pgsql_connection = db_instance._db_connection
    pgsql_cursor = db_instance._db_cur

    with open(query_loc, 'r') as f:
        query_tmpl = f.read()
    query = query_tmpl.format(spatial_pseudo_wz_info=config['spatial_pseudo_wz_info_table_name'])
    pgsql_cursor.execute(query)
    pgsql_connection.commit()
    pgsql_connection.close()


def join_feature_tables(query_loc, config):
    ''' 
    Input:  query location to join all feature tables
            and name of output table
    Action: creates output_table based on query
    Output: string location of output_table
    '''
    db_instance = PostgresqlDB(config)
    pgsql_cursor = db_instance._db_cur
    pgsql_connection = db_instance._db_connection

    with open(query_loc, 'r') as f:
        query_tmpl = f.read()

    query = query_tmpl.format(pseudo_output_table=config['pseudo_output_table'])
    pgsql_cursor.execute(query)
    pgsql_connection.commit()
    pgsql_connection.close()
