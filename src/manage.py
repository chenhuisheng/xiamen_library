#coding:utf-8

import os
from flask import g
from flask_script import Manager, Shell, Server
from app import create_app, db

app = create_app(os.getenv('MIKE_BI_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

@manager.command
def add_opf():
    from app.service.book import get_opf_path
    get_opf_path()


if __name__ == '__main__':
    manager.run()