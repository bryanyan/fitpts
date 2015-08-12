from flask import render_template, flash, redirect, request, session, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import RegistrationForm, LoginForm, GroupForm
from .models import User, Group, Active
import json

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegistrationForm()
	if request.method == 'POST' and form.validate():
		user = User(username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Account created for "%s"' %(form.username.data))
		return redirect('/login')
	return render_template('signup.html', title="Create Account", form=form)

@app.before_request
def before_request():
	g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	if request.method == 'POST' and form.validate():
		user = User.query.filter_by(username=form.username.data).first()
		if user != None and form.password.data == user.password:
			login_user(user)
			flash('Login requested for "%s"' %(form.username.data))
			return redirect(url_for('index'))
	flash('Invalid login, please try again')
	return render_template('login.html', title="Login", form=form)

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/leaderboard')
@login_required
def leaderboard():
	return render_template('leaderboard.html', title="Leaderboards")

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
	form = GroupForm()
	if request.method == 'POST' and form.validate():
		group = Group(group_name=form.name.data, numppl=form.numppl.data, author=g.user)
		db.session.add(group)
		for i in xrange(int(request.form['numppl'])):
			active = Active(active_name=request.form['p%d' %(i)], points=0, group=group)
			db.session.add(active)
		db.session.commit()
		flash('Group created called "%s"' %(form.name.data))
		return redirect('/viewgroups')
	return render_template('create.html', title="Create Group", form=form)

@app.route('/viewgroups')
@login_required
def viewgroups():
	groups = g.user.groups.all()
	
	return render_template('groups.html', title="Your Groups", groups=groups)









