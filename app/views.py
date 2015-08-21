from flask import render_template, flash, redirect, request, session, url_for, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import RegistrationForm, LoginForm, GroupForm
from .models import User, Group, Active
from operator import itemgetter, attrgetter
from datetime import datetime, timedelta, date
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

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
	form = GroupForm()
	if request.method == 'POST' and form.validate():
		day = str(date.today())
		group = Group(group_name=form.name.data, numppl=form.numppl.data, author=g.user, time=day)
		db.session.add(group)
		for i in xrange(int(request.form['numppl'])):
			active = Active(active_name=request.form['p%d' %(i)], points=0, session_points=0, group=group)
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

@app.route('/members/group<int:group>', methods=['GET','POST'])
@login_required
def members(group):
	groups = g.user.groups.all()
	selectedGroup = groups[group-1]
	members = selectedGroup.actives.all()
	if request.method == "POST":
		members[int(request.form['activeindex'])-1].points += int(request.form['ptadd'])
		members[int(request.form['activeindex'])-1].session_points += int(request.form['ptadd'])
		db.session.commit()
		return redirect('/members/group%d' %(group))
	return render_template('members.html', title="Members", members=members)


def check_date(group):
	current_date = date.today()
	mems = group.actives.all()
	if group.time != None:
		prev_time = datetime.strptime(group.time, "%Y-%m-%d")
		prev_day = datetime.date(prev_time)
		delta = current_date-prev_day
		for actives in mems:
			if delta.days >= 7:
				actives.session_points = 0
				group.time = str(current_date)
		db.session.commit()
	return

@app.route('/leaderboards/group<int:group>', methods=['GET', 'POST'])
@login_required
def leaderboards(group):
	groups = g.user.groups.all()
	selectedGroup = groups[group-1]
	members = selectedGroup.actives.all()
	check_date(selectedGroup)
	leaders = sorted(members, key=attrgetter('points'), reverse=True)
	weekly = sorted(members, key=attrgetter('session_points'), reverse=True)
	return render_template('leaderboards.html', title="Leaderboards", leaders=leaders, weekly=weekly)


