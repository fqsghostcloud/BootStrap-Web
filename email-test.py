# coding=utf8
from flask import Flask
from flask.ext.mail import Message, Mail
import os



app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '1178996513@qq.com'
app.config['MAIL_PASSWORD'] = '???rwrmfoewwqhjaj'

mail = Mail(app)

@app.route('/')
def index():
    msg = Message('Hello',sender='1178996513@qq.com',recipients=['376141249@qq.com'])
    msg.body = 'testind body'
    msg.html = '<b>HTML</b> body'
    mail.send(msg)

    return '<h1>send email success!</h1>'


if __name__ == '__main__':
    app.run(debug=True)