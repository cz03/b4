import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
	__tablename__ = "user"

	id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.REAL)

class Athlete(Base):
	__tablename__ = "athelete"

	id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
	age = sa.Column(sa.Integer)
	birthdate = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	height = sa.Column(sa.REAL)
	name = sa.Column(sa.Text)
	weight = sa.Column(sa.Integer)
	gold_medals = sa.Column(sa.Integer)
	silver_medals = sa.Column(sa.Integer)
	bronze_medals = sa.Column(sa.Integer)
	total_medals = sa.Column(sa.Integer)
	sport = sa.Column(sa.Text)
	country = sa.Column(sa.Text)


def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	Session = sessionmaker(engine)
	session = Session()

	return session


def choose_gender(number):
	if number == "1":
		return "Male"
	elif number == "2":
		return "Female"

def main():
	session = connect_db()

	mode = input("Выберите протокол, 1 - Регистрация нового пользователя, 2 - Поиск пользователя: ")

	if mode == "1":
		print("\nРегистрация нового пользователя.\n")
		first_name = input("Введите ваше имя: ")
		last_name = input("Введите вашу фамилию: ")
		gender = choose_gender(input("Укажите ваш пол, 1 - Мужчина, 2 - Женщина: "))
		email = input("Укажите вашу почту: ")
	
		birthdate = input("Введите вашу дату рождения в формате ГГГГ-ММ-ДД: ")
		height = input("Укажите ваш рост: ")
	
		user = User(
			first_name = first_name,
			last_name = last_name,
			gender = gender,
			email = email,
			birthdate = birthdate,
			height = height
		)

		session.add(user)
		session.commit()

		print("Спасибо, данные записаны!")

	elif mode == "2":

		user_id = input("Введите id пользователя: ")
		query = session.query(User).filter(User.id == user_id)
		for each in query:
			print(each.id, each.first_name, each.last_name)



if __name__ == "__main__":
	main()
