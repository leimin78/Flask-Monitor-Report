import datetime
import time
import requests
import re
import hashlib
import xml.etree.ElementTree as ET
from .talk import talk,wechat_site_report,wechat_alarm,wechat_allsite,wechat_all_site_info,wechat_all_site_report_sub,wechat_all_site_report_ope
from flask import render_template,redirect,url_for,flash,request,make_response
from flask_login import login_user,login_required,logout_user
from . import main
from ..models import *
from ..get_server_info_mysql import *
from ..alarm_dict import alarmDict
from .. import login_manager
from ..insert_data import *

import os

basedir = os.path.abspath(os.path.dirname(__file__))
rule_sub = re.compile(r'sub\d{8}')
rule_ope = re.compile(r'ope\d{8}')

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect('login')

@main.route('/login',methods=["GET","POST"])
def login():
    #进入首页时对用户session进行清除
    logout_user()
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
    #获取维护人员信息
    db.query_db(sys_user_sql)
    sys_user_info = db.datas

    #获取商用局点信息
    db.query_db(launch_site_info)
    launch_info = db.datas
    return render_template('site_info.html',site_info=site_info,sys_user_info=sys_user_info,launch_info=launch_info)


#局点基本信息页面
@main.route('/server_info/<siteid>',methods=['GET','POST'])
@login_required
def serverList(siteid):
    db = queryDB()
    max_time = []
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

    #删除运行节点老数据只保留最新数据
    db.query_db(ip_maxtime_sql)
    ip_maxtime_list = db.datas
    del_old_sql = "delete from sys_info where run_node_name is not null and record_time<'{max_time}' and host_ip='{host_ip}'"
    for id,maxtime,ip in ip_maxtime_list:
        new_del_old_sql = del_old_sql.format(max_time=maxtime,host_ip=ip)
        db.delete_db(new_del_old_sql)

    #获取运行节点
    db.query_db(run_node_list_sql)
    run_node_list = db.datas

    #获取最近内存使用率
    db.query_db(mem_use_sql)
    mem_use_list = db.datas
    return render_template('server_info.html',server_list=server_list,site_name=site_name,cpu_use_list=cpu_use_list,
                           mem_use_list=mem_use_list,run_node_list=run_node_list)

#服务器详细细信息页面
@main.route('/server_detail/<serverip>',methods=['GET','POST'])
@login_required
def serverDetail(serverip):

    #设置时间参数
    week_time = datetime.datetime.now() - datetime.timedelta(days=7)
    new_week_time = week_time.strftime("%Y%m%d%H%M%S")
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
    sub_user = [ int(x[2]) for x in sub_user_list ]
    day_time = [ int(x[1]) for x in sub_user_list ]

    #获取销户数
    db.query_db(unsub_user_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    unsub_user_list = db.datas
    unsub_user = [ int(x[2]) for x in unsub_user_list ]

    #获取总用户数
    db.query_db(total_user_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    total_user_list = db.datas
    total_user = [ int(x[2]) for x in total_user_list ]

    #获取收费用户数
    db.query_db(charge_user_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    charge_user_list = db.datas
    charge_user = [ int(x[2]) for x in charge_user_list ]


    #呼叫次数
    db.query_db(call_times_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    call_times_list = db.datas
    call_times = [ int(x[2]) for x in call_times_list ]

    #USSD发送次数
    db.query_db(ussd_times_sql.format(weektime=new_week_time,site_id=siteid,today=today))
    ussd_times_list = db.datas
    ussd_times = [ int(x[2]) for x in ussd_times_list ]

    #USSD发送成功数
    db.query_db(ussd_sucess_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    ussd_sucess_list = db.datas
    ussd_sucess = [ int(x[2]) for x in ussd_sucess_list ]

    #闪信发送次数
    db.query_db(flash_times_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    flash_times_list = db.datas
    flash_times = [ int(x[2]) for x in flash_times_list ]

    #闪信发送成功数
    db.query_db(flash_sucess_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    flash_sucess_list = db.datas
    flash_sucess = [ int(x[2]) for x in flash_sucess_list ]

    #短信上行次数
    db.query_db(mo_times_sql.format(weektime=new_week_time, site_id=siteid,today=today))
    mo_times_list = db.datas
    mo_times = [ int(x[2]) for x in mo_times_list ]

    #短信下行次数
    db.query_db(mt_times_sql.format(weektime=new_week_time, site_id=siteid, today=today))
    mt_times_list = db.datas
    mt_times = [int(x[2]) for x in mt_times_list]

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

    #如果告警最近告警时间超过2天则认为告警恢复数据清楚
    two_days = datetime.datetime.now() - datetime.timedelta(days=2)
    new_two_days = two_days.strftime("%Y%m%d%H%M%S")

    db.delete_db(delete_alarm_sql.format(site_id=siteid,two_days=new_two_days))

    #获取局点告警信息列表
    db.query_db(site_alarm_sql.format(site_id=siteid))
    site_alarm_info = db.datas

    return render_template('site_alarm.html',site_name=site_name,
                           site_alarm_info=site_alarm_info,alarmDict=alarmDict)


#增加微信查询功能
@main.route('/wx',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='hello2017' #微信配置所需的token
        data = request.args
        print(data)
        signature = data.get('signature','')
        print("signature:{0}".format(signature))
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        print(s)
        if (hashlib.sha1(s.encode('utf-8')).hexdigest() == signature):
            return make_response(echostr)
    elif request.method == 'POST':
        db = queryDB()
        db.query_db(site_info_sql)
        site_info = db.datas

        db.query_db(all_siteid_name_sql)
        all_site_info = db.datas

        rec = request.stream.read()
        print("im posting:{0}".format(rec))
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        if content.upper() == u'帮助':
            text = u"日报查询例如:C10R\n告警查询例如:C10A\n所有日报查询:ALL\n所有商用局点信息:LIST\n"
        elif content.upper() == u'SUB':
            text = wechat_all_site_report_sub()
        elif content.upper() == u'OPE':
            text = wechat_all_site_report_ope()
        elif rule_sub.search(content.upper()):
            query_time = rule_sub.search(content.upper()).group()[3:]
            wechat_all_site_report_sub(query_time)
        elif rule_ope.search(content.upper()):
            query_time = rule_ope.search(content.upper()).group()[3:]
            wechat_all_site_report_ope(query_time)
        elif content.upper() == u'LIST':
            text = wechat_all_site_info()
        elif content.upper() in [ siteid+'R' for siteid,sitename in site_info]:
            text = wechat_site_report(content.upper().strip('R'))
        elif content.upper() in [ siteid+'A' for siteid,sitename in site_info]:
            text = wechat_alarm(content.upper().strip('A'))
        elif content.upper() in [ siteid for siteid,sitename in all_site_info]:
            text = wechat_allsite(content.upper())
            print("text:{0}".format(text))
        else:
            text = talk(tou,content)
        xml_rep = "<xml>" \
                  "<ToUserName>" \
                  "<![CDATA[%s]]></ToUserName>" \
                  "<FromUserName><![CDATA[%s]]></FromUserName>" \
                  "<CreateTime>%s</CreateTime>" \
                  "<MsgType><![CDATA[text]]></MsgType>" \
                  "<Content><![CDATA[%s]]></Content>" \
                  "<FuncFlag>0</FuncFlag>" \
                  "</xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())), text))
        response.content_type='application/xml'
        return response

    else:
        pass
    return 'Hello weixin!'
