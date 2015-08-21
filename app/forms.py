from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators, IntegerField
from wtforms.validators import DataRequired


class RegistrationForm(Form):
	username = TextField('username', [validators.Length(min=4, max=25)])
	password = PasswordField('password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')

class LoginForm(Form):
	username = TextField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class GroupForm(Form):
	name = TextField('Name of Group', validators=[DataRequired()])
	numppl = IntegerField('Number of People', validators=[validators.NumberRange(min=1, max=50)])

	

