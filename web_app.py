from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'i love potatoes'

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Person, Event, Attendance

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


#YOUR WEB APP CODE GOES HERE
from datetime import datetime
# wget http://tinyurl.com/MEETpythonY2
# source MEETpythonY2


@app.route('/', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login_page.html')
	else:
		# ADD LOGIN AND ALL THAT GOOD STUFF HERE!!!
		user = dbsession.query(Person).filter_by(username = request.form['username']).first()
		if user == None or user.password != request.form['password']: # If username doesn't exist or wrong password
			return render_template('login_page.html', error=True)
		else:
			session['user_id'] = user.id
			return redirect(url_for('main'))


@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('login'))


@app.route('/main')
def main():
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	events = dbsession.query(Event).all()
	first_event = events.pop(0)
	events_len = len(events)
	return render_template('main_page.html', user=user, first_event = first_event, events=events, events_len=events_len)


@app.route('/create-account', methods = ['GET', 'POST'])
def create_account():
	if request.method == 'GET':
		return render_template('create_account.html')
	else:
		# ADD CREATING ACCOUNT AND ALL THAT GOOD STUFF HERE!!!
		user = Person(name = request.form['fullname'],
					  username = request.form['username'],
					  password = request.form['password'],
					  gender = request.form['gender'],
					  nationality = request.form['nationality'],
					  bio = request.form['bio'],
					  rating = 5,
					  pic = "")
		dbsession.add(user)
		dbsession.commit()
		return redirect(url_for('login'))


@app.route('/create-event', methods = ['GET', 'POST'])
def create_event():
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	events = dbsession.query(Event).all()  # Get all events

	if request.method == 'GET':
		currentyear = datetime.now().year
		years = [currentyear, currentyear + 1]
		months = range(1, 13)
		days = range(1, 32) 
		return render_template('create_event.html', user=user , years = years, months = months, days = days)

	else:  # If user wants to create an event

		event_exists = False
		for event in events:
			if event.title == request.form['title']:  # If event name exists
				event_exists = True
				break


		if not event_exists:  # Check if event exists flag is set
			event_date = datetime(int(request.form['year']), int(request.form['month']), int(request.form['day']))		
			event = Event(title = request.form['title'],
						  date = event_date,
						  description = request.form['description'],
						  owner_id = user.id,
						  owner = user,
						  location = request.form['location'])

			event_attendance = Attendance(person_id = session['user_id'],
										  person = dbsession.query(Person).filter_by(id = session['user_id']).first(),
										  event_id = event.id,
										  event = event,
										  chef_flag = True)

			dbsession.add(event)
			dbsession.add(event_attendance)
			dbsession.commit()
			## ADD ELSE (EVENT EXISTS) TELL USER

		return redirect(url_for('event_page', event_id = event.id))


@app.route('/event/<int:event_id>') #Add and event id or smth
def event_page(event_id):
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	event = dbsession.query(Event).filter_by(id = event_id).first()
	attendance_list = dbsession.query(Attendance).filter_by(event_id = event_id).all()  # All attendance for this event

	already_attending = False

	for attendance in attendance_list:
		if attendance.person_id == session['user_id']:
			already_attending = True  # Check if user is in this event
			break


	if event.owner == user:
		session['event_id'] = event.id
	return render_template('event_page.html', user=user, event = event, attendance_list = attendance_list, already_attending = already_attending)


@app.route('/edit-event', methods = ['GET','POST'])
def edit_event():
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	event = dbsession.query(Event).filter_by(id = session['event_id']).first()
	if request.method == 'GET':
		currentyear = datetime.now().year
		years = [currentyear, currentyear + 1]
		months = range(1, 13)
		days = range(1, 32) 
		return render_template('edit_event.html', user=user , event = event, years = years, months = months, days = days)

	else:
		new_title = request.form['title']
		new_date = datetime(int(request.form['year']), int(request.form['month']), int(request.form['day']))
		new_desc = request.form['description']

		event.name = new_title
		event.date = new_date
		event.description = new_desc

		dbsession.commit()
		return redirect(url_for('event_page', event_id = event_id))


@app.route('/attend-event/<int:event_id>')
def attend_event(event_id):
	already_attending = False
	event = dbsession.query(Event).filter_by(id = event_id).first()
	attendance_list = dbsession.query(Attendance).filter_by(event_id = event.id).all()

	for attendance in attendance_list:
		if attendance.person_id == session['user_id']:
			already_attending = True
			break

	if request.args.get('chef') == '1':
		chef_flag = True
	else:
		chef_flag = False

	if not already_attending:  # If the user is not already going to the event, add him to the event
		event_attendance  = Attendance(person_id = session['user_id'],
									   person = dbsession.query(Person).filter_by(id = session['user_id']).first(),
									   event_id = event.id,
									   event = event,
									   chef_flag = chef_flag)

		dbsession.add(event_attendance)
		dbsession.commit()
	return redirect(url_for('event_page', event_id = event_id))


@app.route('/unattend-event/<int:event_id>')
def unattend_event(event_id):
	event = dbsession.query(Event).filter_by(id = event_id).first()
	attendance_list = dbsession.query(Attendance).filter_by(event_id = event_id).all()

	for attendance in attendance_list:
		if session['user_id'] == attendance.person_id and session['user_id'] != event.owner_id:
			dbsession.delete(attendance)

	dbsession.commit()
	return redirect(url_for('event_page', event_id = event_id))


@app.route('/profile/<int:user_id>')
def profile(user_id):
	user = dbsession.query(Person).filter_by(id = user_id).first()
	return render_template('profile_page.html', user = user, current_id = session['user_id'])


@app.route('/edit-profile', methods = ['GET', 'POST'])
def edit_profile():
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	if request.method == 'GET':
		return render_template('edit_profile.html', user = user)

	else:  # User submitted his changes
		new_name = request.form['fullname']
		new_password = request.form['password']
		new_gender = request.form['gender']
		new_nationality = request.form['nationality']
		new_bio = request.form['bio']
		new_pic = request.form['pic']


		user.name = new_name
		user.password = new_password
		user.gender = new_gender
		user.nationality = new_nationality
		user.bio = new_bio
		user.pic = new_pic

		dbsession.commit()
		return redirect(url_for('profile', user=user, user_id = user.id))


@app.route('/results')
def results_page():
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	searchtype = request.args.get('searchtype')
	search = request.args.get('search')
	#search = search.lower()

	if searchtype in ('Events', 'Food'):
		results = dbsession.query(Event).filter(or_(Event.title.contains(search), Event.description.contains(search))).all()

	elif searchtype == 'People':
		results = dbsession.query(Person).filter(or_(Person.name.contains(search), Person.bio.contains(search))).all()

	if results == []:
		searchtype = '404'
		print('nothing found')

	return render_template('results.html', user=user, type=searchtype, results = results)


if __name__ == '__main__':
	app.run(debug=True)

