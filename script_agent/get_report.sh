#!/bin/bash

TODAY=$(date +%Y%m%d)
SEVEN_DAY_AGO=$(date -d '7 day ago' +%Y%m%d)
SEVEN_DAY_AGO_ALARM=$(date -d '7 day ago' +%Y%m%d%H%M%S)
FILE_PATH='/home/oracle/c10_report'
SITE_ID='C10'
DB_USER='cstaitechdb'
DB_PASS='huawei123'

report_sql=" select pk_ds_day||'|'||pk_ds_stat_type||'|'||ds_num from com_day_stat where pk_ds_stat_type in ('13001','13002','13003','13027','13017','13009','13087','13018','13088','13007','13008','13300','13301','13302','13303','13308','13225')
and pk_ds_day >= $SEVEN_DAY_AGO order by pk_ds_day;"

echo $report_sql
sqlplus -s ${DB_USER}/${DB_PASS} > ${FILE_PATH}/report_${TODAY}_${SITE_ID}.txt<<EOF
set heading off;
set pages 0;
set feed off;
$report_sql
EOF

alarm_sql="select ai_node_name||'|'||ai_object_name||'|'||ai_scene_name||'|'||
ai_time||'|'||ai_last_alarm_time||'|'||ai_level from com_alarm_info where (ai_recover_time=' ' or ai_recover_time='')
order by ai_time;"

echo alarm_sql
sqlplus -s ${DB_USER}/${DB_PASS} > ${FILE_PATH}/alarm_${TODAY}_${SITE_ID}.txt<<EOF
set heading off;
set pages 0;
set feed off;
set line 300;
$alarm_sql
EOF