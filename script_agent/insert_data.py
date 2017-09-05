import sqlite3
import time
#分析文本数据插入sqlite数据库

DB_FILE = '/Users/leimin/flask_project/Flask-Monitor-Report/app/data.sqlite'
SYS_TEXT = 'system_info_'+ time.strftime("%Y%m%d", time.localtime())+'.txt'


class parseText:
    #解析系统文本文件，生成入库脚本
    def parseSysText(self):
        sql_list = []
        query_list = []
        result_list = []
        with open(SYS_TEXT) as f:
            lists = [line.split('|') for line in f.readlines()]
            for lis in lists:
                if lis[3] == 'cpu':
                    cpu_sql = """ insert into sys_info('user_use','sys_use','io_use','idle_use','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1].strip('\n'))

                    cpu_query_sql = """ select * from sys_info where (user_use='%s' and sys_use='%s' and io_use='%s' and idle_use='%s' and host_ip='%s' and record_time='%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1].strip('\n'))
                    sql_list.append(cpu_sql)
                    query_list.append(cpu_query_sql)

                elif lis[3] == 'mem':
                    mem_sql = """ insert into sys_info('mem_use','mem_free','mem_buffer','mem_total','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1].strip('\n'))

                    mem_qury_sql = """ select * from sys_info where (mem_use='%s' and mem_free='%s' and mem_buffer='%s' and mem_total='%s' and host_ip = '%s' and record_time='%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1].strip('\n'))
                    sql_list.append(mem_sql)
                    query_list.append(mem_qury_sql)

                elif lis[3] == 'disk':
                    disk_sql = """ insert into sys_info('lun_name','lun_use','lun_size','lun_rate','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1].strip('\n'))

                    disk_query_sql = """ select * from sys_info where(lun_name='%s' and lun_use='%s' and lun_size='%s' and lun_rate='%s' and host_ip='%s' and record_time='%s') """\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1].strip('\n'))

                    sql_list.append(disk_sql)
                    query_list.append(disk_query_sql)

                elif lis[3] == 'base':
                    base_sql = """ insert into sys_info('system_version','server_uptime','host_ip','record_time') values('%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[1],lis[-1].strip('\n'))

                    base_query_sql = """select * from sys_info where (system_version='%s' and server_uptime='%s' and host_ip='%s' and record_time='%s')"""\
                    %(lis[4],lis[5],lis[1],lis[-1].strip('\n'))

                    sql_list.append(base_sql)
                    query_list.append(base_query_sql)

                else:
                    pass

        result_list.append(sql_list)
        result_list.append(query_list)
        return result_list




class insertData:

    #初始化数据链接定义游标
    def __init__(self):
        print("数据库链接初始化..数据写入中.")
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    #执行相关脚本
    def executesql(self,sql_list,query_list):
        for index,query_sql in enumerate(query_list):
            #如果存在相同数据则不插入
            if self.cur.execute(query_sql).fetchall():
                print("存在相同数据不插入")
            else:
                self.cur.execute(sql_list[index])
                self.conn.commit()

    #析构,关闭链接
    def __del__(self):
        print("链接关闭，操作完成。")
        self.conn.close()

if __name__ == '__main__':
    sys1 = parseText()
    print(sys1.parseSysText()[1])
    inse1 = insertData()
    inse1.executesql(sys1.parseSysText()[0],sys1.parseSysText()[1])
