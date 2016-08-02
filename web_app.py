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
		return redirect('main')


@app.route('/main')
def main():
	return render_template('main_page.html')


@app.route('/create', methods = ['GET', 'POST'])
def create():
	if request.method == 'GET':
		return render_template('create_account.html')
	else:
		# ADD CREATING ACCOUNT AND ALL THAT GOOD STUFF HERE!!!
		return redirect('login')




if __name__ == '__main__':
	app.run(debug=True)
