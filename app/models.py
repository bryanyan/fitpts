from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(64), index=True, unique=True)
	groups = db.relationship('Group', backref="author", lazy="dynamic")

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def __repr__(self):
		return '<User %r>' %(self.username)


class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	group_name = db.Column(db.String(140))
	numppl = db.Column(db.Integer)
	actives = db.relationship('Active', backref="group", lazy="dynamic")
	time = db.Column(db.String)

	def __repr__(self):
		return '<Group %r>' %(self.group_name)

class Active(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
	active_name = db.Column(db.String(140))
	points = db.Column(db.Integer)
	session_points = db.Column(db.Integer)

	def __repr__(self):
		return '<Active %r>' %(self.active_name)






