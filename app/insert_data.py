import sqlite3
import pymysql
import time
import datetime
#分析文本数据写入sqlite数据库

from config import config
DB_FILE = config['development'].DATABASE_URI

class parseText:
    #解析系统文本文件，生成入库脚本
    def parseSysText(self,SYS_TEXT):
        start_time = datetime.datetime.now()
        sql_list = []
        query_list = []
        result_list = []
        try:
            with open(SYS_TEXT) as f:
                lists = [line.split('|') for line in f.readlines()[:-1]]
                for lis in lists:
                    if lis[3] == 'cpu':
                        print(lis)
                        cpu_sql = """ insert into sys_info(user_use,sys_use,io_use,idle_use,host_ip,record_time) values ('%s','%s','%s','%s','%s','%s')""" \
                                  % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        cpu_query_sql = """ select * from sys_info where (user_use='%s' and sys_use='%s' and io_use='%s' and idle_use='%s' and host_ip='%s' and record_time='%s')""" \
                                        % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))
                        sql_list.append(cpu_sql)
                        query_list.append(cpu_query_sql)

                    elif lis[3] == 'mem':
                        mem_sql = """ insert into sys_info(mem_use,mem_free,mem_buffer,mem_total,host_ip,record_time) values ('%s','%s','%s','%s','%s','%s')""" \
                                  % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        mem_qury_sql = """ select * from sys_info where (mem_use='%s' and mem_free='%s' and mem_buffer='%s' and mem_total='%s' and host_ip = '%s' and record_time='%s')""" \
                                       % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))
                        sql_list.append(mem_sql)
                        query_list.append(mem_qury_sql)

                    elif lis[3] == 'disk':
                        disk_sql = """ insert into sys_info(lun_name,lun_use,lun_size,lun_rate,host_ip,record_time) values ('%s','%s','%s','%s','%s','%s')""" \
                                   % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        disk_query_sql = """ select * from sys_info where(lun_name='%s' and lun_use='%s' and lun_size='%s' and lun_rate='%s' and host_ip='%s' and record_time='%s') """ \
                                         % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        sql_list.append(disk_sql)
                        query_list.append(disk_query_sql)

                    elif lis[3] == 'base':
                        base_sql = """ insert into sys_info(system_version,server_uptime,host_ip,record_time) values('%s','%s','%s','%s')""" \
                                   % (lis[4], lis[5], lis[1], lis[-1].strip('\n'))

                        base_query_sql = """select * from sys_info where (system_version='%s' and server_uptime='%s' and host_ip='%s' and record_time='%s')""" \
                                         % (lis[4], lis[5], lis[1], lis[-1].strip('\n'))

                        sql_list.append(base_sql)
                        query_list.append(base_query_sql)

                    elif lis[3] == 'run':
                        run_sql = """ insert into sys_info(run_node_name,host_ip,record_time) values('%s','%s','%s')"""\
                        %(lis[4],lis[1],lis[-1].strip('\n'))

                        run_query_sql = """select * from sys_info where (run_node_name='%s' and host_ip='%s' and record_time='%s')"""\
                        %(lis[4],lis[1],lis[-1].strip('\n'))

                        sql_list.append(run_sql)
                        query_list.append(run_query_sql)

                    else:
                        pass
            result_list.append(sql_list)
            result_list.append(query_list)
        except FileNotFoundError as e:
            print(e.strerror)
            print("系统信息文件不存在！")
        end_time = datetime.datetime.now()
        print("耗时{runtime}s".format(runtime=(end_time-start_time).seconds))
        return result_list

    def parseAlarmReportText(self,ALARM_REPORT_TEXT):
        sql_list = []
        query_list = []
        result_list = []
        try:
            with open(ALARM_REPORT_TEXT) as f:
                lists = [line.split('|') for line in f.readlines()[:-1]]
                for lis in lists:
                    if lis[1] == 'report':
                        report_sql = """ insert into site_report(pk_ds_day,pk_ds_stat_type,ds_num,site_id) values('%s','%s','%s','%s')"""\
                        %(lis[2],lis[3],lis[4].strip('\n'),lis[0])

                        report_query_sql = """select * from site_report where(pk_ds_day='%s' and pk_ds_stat_type='%s' and ds_num='%s'and site_id='%s')"""\
                        % (lis[2], lis[3], lis[4].strip('\n'), lis[0])
                        sql_list.append(report_sql)
                        query_list.append(report_query_sql)

                    elif lis[1] == 'alarm':
                        alarm_sql = """ insert into site_alarm(ai_node_name,ai_object_name,ai_scene_name,ai_time,ai_last_alarm_time,ai_level,site_id,send_mail) values('%s','%s','%s','%s','%s','%s','%s','0')"""\
                        %(lis[2],lis[3],lis[4],lis[5],lis[6],lis[7].strip('\n'),lis[0])

                        alarm_query_sql = """select * from site_alarm where(ai_node_name='%s' and ai_object_name='%s' and ai_scene_name='%s' and ai_time='%s' and ai_last_alarm_time='%s' and ai_level='%s' and site_id='%s' )""" \
                        % (lis[2], lis[3], lis[4], lis[5], lis[6], lis[7].strip('\n'), lis[0])
                        sql_list.append(alarm_sql)
                        query_list.append(alarm_query_sql)
            result_list.append(sql_list)
            result_list.append(query_list)
        except FileNotFoundError as e:
            print(e.strerror)
            print("告警信息文件不存在！")
        return result_list

    #分析文本生成服务器脚本
    def parseSiteServer(self,SYS_TEXT):
        sql_list = []
        query_list = []
        result_list = []
        site_server = {}
        site_id = ''
        try:
            with open(SYS_TEXT) as f:
                lists = [line.split('|') for line in f.readlines()[:-1]]
                for lis in lists:
                    site_server[lis[0]] = lis[1]
                    site_id = lis[2]
                for key in site_server:
                    site_server_sql = """ insert into server_info(server_name,server_ip,server_site_id) values('%s','%s','%s')"""\
                    %(key,site_server[key],site_id)

                    site_server_query_sql = """select * from server_info where (server_name='%s' and server_ip='%s' and server_site_id='%s')"""\
                    %(key,site_server[key],site_id)
                    sql_list.append(site_server_sql)
                    query_list.append(site_server_query_sql)
            result_list.append(sql_list)
            result_list.append(query_list)
        except FileNotFoundError as e:
            print(e.strerror)
            print("服务器信息文件不存在！")
        return result_list

