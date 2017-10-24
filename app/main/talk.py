# _*_ encoding:utf-8 _*_
import requests
import json
import datetime
from ..get_server_info_mysql import *
from ..report_dict import sys_report_dict,sys_alarm_level
from ..alarm_dict import alarmDict

__author__ = 'leimin'

api_url = 'http://www.tuling123.com/openapi/api'

def talk(openid, content):
    s = requests.session()
    data = {'key': '09c4833c16444a978a7e432b71bcb133', 'info': content, 'userid': openid}
    f = s.post(api_url, data=json.dumps(data))
    print(f.content)
    text = json.loads(f.content.decode('utf-8'))['text']
    return text

def wechat_site_report(siteid):
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")

    wechat_sub_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13001 order by id desc limit 1""" \
        .format(yesterday, siteid)
    print("testsql:"+wechat_sub_sql)
    wechat_unsub_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13002 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_charge_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13003 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_total_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13027 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_totalcall_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13017 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_ussdtotal_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13009 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_ussdsucess_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13087 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_totalflash_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13018 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_sucessflash_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13088 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_mo_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13007 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_mt_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13008 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_seedtotal_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13300 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_seednew_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13301 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_seedunsub_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13302 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_seedswitch_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13303 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_selfmarket_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13308 order by id desc limit 1""" \
        .format(yesterday, siteid)
    wechat_selfmarketswtich_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13225 order by id desc limit 1""" \
        .format(yesterday, siteid)


    db = queryDB()
    db.query_db(wechat_sub_sql)
    sub_list = db.datas

    db.query_db(wechat_unsub_sql)
    ubsub_list = db.datas

    db.query_db(wechat_charge_sql)
    charge_list = db.datas

    db.query_db(wechat_total_sql)
    total_list = db.datas

    db.query_db(wechat_totalcall_sql)
    totalcall_list = db.datas

    db.query_db(wechat_ussdtotal_sql)
    totalussd_list = db.datas

    db.query_db(wechat_ussdsucess_sql)
    sucessussd_list = db.datas

    db.query_db(wechat_totalflash_sql)
    totalflash_list = db.datas

    db.query_db(wechat_sucessflash_sql)
    sucessflash_list = db.datas

    db.query_db(wechat_mo_sql)
    mo_list = db.datas

    db.query_db(wechat_mt_sql)
    mt_list = db.datas

    db.query_db(wechat_seedtotal_sql)
    seedtotal_list = db.datas

    db.query_db(wechat_seednew_sql)
    seednew_list = db.datas

    db.query_db(wechat_seedunsub_sql)
    seedunsub_list = db.datas

    db.query_db(wechat_seedswitch_sql)
    seedswitch_list = db.datas

    db.query_db(wechat_selfmarket_sql)
    selfmarket_list = db.datas

    db.query_db(wechat_selfmarketswtich_sql)
    selfmarketswitch_list = db.datas

    db.query_db(launch_site_name_sql.format(site_id=siteid))
    site_name_info = db.datas
    sitename_text = '局点{0} {1}{2}日报表:'
    site_text = ''
    for (site_id, site_name) in site_name_info:
        site_text += sitename_text.format(site_id,site_name,yesterday) + '\n'

    text = ''

    for (index, value) in sub_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in ubsub_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in charge_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in total_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in totalcall_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in totalussd_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in sucessussd_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in totalflash_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in sucessflash_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in mo_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in mt_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seedtotal_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seednew_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seedunsub_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seedswitch_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in selfmarket_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in selfmarketswitch_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'

    return site_text+text

def wechat_alarm(siteid):
    db = queryDB()
    db.query_db(site_alarm_sql.format(site_id=siteid))
    site_alarm_info = db.datas
    wechat_text = ''
    text = '节点{0} 存在{1}告警：{2}\n首次告警时间:{3}\n最近告警时间:{4}\n'
    for (id,node,ai_object_name,ai_level,ai_scene_name,ai_time,ai_last_alarm_time,send_mail) in site_alarm_info:
        wechat_text+=text.format(node,sys_alarm_level[ai_level],alarmDict[ai_scene_name],ai_time,ai_last_alarm_time)
    return wechat_text

def wechat_allsite(siteid):
    db = queryDB()
    db.query_db(launch_site_info_id.format(site_id=siteid))
    site_info = db.datas
    wechat_text = ''
    print("site_info:{0}".format(site_info))
    text = '你查询的局点为:{0}\n运维负责人是:{1}\n联系电话:{2}\n'
    for(site_name,site_ops,site_oper) in site_info:
        wechat_text+=text.format(site_name,site_ops,site_oper)
    return wechat_text

def wechat_all_site_info():
    db = queryDB()
    db.query_db(all_launch_list_sql)
    all_site_info = db.datas
    wechat_text = ''
    text = '局点id为:{0}\n局点名:{1}\n运维负责人是:{2}\n联系电话:{3}\n'
    for (site_id,site_name, site_ops, site_oper) in all_site_info:
        wechat_text += text.format(site_id,site_name, site_ops, site_oper)+'\n'
    return wechat_text


def wechat_site_report_sub(siteid,query_time):

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")

    if query_time == '-1':
        query_time = yesterday

    wechat_sub_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13001 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_unsub_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13002 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_charge_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13003 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_total_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13027 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_seedtotal_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13300 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_seednew_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13301 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_seedunsub_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13302 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_seedswitch_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13303 order by id desc limit 1""" \
        .format(query_time, siteid)

    db = queryDB()
    db.query_db(wechat_sub_sql)
    sub_list = db.datas

    db.query_db(wechat_unsub_sql)
    ubsub_list = db.datas

    db.query_db(wechat_charge_sql)
    charge_list = db.datas

    db.query_db(wechat_total_sql)
    total_list = db.datas

    db.query_db(wechat_seedtotal_sql)
    seedtotal_list = db.datas

    db.query_db(wechat_seednew_sql)
    seednew_list = db.datas

    db.query_db(wechat_seedunsub_sql)
    seedunsub_list = db.datas

    db.query_db(wechat_seedswitch_sql)
    seedswitch_list = db.datas


    db.query_db(launch_site_name_sql.format(site_id=siteid))
    site_name_info = db.datas
    sitename_text = '局点{0}-{1}:{2}日开户报表:'
    site_text = ''
    for (site_id, site_name) in site_name_info:
        site_text += sitename_text.format(site_id, site_name, yesterday) + '\n'

    text = ''

    for (index, value) in sub_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in ubsub_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in charge_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in total_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seedtotal_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seednew_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seedunsub_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in seedswitch_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'

    return site_text + text

