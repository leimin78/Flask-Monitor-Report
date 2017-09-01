import sqlite3


DB_FILE = '/Users/leimin/flask_project/Flask-Monitor-Report/app/data.sqlite'

site_info_sql = """ select site_id,site_name from site_info group by site_id,site_name """
server_list_sql = """select server_site_id,server_name,server_ip from server_info where server_site_id='{site_id}' """
site_name_sql = """ select site_name from site_info where site_id='{site_id}' """
cpu_use_sql = """select max(rowid),round(100-idle_use,2),host_ip from sys_info where idle_use is not null group by host_ip"""
mem_use_sql = """select max(rowid),round(1-(mem_free+mem_buffer)/mem_total,2),host_ip from sys_info where mem_free is not null group by host_ip"""
server_name_sql = """ select server_name from server_info where server_ip='{ip}'"""
system_info_sql = """select max(rowid),host_ip,system_version,server_uptime,record_time from sys_info where system_version is not null and host_ip='{ip}'"""
disk_info_sql = """select max(rowid),lun_name,lun_use,lun_size,lun_rate from sys_info where lun_name is not null and host_ip='{ip}' group by lun_name"""

cpu_info_list_sql = """select user_use,sys_use,io_use,idle_use,record_time from sys_info where user_use is not null and host_ip='{ip}'"""

class queryDB:
    # 初始化查询连接
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    def query_db(self, query):
        self.datas = self.cur.execute(query).fetchall()

    def __del__(self):
        self.conn.close()

    #将数据转换为dict存入列表方便转换json数据
    def cpu_info(self):
        self.cpu = []
        d = {}
        for data in self.datas:
            d['user_use'] = data[0]
            d['sys_use'] = data[1]
            d['io_use'] = data[2]
            d['record_time'] = data[-1].strip('\n')
            self.cpu.append(d)
