from app import app, models
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, SelectField, RadioField, SubmitField, SelectMultipleField, HiddenField, DateTimeField, widgets, DecimalField, TextField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email, Required, InputRequired, Optional
from flask import flash, session

class PasswordReset(Form):
    email = StringField('email', validators=[Email(), DataRequired()])

    submit = SubmitField()

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False

        user = models.Tutor.query.filter_by(email = self.email.data).first()

        if not user:
            self.email.errors.append('There is no account associated with that email')
            return False
        return True

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label = False)

    option_widget = widgets.CheckboxInput()

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min = 4, max = 25)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField()
    #    remember_me = BooleanField('remember_me', default=False)

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        user_to_check = models.User.query.filter_by(username = self.username.data).first()
        if not user_to_check:
            self.username.errors.append("No user with this username exists")
            return False
        if (user_to_check and not user_to_check.check_password(self.password.data)):
            self.password.errors.append("Authentication failed")
            return False        
        return True

class FourDigitForm(Form):
    search_field = IntegerField('search', validators=[DataRequired()])

    method = SelectField('method', choices = [('checkin', 'Checkin'), ('uncheckin', 'Uncheckin')])

    submit = SubmitField()

class FourDigitFormCheckout(Form):
    search_field = IntegerField('search', validators=[DataRequired()])

    method = SelectField('method', choices = [('checkout', 'Checkout'), ('uncheckout', 'Uncheckout')])

    submit = SubmitField()

class SearchForm(Form):
    search_field = StringField('search')
    
    submit = SubmitField()

class CreateForm(Form):
    fname = StringField('fname', validators=[DataRequired()])
    nickname = StringField('nickname')
    lname = StringField('lname', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(min = 4, max = 25)]) # add a unique check
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    email = StringField('email', validators=[DataRequired(), Email()])
    osis = IntegerField('osis', validators=[DataRequired()])

    organizations = MultiCheckboxField('organizations', choices = app.config['ORGANIZATIONS_FOR_SIGN_UP'])
    days = MultiCheckboxField('days', choices = app.config['DAYS'])

    grades = RadioField('grade', choices = app.config['GRADES'], validators=[DataRequired()])

    four_digit = IntegerField('four_digit', validators=[DataRequired(), NumberRange(min = 1000, max = 5000)])
    submit = SubmitField()

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False

        isError = False
        user = models.User.query.filter_by(email = self.email.data).first()
        if user:
            self.email.errors.append("This email is already registered")
            isError = True
        user = models.User.query.filter_by(username = self.username.data).first()
        if user:
            self.username.errors.append("This username is already registered")
            isError = True
        user = models.User.query.filter_by(four_digit = self.four_digit.data).first()
        if user:
            self.four_digit.errors.append("This id is already registered")
            isError = True
        user = models.User.query.filter_by(osis = self.osis.data).first()
        if user:
            self.osis.errors.append("This id is already registered")
            isError = True

        if self.grades.data == 'freshmen' or self.grades.data == 'sophomore':
            self.grades.errors.append('Unfortunately, you must be an upperclassmen to volunteer, thanks for your interest')
            isError = True


        return not isError


