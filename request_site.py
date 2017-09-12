## crontab 任务执行该脚本下载数据


import requests
import datetime
import sqlite3
import time

from pyMail import mailSend
from config import config
from app.alarm_dict import alarmDict

DB_FILE = config['development'].DATABASE_URI

site_list = ['C10']
base_url = 'http://127.0.0.1:5000/site_info/download/'

class initDb:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    def getMailInfo(self):
        query_alarm_sql = """  select a.ai_node_name,a.ai_object_name,a.ai_scene_name,a.ai_time,a.ai_last_alarm_time,b.user_mail,b.user_site_id,a.site_id from site_alarm a , user_info b where a.ai_level='4' and send_mail='0'"""
        self.datas = self.cur.execute(query_alarm_sql).fetchall()
        for data in self.datas:
            if data[-2] is not None:
                content = """
                {site_id}局点---告警信息
                告警节点:{ai_node_name}
                告警对象:'{ai_object_name}'
                告警场景:'{ai_scene}'
                首次告警时间:'{ai_time}'
                最近告警时间:'{ai_last_alarm_time}'
                """.format(ai_node_name=data[0],site_id=data[-1], ai_object_name=alarmDict[data[1]],
                        ai_scene=alarmDict[data[2]], ai_time=data[3], ai_last_alarm_time=data[4])

                mail = mailSend()
                subject = "{site_id}局点---告警信息".format(site_id=data[-1])
                mail.mailMsg('andy.lei@taiway.net', data[-3], subject, content)
                mail.mailsend()
                update_alarm_sql = """update site_alarm set send_mail='1' where(ai_node_name='{ai_node_name}' and ai_object_name='{ai_object_name}'and ai_time='{ai_time}' and ai_last_alarm_time='{ai_last_alarm_time}' and site_id='{site_id}') """.format(
                    ai_node_name=data[0],ai_object_name=data[1],ai_time=data[3],ai_last_alarm_time=data[4],site_id=data[-1]
                )
                self.cur.execute(update_alarm_sql)
                self.conn.commit()
                time.sleep(10)
            else:
                pass

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    for site in site_list:
        url = base_url+site
        r = requests.get(url)
        if r.text == u'文件已下载':
            print(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")+"--"+site+" 数据更新成功")
    db = initDb()
    db.getMailInfo()