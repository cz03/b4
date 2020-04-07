import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

import datetime

from users import User, Athlete

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

def connect_db():
	engine = sa.create_engine(DB_PATH)
	Session = sessionmaker(engine)
	session = Session()

	return session

def main():
	session = connect_db()

	user_id = input("Введите идентификатор пользователя: ")

	# Запрос пользователя из БД
	query = session.query(User).filter(User.id == user_id).first()
	# Запрос всех атлетов из БД
	atl_query = session.query(Athlete).all()

	if query:
		print("Данные пользователя: id - {}, имя - {}, фамилия - {}, дата рождения - {}, рост - {}.".format(query.id, query.first_name, query.last_name, query.birthdate, query.height))
		
		# Создание переменной даты рождения пользователя и ее подгатовка к арифметическим операциям с другими датами
		user_bday = query.birthdate.strip().split("-")
		user_bday = datetime.date(int(user_bday[0]), int(user_bday[1]), int(user_bday[2]))
		# Создание переменной роста пользователя
		user_height = query.height

		# Ввод переменной первого атлета и ее подготовка
		first_atl_bday = atl_query[0].birthdate.split("-")
		first_atl_bday = datetime.date(int(first_atl_bday[0]), int(first_atl_bday[1]), int(first_atl_bday[2]))
		# Ввод переменой разницы дат рождения атлета и пользователя
		difference = first_atl_bday - user_bday
		# Ввод списка в котором будет наиблежайший по дате рождения атлет
		min_difference = [first_atl_bday, atl_query[0].id, difference]

		# Ввод списка с ростом и айдишником первого атлета
		first_atl_height = [atl_query[0].height, atl_query[0].id]
		# Разница роста атлета и пользователя
		height_difference = first_atl_height[0] - user_height
		
		# Обход всех атлетов
		for athlete in atl_query:
			# Переменная с датой рождения текущего атлета
			atl_bday = athlete.birthdate.split("-")
			atl_bday = datetime.date(int(atl_bday[0]), int(atl_bday[1]), int(atl_bday[2]))
			# Разница дат рождения атлета и пользователя в днях
			difference = atl_bday - user_bday
			
			# Если разница в днях меньше первой разницы список и первый атлет обновляется на текущего атлета
			if abs(difference) < abs(min_difference[2]):
				min_difference[0] = atl_bday
				min_difference[1] = athlete.id
				min_difference[2] = difference

			# Переменная разницы роста текущего атлета с пользователя
			# Блок трай тут потому что не у всех атлетов указан рост
			try:
				h_difference = athlete.height - user_height
			except TypeError:
				pass

			# Если разница роста рекущего атлета и пользователя меньше первой разницы, список с ростом и айдишником обновляется
			if abs(h_difference) < abs(height_difference):
				# И переменная разницы обновляется
				height_difference = h_difference
				first_atl_height[0] = athlete.height
				first_atl_height[1] = athlete.id


		atl_with_the_same_bday = session.query(Athlete).filter(Athlete.id == min_difference[1]).first()
		print("Ближайший по дате рождения атлет: id - {}, имя - {}, дата рождения - {}.".format(atl_with_the_same_bday.id, atl_with_the_same_bday.name, atl_with_the_same_bday.birthdate))
		
		atl_with_the_same_height = session.query(Athlete).filter(Athlete.id == first_atl_height[1]).first()
		print("Ближайший по росту атлет: id - {}, имя - {}, рост - {}.".format(atl_with_the_same_height.id, atl_with_the_same_height.name, atl_with_the_same_height.height))

	# Если пользователя с введеным идентификатором не наййдено
	elif query is None:
		print("Пользователя с таким идентификатором не зарегистрировано!")


if __name__ == "__main__":
	main()