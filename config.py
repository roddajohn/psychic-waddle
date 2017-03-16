import os
# The base directory (DO NOT CHANGE, unless you know EXACTLY what you are doing)
basedir = os.path.abspath(os.path.dirname(__file__))

# The base directory for the database (DO NOT CHANGE, unless you know EXACTLY what you are doing)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# More sql setup, reference previous comment
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# WTForms Config
# Enable the security on the forms
WTF_CSRF_ENABLED = True
# Secret key for the hashes
SECRET_KEY = 'THIS IS A SECRET KEY'

ORGANIZATIONS = [('arista', 'ARISTA'),
                 ('big_sibs', 'Big Sibs'),
                 ('red_cross', 'Red Cross'),
                 ('key_club', 'Key Club')]

ORGANIZATIONS_FOR_SIGN_UP = [('red_cross', 'Red Cross'),
                             ('key_club', 'Key Club')]

DAYS = [('wed', 'Wednesday, October 5'),
        ('thurs', 'Thursday, October 6')]

ELEMENTS_PER_PAGE = 10
