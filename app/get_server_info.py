import sqlite3


DB_FILE = '/Users/leimin/flask_project/Flask-Monitor-Report/app/data.sqlite'
cpu_sql = """select * from (select rowid,user_use,sys_use,io_use,record_time from sys_info where user_use is not null) limit %d,1000"""


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
