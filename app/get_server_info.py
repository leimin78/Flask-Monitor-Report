### 该文件为sql语句及数据库相关操作

import sqlite3
import datetime
from config import config

week_time = datetime.datetime.now() - datetime.timedelta(days=7)
new_week_time = week_time.strftime("%Y%m%d%H%M%S")

DB_FILE = config['development'].DATABASE_URI

## 服务器相关语句
site_info_sql = """ select site_id,site_name from site_info group by site_id,site_name """
server_list_sql = """select server_site_id,server_name,server_ip from server_info where server_site_id='{site_id}' """
site_name_sql = """ select site_name from site_info where site_id='{site_id}' """
cpu_use_sql = """select max(rowid),round(100-idle_use,2),host_ip from sys_info where idle_use is not null group by host_ip"""
mem_use_sql = """select max(rowid),round((1-(mem_free+mem_buffer)/mem_total)*100,2),host_ip from sys_info where mem_free is not null group by host_ip"""
server_name_sql = """ select server_name from server_info where server_ip='{ip}'"""
system_info_sql = """select max(rowid),host_ip,system_version,server_uptime,record_time from sys_info where system_version is not null and host_ip='{ip}'"""
disk_info_sql = """select max(rowid),lun_name,lun_use,lun_size,lun_rate from sys_info where lun_name is not null and host_ip='{ip}' group by lun_name"""
cpu_info_list_sql = """select user_use,sys_use,io_use,idle_use,record_time from sys_info where user_use is not null and host_ip='{ip}' and record_time>='{weektime}' order by record_time """
mem_info_list_sql = """select round(1-(mem_free+mem_buffer)/mem_total,2)*100,record_time from sys_info where mem_free is not null and host_ip='{ip}' and record_time>='{weektime}' order by record_time """
run_node_list_sql = """select max(id),run_node_name,host_ip from sys_info where run_node_name is not null group by run_node_name,host_ip """

#查询各IP最新的时间
ip_maxtime_sql = """select max(id),record_time,host_ip from sys_info where run_node_name is not null group by host_ip"""

#开销户数
sub_user_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13001' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
unsub_user_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13002' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
total_user_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13027' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
charge_user_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13003' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""


#呼叫及彩印推送
call_times_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13017' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
ussd_times_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13009' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
ussd_sucess_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13087' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
flash_times_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13018' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
flash_sucess_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13088' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""

#上下行短信推送数
mo_times_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13007' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""
mt_times_sql = """select max(id),pk_ds_day,ds_num from site_report where pk_ds_stat_type='13008' and pk_ds_day >='{weektime}' and pk_ds_day < '{today}' and site_id='{site_id}' group by pk_ds_day,pk_ds_day order by pk_ds_day"""

#获取高告警信息
site_alarm_sql = """select max(id),ai_node_name,ai_object_name,ai_level,ai_scene_name,ai_time,ai_last_alarm_time,send_mail from site_alarm where site_id='{site_id}' group by ai_node_name,ai_object_name,ai_level,ai_scene_name"""

#删除告警信息
delete_alarm_sql = """delete from site_alarm where ai_last_alarm_time is not null and site_id='{site_id}' and ai_last_alarm_time<='{two_days}' """
#获取局点域名
site_domain_sql = """select site_url from site_info where site_id='{site_id}'"""

#获取维护人员相关信息
sys_user_sql = """select user_cname,user_phone,user_mail,user_site_id from user_info where user_phone is not null"""

class queryDB:
    # 初始化查询连接
    def __init__(self):
        print(DB_FILE)
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    def query_db(self, query):
        self.datas = self.cur.execute(query).fetchall()

    def delete_db(self,delsql):
        self.cur.execute(delsql)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
