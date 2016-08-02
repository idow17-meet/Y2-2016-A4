from flask import Flask, render_template
app = Flask(__name__)

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#YOUR WEB APP CODE GOES HERE

@app.route('/')
def login():
    return render_template('login_page.html')


@app.route('/main')
def main():
	return render_template('main_page.html')


@app.route('/create')
def create():
	return render_template('create_account.html')




if __name__ == '__main__':
    app.run(debug=True)
