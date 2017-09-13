import sqlite3
import time
import datetime
#分析文本数据写入sqlite数据库

DB_FILE = '/Users/leimin/flask_project/Flask-Monitor-Report/app/data.sqlite'
SYS_TEXT = 'system_info_'+ time.strftime("%Y%m%d", time.localtime())+'.txt'
ALARM_REPORT_TEXT = 'alarm_report_'+ time.strftime("%Y%m%d", time.localtime())+'.txt'

class parseText:
    #解析系统文本文件，生成入库脚本
    def parseSysText(self):
        start_time = datetime.datetime.now()
        sql_list = []
        query_list = []
        result_list = []
        try:
            with open(SYS_TEXT) as f:
                lists = [line.split('|') for line in f.readlines()]
                for lis in lists:
                    if lis[3] == 'cpu':
                        cpu_sql = """ insert into sys_info('user_use','sys_use','io_use','idle_use','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')""" \
                                  % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        cpu_query_sql = """ select * from sys_info where (user_use='%s' and sys_use='%s' and io_use='%s' and idle_use='%s' and host_ip='%s' and record_time='%s')""" \
                                        % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))
                        sql_list.append(cpu_sql)
                        query_list.append(cpu_query_sql)

                    elif lis[3] == 'mem':
                        mem_sql = """ insert into sys_info('mem_use','mem_free','mem_buffer','mem_total','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')""" \
                                  % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        mem_qury_sql = """ select * from sys_info where (mem_use='%s' and mem_free='%s' and mem_buffer='%s' and mem_total='%s' and host_ip = '%s' and record_time='%s')""" \
                                       % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))
                        sql_list.append(mem_sql)
                        query_list.append(mem_qury_sql)

                    elif lis[3] == 'disk':
                        disk_sql = """ insert into sys_info('lun_name','lun_use','lun_size','lun_rate','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')""" \
                                   % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        disk_query_sql = """ select * from sys_info where(lun_name='%s' and lun_use='%s' and lun_size='%s' and lun_rate='%s' and host_ip='%s' and record_time='%s') """ \
                                         % (lis[4], lis[5], lis[6], lis[7], lis[1], lis[-1].strip('\n'))

                        sql_list.append(disk_sql)
                        query_list.append(disk_query_sql)

                    elif lis[3] == 'base':
                        base_sql = """ insert into sys_info('system_version','server_uptime','host_ip','record_time') values('%s','%s','%s','%s')""" \
                                   % (lis[4], lis[5], lis[1], lis[-1])

                        base_query_sql = """select * from sys_info where (system_version='%s' and server_uptime='%s' and host_ip='%s' and record_time='%s')""" \
                                         % (lis[4], lis[5], lis[1], lis[-1])

                        sql_list.append(base_sql)
                        query_list.append(base_query_sql)

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

    def parseAlarmReportText(self):
        sql_list = []
        query_list = []
        result_list = []
        try:
            with open(ALARM_REPORT_TEXT) as f:
                lists = [line.split('|') for line in f.readlines()]
                for lis in lists:
                    if lis[1] == 'report':
                        report_sql = """ insert into site_report(pk_ds_day,pk_ds_stat_type,ds_num,site_id) values('%s','%s','%s','%s')"""\
                        %(lis[2],lis[3],lis[4].strip('\n'),lis[0])

                        report_query_sql = """select * from site_report where(pk_ds_day='%s' and pk_ds_stat_type='%s' and ds_num='%s'and site_id='%s')"""\
                        % (lis[2], lis[3], lis[4].strip('\n'), lis[0])
                        sql_list.append(report_sql)
                        query_list.append(report_query_sql)

                    elif lis[1] == 'alarm':
                        alarm_sql = """ insert into site_alarm(ai_node_name,ai_object_name,ai_scene_name,ai_time,ai_last_alarm_time,ai_level,site_id) values('%s','%s','%s','%s','%s','%s','%s')"""\
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

class insertData:
    #初始化数据链接定义游标
    def __init__(self):
        self.start_time = datetime.datetime.now()
        print("数据库链接初始化..数据写入中.")
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    #执行相关脚本
    def executesql(self,sql_list,query_list):
        for index,query_sql in enumerate(query_list):
            #如果存在相同数据则不写入
            if self.cur.execute(query_sql).fetchall():
                pass
                #print("{i}行存在相同数据不写入".format(i=index))
            else:
                print("第{i}行数据正在写入".format(i=index))
                self.cur.execute(sql_list[index])
                self.conn.commit()

    #析构,关闭链接
    def __del__(self):
        self.end_time = datetime.datetime.now()
        print("共耗时{runtime}".format(runtime=(self.end_time-self.start_time).seconds))
        print("链接关闭，操作完成。")
        self.conn.close()

if __name__ == '__main__':
    sys1 = parseText()
    sys_insert = insertData()
    alarm_insert = insertData()
    #插入服务器相关数据
    try:
        sys_insert.executesql(sys1.parseSysText()[0],sys1.parseSysText()[1])
    except IndexError as e:
        print(e.args)
        print ("服务器信息文件不存在本次不写入数据")

    #写入报表告警相关数据
    try:
        alarm_insert.executesql(sys1.parseAlarmReportText()[0],sys1.parseAlarmReportText()[1])
    except IndexError as e:
        print(e.args)
        print("告警信息文件不存在本次不写入数据.")
