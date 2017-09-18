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

app 主程序目录
mail 视图目录
static 资源文件
templates 模板目录
alarm_dict 字典解析相关告警场景
get_server_info 数据查询
models 表结构定义


### 定义局点表，用户表，服务器表，系统信息表的模型

> 一个用户可以管理多个局点，一台服务器只能属于一个局点，一条记录属于一台服务器

2017-08-27

### 新增文本解析，入库脚本。

2017-08-28
gi
### 用echarts 对数据库数据进行可视化处理

对cpu数据进行可视化,目前还在测试阶段

2017-08-29

### 不懂前端是硬伤呀.. ajax调测一天都没通暂时放放先搞定其他功能

> 今天新增登录页面

2017-08-30

> 实现用户登录

> 新增局点列表页面

2017-08-31

> 新增局点服务器列表
> 优化客户端数据采集,新增操作系统,运行时间采集

2017-09-01

> 完成服务器详细信息页面制作
> 优化客户端数据采集,新增磁盘使用率信息采集

基本功能已经具备 下一步需要对代码结构做调整。

2017-09-03
> 完成内存信息采集

2017-09-04
> 局点报表页面，该页面包含用户数据，彩印推送数据
> 对数据库初始脚本做优化,插入数据前判断数据是否已存在，只插入不同数据

2017-09-05
> 新增告警，及报表数据采集脚本


2017-09-06
> 对加入告警,报表数据的初始化
> 新增告警页面

2017-09-07
> 调整代码结构为 分离视图,模型
> 对模板做优化,加入退出功能

2017-09-08
> 修改文件合并脚本,部署脚本到服务器

2017-09-09
> 跟生成服务器进行对接，完成数据下载接口，及数据解析插入

2017-09-10
> 格式化页面时间，对一些查询脚本做优化，优化数据库参数配置 同时支持windows，linux

2017-09-11  
> 新增uwsgi脚本部署上线

2017-09-12
> 优化报表页面，统一大小，优化告警报表语句
> 优化session机制用户撤回到首页清空session
> 增加服务器运行节点信息采集

已知问题，邮件发送时 可能会被邮件服务器拦截导致收不到邮件

2017-09-13
> 优化运行节点，对运行节点只保留最近数据
> 增加插入数据异常处理

2017-09-14
> 优化告警数据，最近告警时间2天没发生变化时则删除数据


2017-09-15
> 改为mysql数据库 ，数据更新改为异步方式

2017-09-17
> 优化数据插入加入标记每次插入数据从上一次位置开始

2017-09-18
> 加入微信查询