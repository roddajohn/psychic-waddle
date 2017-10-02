from app import db
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    fname = db.Column(db.String(128), index = True, unique = False)
    lname = db.Column(db.String(128), index = True, unique = False)
    nickname = db.Column(db.String(128), index = True, unique = False)

    username = db.Column(db.String(128), index = True, unique = True)
    password = db.Column(db.String(1024), index = True, unique = False)

    email = db.Column(db.String(128), index = True, unique = False)

    osis = db.Column(db.Integer, index = True, unique = True)
    four_digit = db.Column(db.Integer, index = True, unique = True)

    organizations = db.Column(db.String(2048), index = True, unique = False)

    wednesday = db.Column(db.Boolean, index = True, unique = False)
    thursday = db.Column(db.Boolean, index = True, unique = False)

    timestamp_wednesday_checked_in = db.Column(db.DateTime, index = True, unique = False)
    timestamp_wednesday_checked_out = db.Column(db.DateTime, index = True, unique = False)

    timestamp_thursday_checked_in = db.Column(db.DateTime, index = True, unique = False)
    timestamp_thursday_checked_out = db.Column(db.DateTime, index = True, unique = False)

    wednesday_excused = db.Column(db.Boolean, index = True, unique = False)
    thursday_excused = db.Column(db.Boolean, index = True, unique = False)

    wednesday_status = db.Column(db.Integer, index = True, unique = False)
    thursday_status = db.Column(db.Integer, index = True, unique = False)

    # 0 not checked in
    # 1 checked in ONLY
    # 2 checked out ONLY
    # 3 checked both in and out

    permissions = db.Column(db.String(1024), index = True, unique = False)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)
        db.session.commit()

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def add_organization(self, organization):
        if not self.organizations[:-1] == ',':
            self.organizations += ','
        if not self.check_organization(organization):
            self.organizations += organization + ','
        db.session.commit()

    def remove_organization(self, organization):
        self.organizations = self.organizations.replace(organization + ',', ',')
        db.session.commit()

    def check_organization(self, organization):
        contains_organization = False
        for p in self.organizations.split(','):
            contains_organization = contains_organization or (p == organization)
        return contains_organization

    def add_permission(self, permission):
        if not self.permissions[:-1] == ',':
            self.permissions += ','
        if not self.check_permission(permission):
            self.permissions += permission + ','
        db.session.commit()

    def remove_permission(self, permission):
        self.permissions = self.permissions.replace(permission + ',', ',')
        db.session.commit()

    def check_permission(self, permission):
        contains_permission = False
        for p in self.permissions.split(','):
            contains_permission = contains_permission or (p == permission)
        return contains_permission
    
