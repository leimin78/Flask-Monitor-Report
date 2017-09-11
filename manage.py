#!/usr/bin/env python
from app import create_app, db
from flask_script import Manager, Shell
app = create_app('development')
manager = Manager(app)

if __name__ == '__main__':
    #manager.run()
    app.run(host='0.0.0.0',port=5000)
