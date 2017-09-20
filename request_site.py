## crontab 任务执行该脚本下载数据


import requests
import datetime
import pymysql
import time
import os

from pyMail import mailSend
from config import config
from app.alarm_dict import alarmDict
from app.get_server_info_mysql import *
from app.insert_data import *

DB_FILE = config['development'].DATABASE_URI

site_list = ['C02','C26', 'C18', 'C10', 'C06', 'C05']
base_url = 'http://127.0.0.1:5000/site_info/download/'
basedir = os.path.abspath(os.path.dirname(__file__))


def siteDownload(siteid):
    # 根据局点名获取文件下载地址
    Today = datetime.datetime.now().strftime('%Y%m%d')
    db = queryDB()
    site_domain_new_sql = site_domain_sql.format(site_id=siteid)
    db.query_db(site_domain_new_sql)
    site_url = db.datas[0][0]

    # 定义需要下载的文件名及下载链接
    site_alarm_filename = siteid + '_alarm_report_' + Today
    site_sys_filename = siteid + '_sysinfo_' + Today
    site_record_filename = siteid + '_record_' + Today
    site_alarm_url = site_url + site_alarm_filename
    site_sys_url = site_url + site_sys_filename

    # 定义下载目录
    site_file_path = os.path.join(basedir, 'downloads', siteid)

    # 目录不存在则创建
    isExists = os.path.exists(site_file_path)
    if not isExists:
        os.makedirs(site_file_path)
    else:
        print("目录已存在不需要创建。")

    # 下载告警报表文件
    try:
        alarm_req = requests.get(site_alarm_url, stream=True)
        f = open(os.path.join(site_file_path, site_alarm_filename), "wb")
        for chunk in alarm_req.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
    except:
        print("网络错误")
    # 下载服务器信息文件

    try:
        sys_req = requests.get(site_sys_url, stream=True)
        f = open(os.path.join(site_file_path, site_sys_filename), "wb")
        for chunk in sys_req.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
    except:
        print("网络错误")

    # 将获取的文件插入数据库
    SYS_TEXT = os.path.join(site_file_path, site_sys_filename)
    ALARM_REPORT_TEXT = os.path.join(site_file_path, site_alarm_filename)
    RECORD_TEXT = os.path.join(site_file_path, site_record_filename)

    try:
        with open(RECORD_TEXT, 'r') as f:
            data = f.readlines()
            if len(data) != 0:
                last_len = int(data[-1].strip('\n'))
            else:
                last_len = 0
    except Exception:
        last_len = 0
        with open(RECORD_TEXT, 'a+') as f:
            print("文件不存在已创建")

    print(SYS_TEXT)
    sys1 = parseText()
    sys_insert = insertDataMysql()
    alarm_insert = insertDataMysql()
    server_insert = insertDataMysql()
    # 插入服务器相关数据
    try:
        sys_insert.executesql(sys1.parseSysText(SYS_TEXT)[0][last_len:], sys1.parseSysText(SYS_TEXT)[1][last_len:])
        with open(SYS_TEXT, 'r') as sf:
            new_last_len = len(sf.readlines())
        with open(RECORD_TEXT, 'a+') as rf:
            rf.write(str(new_last_len) + '\n')
    except IndexError as e:
        print(e.args)
        print("服务器信息文件不存在本次不写入数据")

    # 写入报表告警相关数据
    try:
        alarm_insert.executesql(sys1.parseAlarmReportText(ALARM_REPORT_TEXT)[0],
                                sys1.parseAlarmReportText(ALARM_REPORT_TEXT)[1])
    except IndexError as e:
        print(e.args)
        print("告警信息文件不存在本次不写入数据.")
    try:
        server_insert.executesql(sys1.parseSiteServer(SYS_TEXT)[0], sys1.parseSiteServer(SYS_TEXT)[1])
    except IndexError as e:
        print(e.args)
        print("服务器文件不存在本次不写入数据.")

    return "文件已下载"


class initDb:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.conn = pymysql.connect('localhost', 'root', '123456', 'csmonitor', charset='utf8')
        self.cur = self.conn.cursor()

    def getMailInfo(self):
        query_alarm_sql = """  select a.ai_node_name,a.ai_object_name,a.ai_scene_name,a.ai_time,a.ai_last_alarm_time,b.user_mail,b.user_site_id,a.site_id from site_alarm a , user_info b where a.ai_level='4' and send_mail='0'"""
        self.cur.execute(query_alarm_sql)
        self.datas = self.cur.fetchall()
        for data in self.datas:
            if data[-2] is not None:
                content = """
                {site_id}局点---告警信息
                告警节点:{ai_node_name}
                告警对象:'{ai_object_name}'
                告警场景:'{ai_scene}'
                首次告警时间:'{ai_time}'
                最近告警时间:'{ai_last_alarm_time}'
                """.format(ai_node_name=data[0], site_id=data[-1], ai_object_name=alarmDict[data[1]],
                           ai_scene=alarmDict[data[2]], ai_time=data[3], ai_last_alarm_time=data[4])

                mail = mailSend()
                subject = "{site_id}局点---告警信息".format(site_id=data[-1])
                mail.mailMsg('andy.lei@taiway.net', data[-3], subject, content)
                mail.mailsend()
                update_alarm_sql = """update site_alarm set send_mail='1' where(ai_node_name='{ai_node_name}' and ai_object_name='{ai_object_name}'and ai_time='{ai_time}' and ai_last_alarm_time='{ai_last_alarm_time}' and site_id='{site_id}') """.format(
                    ai_node_name=data[0], ai_object_name=data[1], ai_time=data[3], ai_last_alarm_time=data[4],
                    site_id=data[-1]
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
        if siteDownload(site) == u'文件已下载':
            print(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "--" + site + " 数据更新成功")
    db = initDb()
    db.getMailInfo()
