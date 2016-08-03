from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'i love potatoes'

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Person, Event, Attendance

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


#YOUR WEB APP CODE GOES HERE

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
	return render_template('main_page.html', user=user)


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
					  rating = 5)
		dbsession.add(user)
		dbsession.commit()
		return redirect(url_for('login'))


@app.route('/create-event', methods = ['GET', 'POST'])
def create_event():
	if request.method == 'GET':
		return render_template('create_event.html')
	else:
		event = Event(title = request.form['title'],
			date = request.form['date'],
			description = request.form['description'])
		dbsession.add(event)
		dbsession.commit()
		return redirect(url_for('event'))

@app.route('/event/<int:event_id>') #Add and event id or smth
def event(event_id):
	event = dbsession.query(Event).filter_by(id = event_id).first()
	return render_template('event_page.html', event = event)


@app.route('/profile/<int:user_id>')
def profile(user_id):
	user = dbsession.query(Person).filter_by(id = user_id).first()
	return render_template('profile_page.html', user = user)


@app.route('/edit-profile', methods = ['GET', 'POST'])
def edit_profile():
	user = dbsession.query(Person).filter_by(id = session['user_id']).first()
	if request.method == 'GET':
		return render_template('edit_profile.html', user = user)
	else:
		new_name = request.form['fullname']
		new_username = request.form['username']
		new_password = request.form['password']
		new_gender = request.form['gender']
		new_nationality = request.form['nationality']
		new_bio = request.form['bio']

		user.name = new_name
		user.username = new_username
		user.password = new_password
		user.gender = new_gender
		user.nationality = new_nationality
		user.bio = new_bio

		dbsession.commit()
		return redirect(url_for('profile', user_id = user.id))



if __name__ == '__main__':
	app.run(debug=True)
