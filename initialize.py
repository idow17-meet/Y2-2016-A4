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
				gender = 'Male',
				nationality = 'Italian',
				bio = 'I identify as a chair because why not',
				rating = 4,
				pic = "http://www.ikea.com/gb/en/images/products/kaustby-chair__21141_PE106141_S4.JPG")

loai = Person(name = 'Loai Qubti',
			  username = 'Loai',
			  password = 'yoyoyo',
			  gender = 'Male',
			  nationality = 'Palestinian',
			  bio = 'I love potatoes because cucumbers suck.',
			  rating = 5,
			  pic = "https://scontent.xx.fbcdn.net/v/t1.0-9/12247079_10205214049643216_7082800669741656003_n.jpg?oh=8953d14625b2e431401f6937c1902945&oe=581CD9E7")

haitham = Person(name = 'Haitham Slaibi',
			  username = 'Haitham123',
			  password = 'yoyoyo',
			  gender = 'Male',
			  nationality = 'Palestinian',
			  bio = 'My name is haitham and i suck at cs.',
			  rating = 5,
			  pic = "https://pbs.twimg.com/profile_images/570909929034231809/qDzErwpM.jpeg")

basel = Person(name = 'Basel Zoabi',
			  username = 'bslz1',
			  password = 'yoyoyo',
			  gender = 'Male',
			  nationality = 'Palestinian',
			  bio = 'this is my bio;););)',
			  rating = 5,
			  pic = "https://pbs.twimg.com/profile_images/516967068235616256/HkUPCFR-.jpeg")

ido = Person(name = 'Ido Wiernik',
			  username = 'SpacePotato',
			  password = 'baselisgood',
			  gender = 'Male',
			  nationality = 'Israeli',
			  bio = 'I almost died from fake cpr. #true_story',
			  rating = 5,
			  pic = "https://scontent.xx.fbcdn.net/v/t1.0-9/12046810_10205305929344845_6544716097861058090_n.jpg?oh=46635abb7720ca60a4a1c044a0ff4048&oe=5827130D")

juan = Person(name = 'Juan uno',
			  username = 'JuanTime',
			  password = 'yoyoyo',
			  gender = 'Male',
			  nationality = 'Mexican',
			  bio = 'I once got a bike and then it transformed into a Harley sickkk motorcycle !',
			  rating = 5,
			  pic = "http://media1.fdncms.com/chicago/imager/juan-rangel/u/original/8820314/1361207745-uno-cst-xxxxxx_6_25940347.jpg")

nada = Person(name = 'Nada Swedan',
			  username = 'nadaswedan',
			  password = 'yoyoyo',
			  gender = 'Female',
			  nationality = 'Palestinian',
			  bio = 'I am the blessing brought to you in this website by myself.',
			  rating = 5,
			  pic = "https://scontent.xx.fbcdn.net/t31.0-8/s960x960/10295451_1419527308062905_5297607489767182360_o.jpg")


pizza_event = Event(title = 'Awesome Pizza Party',
    				date = datetime(2016, 8, 10),
    				description = 'Come learn how to make good pizza! Antonio will be there!',
    				location = "Ehad Haam, Rehavia, Jerusalem, Israel",
    				owner_id = antonio.id,
    				owner = antonio)


pizza_event_attendance1 = Attendance(person_id = antonio.id,
						   person = antonio,
						   event_id = pizza_event.id,
						   event = pizza_event,
						   chef_flag = True)

shakshuka_event = Event(title = 'Shakshuka workshop',
    				date = datetime(2016, 6, 12),
    				description = "Shakshuka learning workshop in the park , don't hesitate to come! ",
    				location = "SomePark , Nazareth ilit, Israel",
    				owner_id = ido.id,
    				owner = ido)


shakshuka_event_attendance1 = Attendance(person_id = ido.id,
						   person = ido,
						   event_id = shakshuka_event.id,
						   event = shakshuka_event,
						   chef_flag = True)


dawali_event = Event(title = 'Kusa and Dawali for everyone!',
    				date = datetime(2016, 9, 4),
    				description = "Come and learn how to make the famous palestinian dish 'Kusa and Dawali' !",
    				location = "Jerusalem , Israel",
    				owner_id = haitham.id,
    				owner = haitham)


dawali_event_attendance1 = Attendance(person_id = haitham.id,
						   person = haitham,
						   event_id = dawali_event.id,
						   event = dawali_event,
						   chef_flag = True)

session.query(Person).delete()
session.query(Event).delete()
session.query(Attendance).delete()

session.add(antonio)
session.add(loai)
session.add(nada)
session.add(haitham)
session.add(basel)
session.add(ido)
session.add(juan)
session.add(pizza_event)
session.add(pizza_event_attendance1)
session.add(shakshuka_event)
session.add(shakshuka_event_attendance1)
session.add(dawali_event)
session.add(dawali_event_attendance1)
session.commit()