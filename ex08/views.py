from django.http.response import HttpResponse
from django.shortcuts import render

import psycopg2
from psycopg2 import Error

# Create your views here.
def init(request):
	connection = None
	cursor = None
	try:
		connection = psycopg2.connect(
			user="djangouser",
			password="secret",
			host="127.0.0.1",
			port="5432",
			database="djangotraining"
		)
		cursor = connection.cursor()

		create_table_1_query = '''
			CREATE TABLE IF NOT EXISTS ex08_planets (
				id SERIAL PRIMARY KEY,
				name VARCHAR(64) UNIQUE NOT NULL,
				climate VARCHAR,
				diameter INT,
				orbital_period INT,
				population BIGINT,
				rotation_period INT,
				surface_water REAL,
				terrain VARCHAR(128)
			);'''
		cursor.execute(create_table_1_query)

		create_table_2_query = '''
			CREATE TABLE IF NOT EXISTS ex08_people (
				id SERIAL PRIMARY KEY,
				name VARCHAR(64) UNIQUE NOT NULL,
				birth_year VARCHAR(32),
				gender VARCHAR(32),
				eye_color VARCHAR(32),
				hair_color VARCHAR(32),
				height INT,
				mass REAL,
				homeworld VARCHAR(64) REFERENCES ex08_planets(name)
			);'''
		cursor.execute(create_table_2_query)

		connection.commit()

	except (Exception, Error) as error:
		return render(request, "ex08/page.html", {
			'title': "ex08 init",
			'messages': ["Database error: " + str(error)],
		})
	finally:
		if cursor and connection:
			cursor.close()
			connection.close()
	return render(request, "ex08/page.html", {
			'title': "ex08 init",
			'messages': ["Ok"],
		})


def populate(request):
	connection = None
	cursor = None
	people = []
	planets = []
	try:
		connection = psycopg2.connect(
			user="djangouser",
			password="secret",
			host="127.0.0.1",
			port="5432",
			database="djangotraining"
		)
		cursor = connection.cursor()
		cur_dir = __file__.replace('ex08/views.py', '')
		cursor.copy_from(
			open(cur_dir + 'planets.csv', 'r'),
			'ex08_planets',
			null='NULL',
			columns=(
				'name',
				'climate',
				'diameter',
				'orbital_period',
				'population',
				'rotation_period',
				'surface_water',
				'terrain'
			)
		)
		cursor.copy_from(
			open(cur_dir + 'people.csv', 'r'),
			'ex08_people',
			null='NULL',
			columns=(
				"name",
				"birth_year",
				"gender",
				"eye_color",
				"hair_color",
				"height",
				"mass",
				"homeworld"
			)
		)
		connection.commit()

		cursor.execute("SELECT * FROM ex08_people")
		people = cursor.fetchall()

		cursor.execute("SELECT * FROM ex08_planets")
		planets = cursor.fetchall()
	except (Exception, Error) as error:
		return render(request, "ex08/page.html", {
			'title': "ex08 init",
			'messages': ["Database error: " + str(error)],
		})
	finally:
		if cursor and connection:
			cursor.close()
			connection.close()
	messages = [str(x) + ' OK' for x in people + planets]
	return render(request, "ex08/page.html", {
			'title': "ex08 init",
			'messages': messages,
		})


def display(request):
	connection = None
	cursor = None
	records = None
	try:
		connection = psycopg2.connect(user="djangouser",
										password="secret",
										host="127.0.0.1",
										port="5432",
										database="djangotraining")
		cursor = connection.cursor()

		cursor.execute('''
		SELECT ex08_people.name, homeworld, climate
		FROM ex08_planets, ex08_people
		WHERE homeworld = ex08_planets.name AND climate LIKE '%windy%'
		ORDER BY ex08_people.name;
		''')
		records = cursor.fetchall()

	except (Exception, Error) as error:
		return render(request, "ex08/page.html", {
			'title': "ex08 display",
			'messages':  ["No data available"],
		})
	finally:
		if cursor and connection:
			cursor.close()
			connection.close()

	if records:
		return render(request, 'ex08/display.html', {'records': records})
	else:
		return render(request, "ex08/page.html", {
			'title': "ex08 display",
			'messages':  ["No data available"],
		})