class insertData:
    #初始化数据链接定义游标
    def __init__(self):
        self.start_time = datetime.datetime.now()
        print("数据库链接初始化..数据写入中.")
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    #执行相关脚本
    def executesql(self,sql_list,query_list):
        for index, query_sql in enumerate(query_list):
            # 如果存在相同数据则不写入
            if self.cur.execute(query_sql).fetchall():
                pass
            # print("存在相同数据不写入")
            else:
                try:
                    self.cur.execute(sql_list[index])
                    self.conn.commit()
                except Exception:
                    continue


class insertDataMysql:
    #初始化数据连接定义游标
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.conn = pymysql.connect('localhost', 'root', '', 'test')
        print("数据库链接初始化..数据写入中.")
        self.cur = self.conn.cursor()

    def executesql(self,sql_list,query_list):
        for index, query_sql in enumerate(query_list):
            if self.cur.execute(query_sql)!=0:
                print("存在相同数据不写入")
            else:
                try:
                    print("正在执行语句"+sql_list[index])
                    self.cur.execute(sql_list[index])
                    self.conn.commit()
                except Exception:
                    continue

    #析构,关闭链接
    def __del__(self):
        self.end_time = datetime.datetime.now()
        print("共耗时{runtime}".format(runtime=(self.end_time-self.start_time).seconds))
        print("链接关闭，操作完成。")
        self.conn.close()
