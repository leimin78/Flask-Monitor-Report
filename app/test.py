import os
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

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
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


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
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(100),unique=True)
    user_pass = db.Column(db.String(100))
    user_mail = db.Column(db.String(100),unique=True)

    #一个用户可以管理多个局点
    user_site_id = db.Column(db.String(100))

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

    host_id = db.Column(db.Integer,db.ForeignKey('server_info.id'))




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


@app.route('/sys_info')
def sys_info():
    with open('../script_agent/system_info_20170825.txt', 'r') as f:
        content = f.readlines()
    return render_template('system_info.html', content=content)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
