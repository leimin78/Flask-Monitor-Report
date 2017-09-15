from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


## 定义数据模型,初始化表
#  局点表,局点ID,局点名,局点url
class SiteInfo(db.Model):
    __tablename__ = 'site_info'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    site_id = db.Column(db.String(10),unique=True)
    site_name = db.Column(db.String(50),unique=True)
    site_url = db.Column(db.String(100),unique=True)

    def __repr__(self):
        return self.site_name

#用户表,用户名,密码,邮箱,负责局点
class UserInfo(UserMixin,db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(100),unique=True)
    user_mail = db.Column(db.String(100),unique=True)
    password_hash = db.Column(db.String(128))
    #一个用户可以管理多个局点
    user_site_id = db.Column(db.String(100))

    #新增用户姓名，电话号码字段
    user_cname  = db.Column(db.String(100))
    user_phone = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

#服务器信息表,服务器名，服务器IP，服务器所属局点
class ServerInfo(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    server_name = db.Column(db.String(100),unique=True)
    server_ip = db.Column(db.String(30),unique=True)
    server_site_id = db.Column(db.String(10))

#局点维护报表,局点名,日期,数据类型,数据
class SiteReport(db.Model):
    __tablename__ = 'site_report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pk_ds_day = db.Column(db.String(14),nullable=True)
    pk_ds_stat_type = db.Column(db.String(14),nullable=True)
    ds_num = db.Column(db.String(100),nullable=True)
    site_id = db.Column(db.String(10))

#局点告警列表,告警节点,告警对象,告警场景,首次告警时间,最近告警时间,告警级别,局点名

class SiteAlarm(db.Model):
    __tablename__ = 'site_alarm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ai_node_name = db.Column(db.String(100),nullable=True)
    ai_object_name = db.Column(db.TEXT,nullable=True)
    ai_scene_name = db.Column(db.TEXT,nullable=True)
    ai_time = db.Column(db.String(14),nullable=True)
    ai_last_alarm_time = db.Column(db.String(14),nullable=True)
    ai_level = db.Column(db.String(10),nullable=True)
    site_id = db.Column(db.String(10))
    send_mail = db.Column(db.String(128),default=0)



#系统状态表,cpu用户使用,cpu系统使用,cpu_io使用,cpu空闲,
# 内存使用,内存剩余,内存buffer,内存总量
# 磁盘分区名,已用大小,总大小
# 所属机器
class SysInfo(db.Model):
    __tablename__ = 'sys_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_use = db.Column(db.Float,nullable=True)
    sys_use = db.Column(db.Float,nullable=True)
    io_use = db.Column(db.Float,nullable=True)
    idle_use = db.Column(db.Float,nullable=True)

    mem_use = db.Column(db.Float,nullable=True)
    mem_free = db.Column(db.Float,nullable=True)
    mem_buffer = db.Column(db.Float,nullable=True)
    mem_total = db.Column(db.Float,nullable=True)

    lun_name = db.Column(db.String(10),nullable=True)
    lun_use = db.Column(db.String(10),nullable=True)
    lun_size = db.Column(db.String(10),nullable=True)
    lun_rate = db.Column(db.String(10), nullable=True)

    system_version = db.Column(db.String(128),nullable=True)
    server_uptime = db.Column(db.String(128),nullable=True)

    run_node_name = db.Column(db.String(128),nullable=True)

    record_time = db.Column(db.String(14))
    host_ip = db.Column(db.String(30))