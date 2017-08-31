import os
from flask import Flask, render_template, redirect, url_for, session, flash,jsonify,request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_login import LoginManager,login_user,login_required,logout_user,UserMixin
from flask_script import Manager
from get_server_info  import *
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))


# 定义表单
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


login_manager = LoginManager()
login_manager.init_app(app)


password = "123456"

## 定义数据模型
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

    server_site_id = db.Column(db.String(10),db.ForeignKey('site_info.site_id'))

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
    lun_use = db.Column(db.Float,nullable=True)
    lun_size = db.Column(db.Float,nullable=True)

    system_version = db.Column(db.String(128),nullable=True)
    server_uptime = db.Column(db.String(128),nullable=True)

    record_time = db.Column(db.String(14))
    host_ip = db.Column(db.String(30),db.ForeignKey('server_info.server_ip'))




@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你刚才改过输入了.')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/sys_info',methods=["POST","GET"])
def sys_info():
    new_cpu_sql = (cpu_sql % int(request.form.get('id',0)))
    print("hello im post")
    db = queryDB()
    db.query_db(new_cpu_sql)
    data = db.datas
    return jsonify(
        user_use = [x[0] for x in data],
        sys_use = [x[1] for x in data],
        io_use = [x[2] for x in data],
        record_time = [x[-1].strip('\n') for x in data]
        )

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))

@app.route('/cpuinfo')
@login_required
def cpu_info():

    return render_template('cpu_info.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname = request.form.get('uname')
        print(uname)
        user = UserInfo.query.filter_by(user_name=uname).first()
        print(user)
        if not user:
            flash('抱歉用户不存在')
            return redirect(url_for('login'))
        elif user.verify_password(request.form.get('pass')) == False:
            flash('抱歉密码错误')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('cpu_info'))
    return render_template('login.html')

#局点服务器列表页面
@app.route('/site_info',methods=['GET','POST'])
def siteInfo():
    db = queryDB()
    db.query_db(site_info_sql)
    site_info = db.datas
    return render_template('site_info.html',site_info=site_info)

@app.route('/server_info/<siteid>',methods=['GET','POST'])
def serverList(siteid):
    db = queryDB()
    print(siteid)
    site_server_sql = server_list_sql.format(site_id=siteid)
    site_name_new_sql = site_name_sql.format(site_id=siteid)
    print(site_server_sql)
    db.query_db(site_server_sql)
    server_list = db.datas
    db.query_db(site_name_new_sql)
    site_name = db.datas[0][0]
    return render_template('server_info.html',server_list=server_list,site_name=site_name)

@app.route('/server_detail',methods=['GET','POST'])
def serverDetail():
    return render_template('server_detail.html')

if __name__ == '__main__':
    manager.run()
