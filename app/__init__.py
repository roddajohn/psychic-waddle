from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

from flask_mail import Mail

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.update(dict(MAIL_SERVER = 'mail.stuyarista.org',
                       MAIL_PORT = 465,
                       MAIL_USE_SSL = True,
                       MAIL_USERNAME = 'ec@stuyarista.org',
                       MAIL_PASSWORD = '[16ejgrs17!]',
                       MAIL_USER_TLS = False,
                       MAIL_MAX_EMAILS = 10,
                       MAIL_DEFAULT_SENDER = 'ARISTA <ec@stuyarista.org>')) 

app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

import views
