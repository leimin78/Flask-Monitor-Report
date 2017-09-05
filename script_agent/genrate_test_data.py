import time,datetime
import random,sqlite3

#生成测试用数据

DB_FILE = '/Users/leimin/flask_project/Flask-Monitor-Report/app/data.sqlite'
IP_LIST = ['192.168.0.35','192.168.0.36','192.168.0.37','192.168.0.38','192.168.0.10',
           '192.168.0.11','192.168.0.12','192.168.0.13','192.168.0.14','192.168.0.15',
           '192.168.0.16']
#生成每天的时间列表

def setTimeList():
    #将时间转换成秒,默认时间为 20170904000000
    time_list = []
    d = datetime.datetime.strptime('20170904000000', "%Y%m%d%H%M%S")
    s = time.mktime(d.timetuple())
    for i in range(1,86401,120):
        record_time = time.strftime("%Y%m%d%H%M%S",time.localtime(s))
        time_list.append(record_time)
        s += 120
        print(s)
    return time_list

time_list = setTimeList()

class insertData:
    #初始化数据链接定义游标
    def __init__(self):
        print("数据库链接初始化..数据写入中.")
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    def executesql(self, sql_list):
        print("测试数据初始化")
        for sql in sql_list:
            self.cur.execute(sql)
            self.conn.commit()

    def __del__(self):
        print("数据初始完成..")
        self.conn.close()

class testData:
    def __init__(self):
        print("测试数据开始初始化")
        self.sql_list = []

    #初始化cpu信息
    def initCpu(self,hostip):
        for time in time_list:
            user_use = random.randint(1,100)
            sys_use = random.randint(1,100)
            io_use = random.randint(1,100)
            idle_use = random.randint(1,100)
            hostip = hostip
            record_time = time
            cpu_sql = """ insert into sys_info('user_use','sys_use','io_use','idle_use','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')"""\
            %(user_use,sys_use,io_use,idle_use,hostip,record_time)
            self.sql_list.append(cpu_sql)

    def initMem(self,hostip):
        for time in time_list:
            mem_use = random.randint(1,8)
            mem_total = 8
            mem_free = random.randint(1,2)
            mem_buffer = random.randint(1,4)
            mem_sql = """ insert into sys_info('mem_use','mem_free','mem_buffer','mem_total','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')""" \
            %(mem_use,mem_free,mem_buffer,mem_total,hostip,time)
            self.sql_list.append(mem_sql)

    def initDisk(self,hostip):
        for time in time_list:
            lun_name = random.choice(['/','/home'])
            lun_use = random.randint(1,300)
            lun_size = 300
            lun_rate = round(lun_use/lun_size,2)
            hostip = hostip
            disk_sql = """ insert into sys_info('lun_name','lun_use','lun_size','lun_rate','host_ip','record_time') values ('%s','%s','%s','%s','%s','%s')""" \
            %(lun_name,lun_use,lun_size,lun_rate,hostip,time)
            self.sql_list.append(disk_sql)

    def initBase(self,hostip):
        for time in time_list:
            system_version = 'SUSE Linux Enterprise Server  11 x86_64'
            server_uptime = '68 days, 10:19:30'
            hostip = hostip
            record_time = time
            base_sql = """ insert into sys_info('system_version','server_uptime','host_ip','record_time') values('%s','%s','%s','%s')""" \
            %(system_version,server_uptime,hostip,record_time)
            self.sql_list.append(base_sql)

if __name__ == '__main__':
    db = insertData()
    test = testData()
    for hostip in IP_LIST:
        test.initBase(hostip)
        test.initCpu(hostip)
        test.initMem(hostip)
        test.initDisk(hostip)
    db.executesql(test.sql_list)