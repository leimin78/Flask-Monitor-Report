import datetime
import time
import requests
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,login_required,logout_user
from . import main
from ..models import *
from ..get_server_info import *
from ..alarm_dict import alarmDict
from .. import login_manager
from ..insert_data import *

import os

basedir = os.path.abspath(os.path.dirname(__file__))


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect('login')

@main.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname = request.form.get('uname')
        print(uname)
        user = UserInfo.query.filter_by(user_name=uname).first()
        print(user)
        if not user:
            flash('抱歉用户不存在')
            return redirect(url_for('main.login'))
        elif user.verify_password(request.form.get('pass')) == False:
            flash('抱歉密码错误')
            return redirect(url_for('main.login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('main.siteInfo'))
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出系统了.')
    return redirect(url_for('main.login'))

#局点服务器列表页面
@main.route('/site_info',methods=['GET','POST'])
@login_required
def siteInfo():
    db = queryDB()
    db.query_db(site_info_sql)
    site_info = db.datas
    return render_template('site_info.html',site_info=site_info)


#局点基本信息页面
@main.route('/server_info/<siteid>',methods=['GET','POST'])
@login_required
def serverList(siteid):
    db = queryDB()
    site_server_sql = server_list_sql.format(site_id=siteid)
    site_name_new_sql = site_name_sql.format(site_id=siteid)

    #获取局点相关的服务器列表
    db.query_db(site_server_sql)
    server_list = db.datas

    #获取局点名
    db.query_db(site_name_new_sql)
    site_name = db.datas[0][0]

    #获取最近CPU使用率
    db.query_db(cpu_use_sql)
    cpu_use_list = db.datas

    #获取最近内存使用率
    db.query_db(mem_use_sql)
    mem_use_list = db.datas

    return render_template('server_info.html',server_list=server_list,site_name=site_name,cpu_use_list=cpu_use_list,
                           mem_use_list=mem_use_list)

#服务器详细细信息页面
@main.route('/server_detail/<serverip>',methods=['GET','POST'])
@login_required
def serverDetail(serverip):

    #设置时间参数
    week_time = datetime.datetime.now() - datetime.timedelta(days=7)
    new_week_time = week_time.strftime("%Y%m%d%H%M%S")
    print(new_week_time)
    #获取主机名
    db = queryDB()
    db.query_db(server_name_sql.format(ip=serverip))
    server_name = db.datas[0][0]

    #获取，系统版本，系统运行时间信息
    db.query_db(system_info_sql.format(ip=serverip))
    sys_info = db.datas

    #获取磁盘信息
    db.query_db(disk_info_sql.format(ip=serverip))
    disk_info = db.datas

    #获取cpu列表信息
    print(cpu_info_list_sql.format(ip=serverip,weektime=new_week_time))
    db.query_db(cpu_info_list_sql.format(ip=serverip,weektime=new_week_time))
    cpu_info_list = db.datas

    cpu_user = [x[0] for x in cpu_info_list]
    cpu_system = [x[1] for x in cpu_info_list]
    cpu_io = [x[2] for x in cpu_info_list]
    cpu_idle = [x[3] for x in cpu_info_list]
    cpu_time = [x[4].strip('\n') for x in cpu_info_list]
    new_cpu_time = []
    for cputime in cpu_time:
        local = time.mktime(time.strptime(cputime, "%Y%m%d%H%M%S"))
        new_cpu_time.append(time.strftime("%Y%m%d-%H:%M:%S",time.localtime(local)))



    #获取内存列表信息
    db.query_db(mem_info_list_sql.format(ip=serverip,weektime=new_week_time))
    mem_info_list = db.datas

    mem_use = [x[0] for x in mem_info_list]
    mem_time = [x[1] for x in mem_info_list]
    new_mem_time = []
    for memtime in mem_time:
        local1 = time.mktime(time.strptime(memtime, "%Y%m%d%H%M%S"))
        new_mem_time.append(time.strftime("%Y%m%d-%H:%M:%S",time.localtime(local1)))

    return render_template('server_detail.html',
                           server_name=server_name,
                           sys_info=sys_info,
                           disk_info=disk_info,
                           cpu_user=cpu_user,
                           cpu_system = cpu_system,
                           cpu_io = cpu_io,
                           cpu_idle = cpu_idle,
                           new_cpu_time = new_cpu_time,
                           mem_use = mem_use,
                           new_mem_time = new_mem_time
                           )


@main.route('/site_info/report/<siteid>',methods=["GET","POST"])
@login_required
def siteReport(siteid):

    #获取局点名
    db = queryDB()
    site_name_new_sql = site_name_sql.format(site_id=siteid)
    db.query_db(site_name_new_sql)
    site_name = db.datas[0][0]

    #获取报表数据
    # 设置时间参数
    week_time = datetime.datetime.now() - datetime.timedelta(days=7)
    new_week_time = week_time.strftime("%Y%m%d")
    today = datetime.datetime.now().strftime("%Y%m%d")

    #获取开户数
    db.query_db(sub_user_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    sub_user_list = db.datas
    sub_user = [ int(x[1]) for x in sub_user_list ]
    day_time = [ int(x[0]) for x in sub_user_list ]

    #获取销户数
    db.query_db(unsub_user_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    unsub_user_list = db.datas
    unsub_user = [ int(x[1]) for x in unsub_user_list ]

    #获取总用户数
    db.query_db(total_user_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    total_user_list = db.datas
    total_user = [ int(x[1]) for x in total_user_list ]

    #获取收费用户数
    db.query_db(charge_user_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    charge_user_list = db.datas
    charge_user = [ int(x[1]) for x in charge_user_list ]


    #呼叫次数
    db.query_db(call_times_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    call_times_list = db.datas
    call_times = [ int(x[1]) for x in call_times_list ]

    #USSD发送次数
    db.query_db(ussd_times_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    ussd_times_list = db.datas
    ussd_times = [ int(x[1]) for x in ussd_times_list ]

    #USSD发送成功数
    db.query_db(ussd_sucess_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    ussd_sucess_list = db.datas
    ussd_sucess = [ int(x[1]) for x in ussd_sucess_list ]

    #闪信发送次数
    db.query_db(flash_times_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    flash_times_list = db.datas
    flash_times = [ int(x[1]) for x in flash_times_list ]

    #闪信发送成功数
    db.query_db(flash_sucess_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    flash_sucess_list = db.datas
    flash_sucess = [ int(x[1]) for x in flash_sucess_list ]

    #短信上行次数
    db.query_db(mo_times_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    mo_times_list = db.datas
    mo_times = [ int(x[1]) for x in mo_times_list ]

    #短信下行次数
    db.query_db(mt_times_sql.format(weektime=new_week_time, site_id=siteid, today=today))
    mt_times_list = db.datas
    mt_times = [int(x[1]) for x in mt_times_list]

    return render_template('site_report.html',
                           site_name=site_name,
                           sub_user=sub_user,
                           day_time=day_time,
                           unsub_user=unsub_user,
                           total_user=total_user,
                           charge_user=charge_user,
                           call_times=call_times,
                           ussd_times=ussd_times,
                           ussd_sucess=ussd_sucess,
                           flash_times=flash_times,
                           flash_sucess=flash_sucess,
                           mo_times=mo_times,
                           mt_times=mt_times)

#局点告警页面
@main.route('/site_info/alarm/<siteid>',methods=["GET","POST"])
@login_required
def siteAlarm(siteid):

    # 获取局点名
    db = queryDB()
    site_name_new_sql = site_name_sql.format(site_id=siteid)
    db.query_db(site_name_new_sql)
    site_name = db.datas[0][0]

    #获取局点告警信息列表
    db.query_db(site_alarm_sql.format(site_id=siteid))
    site_alarm_info = db.datas


    return render_template('site_alarm.html',site_name=site_name,
                           site_alarm_info=site_alarm_info,alarmDict=alarmDict)


##下载接口当访问局点信息是触发下载请求下载文件
@main.route('/site_info/download/<siteid>',methods=["GET","POST"])
@login_required
def siteDownload(siteid):
    #根据局点名获取文件下载地址
    Today = datetime.datetime.now().strftime('%Y%m%d')
    db = queryDB()
    site_domain_new_sql = site_domain_sql.format(site_id=siteid)
    db.query_db(site_domain_new_sql)
    site_url = db.datas[0][0]

    #定义需要下载的文件名及下载链接
    site_alarm_filename = siteid+'_alarm_report_'+Today
    site_sys_filename = siteid+'_sysinfo_'+Today
    site_alarm_url = site_url+site_alarm_filename
    site_sys_url = site_url+site_sys_filename

    #定义下载目录
    site_file_path = basedir+'/downloads/'+siteid

    #目录不存在则创建
    isExists = os.path.exists(site_file_path)
    if not isExists:
        os.makedirs(site_file_path)
    else:
        print("目录已存在不需要创建。")

    #下载告警报表文件
    alarm_req = requests.get(site_alarm_url, stream=True)
    f = open(os.path.join(site_file_path,site_alarm_filename), "wb")
    for chunk in alarm_req.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

    #下载服务器信息文件
    sys_req = requests.get(site_sys_url,stream=True)
    f = open(os.path.join(site_file_path, site_sys_filename), "wb")
    for chunk in sys_req.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

    #将获取的文件插入数据库
    SYS_TEXT = os.path.join(site_file_path,site_sys_filename)
    ALARM_REPORT_TEXT=os.path.join(site_file_path,site_alarm_filename)

    print(SYS_TEXT)
    sys1 = parseText()
    sys_insert = insertData()
    alarm_insert = insertData()
    server_insert = insertData()
    # 插入服务器相关数据
    try:
        sys_insert.executesql(sys1.parseSysText(SYS_TEXT)[0], sys1.parseSysText(SYS_TEXT)[1])
    except IndexError as e:
        print(e.args)
        print("服务器信息文件不存在本次不写入数据")

    # 写入报表告警相关数据
    try:
        alarm_insert.executesql(sys1.parseAlarmReportText(ALARM_REPORT_TEXT)[0], sys1.parseAlarmReportText(ALARM_REPORT_TEXT)[1])
    except IndexError as e:
        print(e.args)
        print("告警信息文件不存在本次不写入数据.")
    try:
        server_insert.executesql(sys1.parseSiteServer(SYS_TEXT)[0], sys1.parseSiteServer(SYS_TEXT)[1])
    except IndexError as e:
        print(e.args)
        print("服务器文件不存在本次不写入数据.")


    return "文件已下载"
