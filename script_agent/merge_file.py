# -*- coding:utf-8 -*-
# 支持在python2 环境下执行加入编码定义
# 对shell生成的alarm_day_site.txt 与 report_day_site.txt 进行合并
import os
import datetime
import re

basedir = os.path.abspath(os.path.dirname(__file__))
today = datetime.datetime.now().strftime('%Y%m%d')
siteid = 'C10'

#新文件名定义 siteId_alarm_report_today.txt

alarm_report_file = os.path.join(basedir,siteid+'_alarm_report_'+today)
sys_info_file = os.path.join(basedir,siteid+'_sysinfo_'+today)


try:
    with open(alarm_report_file,'a+') as f:
        pass
except FileNotFoundError:
    print("alarm_report_file 文件不存在 已创建")

try:
    with open(sys_info_file,'a+') as f:
        pass
except FileNotFoundError:
    print("sys_info_file 文件不存在 已创建")


#需要合并的文件，告警日报文本
alarm_file = os.path.join(basedir,'alarm_'+today+'_'+siteid+'.txt')
report_file = os.path.join(basedir,'report_'+today+'_'+siteid+'.txt')

#需要合并的信息文本列表
def getSysFileList():
    sys_file_list = []
    pattern = re.compile(r'system_info_'+today)
    for filename in os.listdir(basedir):
        file = pattern.match(filename)
        if file:
            sys_file_list.append(os.path.join(basedir,filename))
    return sys_file_list


#新文本格式 siteid|type|
#example C10|report|20170829|13003|1210696
#example C10|alarm|spm|alarm.objname.sas.socket|alarm.scenename.sas.gslconnerror|20170829133830|20170829133830|4
alarm_new_line = siteid+'|'+'alarm'+'|'
report_new_line = siteid+'|'+'report'+'|'

def mergeAlarmFile():
    #告警文本数据插入
    with open(alarm_file, 'r') as alarm:
        for alarm_line in alarm.readlines():
            with open(alarm_report_file, 'r+') as f:
                if alarm_new_line + alarm_line in f.readlines():
                    print("告警重复行不插入")
                else:
                    with open(alarm_report_file, 'a+') as nf:
                        nf.write(alarm_new_line + alarm_line)
        print("告警数据完成插入")

    # 日报文本插入
    with open(report_file, 'r') as report:
        for report_line in report.readlines():
            with open(alarm_report_file, 'r+') as f:
                if report_new_line + report_line in f.readlines():
                    print("日报重复行不插入")
                else:
                    with open(alarm_report_file, 'a+') as nf:
                        nf.write(report_new_line + report_line)
        print("日报数据完成插入")


def mergeSysFile():
    #系统文本插入
    for sysfile in getSysFileList():
        with open(sysfile,'r') as sysinfo:
            for sysinfo_line in sysinfo.readlines():
                with open(sys_info_file,'r+') as f:
                    if sysinfo_line in f.readlines():
                        print("系统信息数据重复不插入")
                    else:
                        with open(sys_info_file,'a+') as nf:
                            nf.write(sysinfo_line)
            print("{filename}的系统数据已插入".format(filename=sysfile))

if __name__ == '__main__':
    mergeAlarmFile()
    mergeSysFile()