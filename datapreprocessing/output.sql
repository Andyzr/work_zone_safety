--sql
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_weather_1117.db" AS output_weather;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_speed_1117.db" AS output_speed;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_crash_1117.db" AS output_crash;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_info_1117.db" AS output_info;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_weather_1117.db" AS output_15weather;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_speed_1117.db" AS output_15speed;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_crash_1117.db" AS output_15crash;
ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_info_1117.db" AS output_15info;

SELECT wzs_info.*,
       wzs_info.wzID as wzID_new,
       output_15weather.output_weather.AveT,
       output_15weather.output_weather.AveP,
       output_15weather.output_weather.AveW,
       output_15speed.speed_xy_61.real_speed_61,
       output_15speed.speed_xy_61.historical_speed_61,
       output_15speed.speed_xy_61.free_speed_61,
       output_15speed.speed_xy_518.real_speed_518,
       output_15speed.speed_xy_518.historical_speed_518,
       output_15speed.speed_xy_518.free_speed_518,
       output_15crash.crash_xy_61.crash_61,
       output_15crash.crash_xy_61.crash_severe_61,
       output_15crash.crash_xy_518.crash_518,
       output_15crash.crash_xy_518.crash_severe_518
FROM output_15info.wzs_info

         LEFT JOIN
     output_15weather.output_weather
     ON
                 output_15info.wzs_info.wzID = output_15weather.output_weather.wzID
             AND
                 output_15info.wzs_info.wzTime_divided_stamp = output_15weather.output_weather.wzTime_divided_stamp

         LEFT JOIN
     output_15speed.speed_xy_61
     ON
                 output_15info.wzs_info.wzID = output_15speed.speed_xy_61.wzID
             AND
                 output_15info.wzs_info.wzTime_divided_stamp = output_15speed.speed_xy_61.wzTime_divided_stamp
             AND
                 output_15info.wzs_info.location = output_15speed.speed_xy_61.location


         LEFT JOIN
     output_15speed.speed_xy_518
     ON
                 output_15info.wzs_info.wzID = output_15speed.speed_xy_518.wzID
             AND
                 output_15info.wzs_info.wzTime_divided_stamp = output_15speed.speed_xy_518.wzTime_divided_stamp
             AND
                 output_15info.wzs_info.location = output_15speed.speed_xy_518.location

         LEFT JOIN
     output_15crash.crash_xy_61
     ON
                 output_15info.wzs_info.wzID = output_15crash.crash_xy_61.wzID
             AND
                 output_15info.wzs_info.wzTime_divided_stamp = output_15crash.crash_xy_61.wzTime_divided_stamp
             AND
                 output_15info.wzs_info.location = output_15crash.crash_xy_61.location

         LEFT JOIN
     output_15crash.crash_xy_518
     ON
                 output_15info.wzs_info.wzID = output_15crash.crash_xy_518.wzID
             AND
                 output_15info.wzs_info.wzTime_divided_stamp = output_15crash.crash_xy_518.wzTime_divided_stamp
             AND
                 output_15info.wzs_info.location = output_15crash.crash_xy_518.location;