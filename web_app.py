from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

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
session = DBSession()


#YOUR WEB APP CODE GOES HERE

# wget http://tinyurl.com/MEETpythonY2
# source MEETpythonY2


@app.route('/', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login_page.html')
	else:
		# ADD LOGIN AND ALL THAT GOOD STUFF HERE!!!
		user = session.query(Person).filter_by(username = request.form['username']).first()
		if user == None or user.password != request.form['password']: # If username doesn't exist or wrong password
			return render_template('login_page.html', error=True)
		else:
			return redirect(url_for('main'))


@app.route('/main')
def main():
	return render_template('main_page.html')


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
		session.add(user)
		session.commit()
		return redirect(url_for('login'))


@app.route('/create-event', methods = ['GET', 'POST'])
def create_event():
	if request.method == 'GET':
		return render_template('create_event.html')
	else:
		event = Event(title = request.form['title'],
			date = request.form['date'],
			description = request.form['description'])
		session.add(event)
		session.commit()
		return redirect(url_for('event'))

@app.route('/event') #Add and event id or smth
def event():
	return render_template('event_page.html')


@app.route('/profile/<int:user_id>')
def profile(user_id):
	user = session.query(Person).filter_by(id = user_id).first()
	return render_template('profile_page.html', user = user)


@app.route('/edit-profile/<int:user_id>', methods = ['GET', 'POST'])
def edit_profile(user_id):
	user = session.query(Person).filter_by(id = user_id).first()
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

		session.commit()
		return redirect(url_for('profile', user_id = user_id))



if __name__ == '__main__':
	app.run(debug=True)
