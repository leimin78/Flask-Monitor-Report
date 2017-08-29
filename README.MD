#   需求分析

2017-08-24:

> 减少维护工作量，对具备门户的系统，进行信息采集，并在web展示报表
> 采集系统信息 cpu,mem,disk,
> 采集业务信息 前一天开户数,销户数,总用户数,呼叫数,签名推送数,mo,mt
> 告警信息收集 告警节点,告警时间,告警描述, 告警是否恢复 （对于未恢复节点的告警需要发送邮件)

### 采集文本格式定义
### 文件名 system_info_YYYYmmdd.txt
### 接口url: http://site_url/sys_monitor/system_info_YYYYmmdd.txt
> server_name|server_ip|site_id|type|record_time
> server_name|server_ip|site_id|cpu|user_use|sys_use|io_use|idle|record_time
> server_name|server_ip|site_id|mem|mem_use|mem_free|mem_buffer|mem_total|record_time
> server_name|server_ip|site_id|disk|/|disk_used|disk_total|record_time
> server_name|server_ip|site_id|disk|/home|disk_used|disk_total|record_time


### 文件名 system_alarm_YYYYmmdd.txt
### 接口url http://site_url/sys_alarm/system_alarm_YYYYmmdd.txt
> site_id|alarm_name|alarm_node|alarm_desc|alarm_time|alarm_resume_time|record_time


### 文件名 system_service_YYYYmmdd.txt
### 接口url http://site_url/sys_service/system_service_YYYYmmdd.txt
> site_id|sub_users|unsub_users|total_users|call_times|show_times|mo_times|mt_times|record_time

### 技术栈 计划使用 Flask + echarts 进行展示


2017-08-25:

### 增加服务器信息采集脚本
### 规划目录结构

Flask-Monitor-Report/ </br>
├── README.MD </br>
├── app </br>
│   ├── main </br>
│   ├── static </br>
│   └── templates </br>
├── config.py </br>
├── migrations </br>
├── script_agent </br>
│   ├── system_info.py </br>
│   └── system_info_20170824.txt </br>
└── tests </br>


### 定义局点表，用户表，服务器表，系统信息表的模型

> 一个用户可以管理多个局点，一台服务器只能属于一个局点，一条记录属于一台服务器

2017-08-27

### 新增文本解析，入库脚本。

2017-08-28

### 用echarts 对数据库数据进行可视化处理

对cpu数据进行可视化,目前还在测试阶段

2017-08-29

### 不懂前端是硬伤呀.. ajax调测一天都没通暂时放放先搞定其他功能

> 今天新增登录页面

