#   需求分析

2017-08-24:

> 减少维护工作量，对具备门户的系统，进行信息采集，并在web展示报表
> 采集系统信息 cpu,mem,disk,
> 采集业务信息 前一天开户数,销户数,总用户数,呼叫数,签名推送数,mo,mt
> 告警信息收集 告警节点,告警时间,告警描述, 告警是否恢复 （对于未恢复节点的告警需要发送邮件)

## 采集文本格式定义
## 文件名 system_info_YYYYmmdd.txt
> server_name|server_ip|site_id|type|record_time
> server_name|server_ip|site_id|cpu|user_use|sys_use|io_use|idle|record_time
> server_name|server_ip|site_id|mem|mem_use|mem_free|mem_buffer|mem_total|record_time
> server_name|server_ip|site_id|disk|/|disk_used|disk_total|record_time
> server_name|server_ip|site_id|disk|/home|disk_used|disk_total|record_time


## 文件名 system_alarm_YYYYmmdd.txt
> site_id|alarm_name|alarm_node|alarm_desc|alarm_time|alarm_resume_time|record_time

## 文件名 system_service_YYYYmmdd.txt
> site_id|sub_users|unsub_users|total_users|call_times|show_times|mo_times|mt_times|record_time


