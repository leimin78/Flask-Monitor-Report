#!/usr/bin/env python
from app import create_app, db
from flask_script import Manager, Shell

# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
# gevent end

app = create_app('testdb')
manager = Manager(app)

if __name__ == '__main__':
    #manager.run()
    #app.run(host='0.0.0.0',port=5000)
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
