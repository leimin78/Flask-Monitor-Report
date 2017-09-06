# -*- coding:utf-8 -*-
# 支持在python2 环境下执行加入编码定义
# 对shell生成的alarm_day_site.txt 与 report_day_site.txt 进行合并
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
today = datetime.datetime.now().strftime('%Y%m%d')
siteid = 'C10'

#新文件名定义 siteId_alarm_report_today.txt

alarm_report_file = os.path.join(basedir,siteid+'_alarm_report_'+today+'.txt')

try:
    with open(alarm_report_file,'w+') as f:
        pass
except FileNotFoundError:
    print("文件不存在")
#需要合并的文件
alarm_file = os.path.join(basedir,'alarm_'+today+'_'+siteid+'.txt')
report_file = os.path.join(basedir,'report_'+today+'_'+siteid+'.txt')

#新文本格式 siteid|type|
#example C10|report|20170829|13003|1210696
#example C10|alarm|spm|alarm.objname.sas.socket|alarm.scenename.sas.gslconnerror|20170829133830|20170829133830|4
alarm_new_line = siteid+'|'+'alarm'+'|'
report_new_line = siteid+'|'+'report'+'|'

def mergeFile():
    #告警文本数据插入
    with open(alarm_file,'r') as alarm:
        for alarm_line in alarm.readlines():
            with open(alarm_report_file,'r+') as f:
                if alarm_new_line+alarm_line in f.readlines():
                    print("告警重复行不插入")
                else:
                    with open(alarm_report_file, 'a+') as nf:
                        nf.write(alarm_new_line+alarm_line)
        print("告警数据完成插入")

    #日报文本插入
    with open(report_file,'r') as report:
        for report_line in report.readlines():
            with open(alarm_report_file,'r+') as f:
                if report_new_line+report_line in f.readlines():
                    print("日报重复行不插入")
                else:
                    with open(alarm_report_file, 'a+') as nf:
                        nf.write(report_new_line+report_line)
        print("日报数据完成插入")

if __name__ == '__main__':
    mergeFile()