def wechat_site_report_ope(siteid,query_time):

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")
    if query_time == '-1':
        query_time = yesterday

    wechat_totalcall_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13017 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_ussdtotal_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13009 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_ussdsucess_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13087 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_totalflash_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13018 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_sucessflash_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13088 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_mo_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13007 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_mt_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13008 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_selfmarket_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13308 order by id desc limit 1""" \
        .format(query_time, siteid)

    wechat_selfmarketswtich_sql = """ select pk_ds_stat_type,ds_num from site_report where pk_ds_day='{0}' and site_id='{1}' and  pk_ds_stat_type=13225 order by id desc limit 1""" \
        .format(query_time, siteid)

    db = queryDB()

    db.query_db(wechat_totalcall_sql)
    totalcall_list = db.datas

    db.query_db(wechat_ussdtotal_sql)
    totalussd_list = db.datas

    db.query_db(wechat_ussdsucess_sql)
    sucessussd_list = db.datas

    db.query_db(wechat_totalflash_sql)
    totalflash_list = db.datas

    db.query_db(wechat_sucessflash_sql)
    sucessflash_list = db.datas

    db.query_db(wechat_mo_sql)
    mo_list = db.datas

    db.query_db(wechat_mt_sql)
    mt_list = db.datas

    db.query_db(wechat_selfmarket_sql)
    selfmarket_list = db.datas

    db.query_db(wechat_selfmarketswtich_sql)
    selfmarketswitch_list = db.datas

    db.query_db(launch_site_name_sql.format(site_id=siteid))
    site_name_info = db.datas
    sitename_text = '局点{0}-{1}{2}日:推送报表:'
    site_text = ''
    for (site_id, site_name) in site_name_info:
        site_text += sitename_text.format(site_id, site_name, yesterday) + '\n'

    text = ''

    for (index, value) in totalcall_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in totalussd_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in sucessussd_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in totalflash_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in sucessflash_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in mo_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in mt_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in selfmarket_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'
    for (index, value) in selfmarketswitch_list:
        text += ''.join(sys_report_dict[index]) + ':' + value + '\n'

    return site_text + text

def wechat_all_site_report_sub(*args):

    try:
        query_time = args[0]
    except IndexError:
        query_time = '-1'

    db = queryDB()
    db.query_db(all_monitor_siteid_sql)
    monitor_site = db.datas
    wechat_text = ''
    for site_id in monitor_site:
        wechat_text +=  wechat_site_report_sub(site_id[0],query_time) +'\n'
    return  wechat_text

def wechat_all_site_report_ope(*args):

    try:
        query_time = args[0]
    except IndexError:
        query_time = '-1'

    db = queryDB()
    db.query_db(all_monitor_siteid_sql)
    monitor_site = db.datas
    wechat_text = ''
    for site_id in monitor_site:
        wechat_text +=  wechat_site_report_ope(site_id[0],query_time) +'\n'
    return  wechat_text
