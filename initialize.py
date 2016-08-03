from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Person, Event, Attendance
from datetime import datetime

engine = create_engine('sqlite:///project.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# You can add some starter data for your database here.

antonio = Person(name = 'Antonio Delegrassi',
				username = 'sexyantonio668',
				password = 'mynameisantonio',
				gender = 'identifies as a chair',
				nationality = 'Italian',
				bio = 'I identify as a chair because why not',
				rating = 4.5)


pizza_event = Event(title = 'Awesome Pizza Party',
    				date = datetime(2016, 8, 10),
    				description = 'Come learn how to make good pizza! Antonio will be there!')


antonio_pizza = Attendance(person_id = antonio.id,
						   person = antonio,
						   event_id = pizza_event.id,
						   event = pizza_event,
						   chef_flag = True)

session.query(Person).delete()
session.query(Event).delete()
session.query(Attendance).delete()

session.add(antonio)
session.add(pizza_event)
session.add(antonio_pizza)
session.commit()