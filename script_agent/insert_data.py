import sqlite3
import time
#分析文本数据插入sqlite数据库

DB_FILE = '/Users/leimin/flask_project/Flask-Monitor-Report/app/data.sqlite'
SYS_TEXT = 'system_info_'+ time.strftime("%Y%m%d", time.localtime())+'.txt'

class parseText:
    #解析系统文本文件，生成入库脚本
    def parseSysText(self):
        sql_list = ['']
        with open(SYS_TEXT) as f:
            lists = [line.split('|') for line in f.readlines()]
            for lis in lists:
                if lis[3] == 'cpu':
                    cpu_sql = """ insert into sys_info('user_use','sys_use','io_use','idle_use','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1])
                    sql_list.append(cpu_sql)

                elif lis[3] == 'mem':
                    mem_sql = """ insert into sys_info('mem_use','mem_free','mem_buffer','mem_total','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[6],lis[7],lis[1],lis[-1])
                    sql_list.append(mem_sql)

                elif lis[3] == 'disk':
                    disk_sql = """ insert into sys_info('lun_name','lun_use','lun_size','host_ip','record_time') values ('%s','%s','%s','%s','%s')"""\
                    %(lis[4],lis[5],lis[6],lis[1],lis[-1])
                    sql_list.append(disk_sql)

                else:
                    pass
        return sql_list




class insertData:

    #初始化数据链接定义游标
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    #执行相关脚本
    def executesql(self,sql_list):
        for sql in sql_list:
            self.cur.execute(sql)
            self.conn.commit()

    #析构,关闭链接
    def __del__(self):
        print("链接关闭，操作完成。")
        self.conn.close()

if __name__ == '__main__':
    sys1 = parseText()
    inse1 = insertData()
    inse1.executesql(sys1.parseSysText())
