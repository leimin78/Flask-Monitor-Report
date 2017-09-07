#!/usr/bin/env python
from app import create_app, db
from flask_script import Manager, Shell
app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)