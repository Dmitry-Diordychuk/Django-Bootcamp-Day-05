import django
from django import forms
from django.shortcuts import render
import psycopg2
from psycopg2 import Error
from django.http import HttpResponse
from django.template import loader
from .forms import MovieForm

def init(request):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="djangouser",
                                      password="secret",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="djangotraining")
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS ex06_movies (
                                  episode_nb INT UNIQUE NOT NULL,
                                  title VARCHAR(64) UNIQUE NOT NULL,
                                  opening_crawl TEXT,
                                  director VARCHAR(32) NOT NULL,
                                  producer VARCHAR(128) NOT NULL,
                                  release_date DATE NOT NULL,
                                  created TIMESTAMPTZ NOT NULL DEFAULT Now(),
                                  updated TIMESTAMPTZ NOT NULL DEFAULT Now(),
                                  PRIMARY KEY (episode_nb)
                                );'''
        cursor.execute(create_table_query)

        create_update_function = '''CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                                    RETURNS TRIGGER AS $$
                                    BEGIN
                                        NEW.updated = now();
                                        NEW.created = OLD.created;
                                        RETURN NEW;
                                    END;
                                    $$ language 'plpgsql';'''
        cursor.execute(create_update_function)

        create_update_trigger = '''CREATE TRIGGER update_films_changetimestamp
                                   BEFORE UPDATE ON ex06_movies
                                   FOR EACH ROW
                                   EXECUTE PROCEDURE update_changetimestamp_column();'''
        cursor.execute(create_update_trigger)

        connection.commit()

    except (Exception, Error) as error:
        return render(request, "ex06/page.html", {
            'title': "ex06 init",
            'messages': ["Database error: " + str(error)],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()
    return render(request, "ex06/page.html", {
        'title': "ex06 init",
        'messages':  ["Ok"],
    })


def populate(request):
    connection = None
    cursor = None
    insert_queries = None
    last_index = -1
    try:
        connection = psycopg2.connect(user="djangouser",
                                      password="secret",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="djangotraining")
        cursor = connection.cursor()

        insert_queries = [
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (1, 'The Phantom Menace', 'George Lucas', 'Rick McCallum', '1999-05-19')
            """,
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (2, 'Attack of the Clones', 'George Lucas', 'Rick McCallum', '2002-05-16')
            """,
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (3, 'Revenge of the Sith', 'George Lucas', 'Rick McCallum', '2005-05-19')
            """,
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (4, 'A New Hope', 'George Lucas', 'Gary Kurtz, Rick McCallum', '1977-05-25')
            """,
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (5, 'The Empire Strikes Back', 'Irvin Kershner', 'Gary Kurtz, Rick McCallum', '1980-05-17')
            """,
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (6, 'Return of the Jedi', 'Richard Marquand', 'Howard G. Kazanjian, George Lucas, Rick McCallum', '1983-05-25')
            """,
            """INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
               VALUES (7, 'The Force Awakens', 'J. J. Abrams', 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', '2015-12-11')
            """]

        last_index = 0
        for i in range(len(insert_queries)):
            cursor.execute(insert_queries[i])
            last_index = i + 1

        connection.commit()
    except (Exception, Error) as error:
        messages = []
        for i in range(len(insert_queries)):
            if i == last_index:
                messages.append(insert_queries[i] + " Error")
                messages.append(str(error))
                break
            else:
                messages.append(insert_queries[i] + " OK")
        if last_index != -1:
            return render(request, "ex06/page.html", {
                'title': "ex06 populate",
                'messages':  messages,
            })
        return render(request, "ex06/page.html", {
            'title': "ex06 populate",
            'messages': ["Database error: " + str(error)],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()
    messages = []
    for q in insert_queries:
        messages.append(q + " OK")
    return render(request, "ex06/page.html", {
        'title': "ex06 populate",
        'messages':  messages,
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

        cursor.execute("SELECT * from ex06_movies")
        records = cursor.fetchall()

    except (Exception, Error) as error:
        return render(request, "ex06/page.html", {
            'title': "ex06 display",
            'messages':  ["No data available"],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()

    if records:
        return render(request, 'ex06/display.html', {'records': records})
    else:
        return render(request, "ex06/page.html", {
            'title': "ex06 display",
            'messages':  ["No data available"],
        })


def update(request):
    if request.method == "POST":
        movie_ep = request.POST.get('movie_name')
        opening_crawl = request.POST.get('opening_crawl')
        try:
            connection = psycopg2.connect(
                user="djangouser",
                password="secret",
                host="127.0.0.1",
                port="5432",
                database="djangotraining"
            )
            cursor = connection.cursor()
            cursor.execute(
                '''
                UPDATE ex06_movies \
                SET opening_crawl = '{}' \
                WHERE episode_nb = {}
                '''.format(opening_crawl, movie_ep)
            )
            connection.commit()
        except (Exception, Error) as error:
            return render(request, "ex06/page.html", {
                'title': "ex06 display",
                'messages':  ["No data available"],
            })
        finally:
            if cursor and connection:
                cursor.close()
                connection.close()

    connection = None
    cursor = None
    titles = None
    try:
        connection = psycopg2.connect(user="djangouser",
                                      password="secret",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="djangotraining")
        cursor = connection.cursor()

        cursor.execute("SELECT episode_nb, title FROM ex06_movies")
        titles = cursor.fetchall()
    except (Exception, Error) as error:
        return render(request, "ex06/page.html", {
            'title': "ex06 display",
            'messages':  ["No data available"],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()

    titles_enum = []
    titles.sort(key=lambda x: x[0])
    for i in range(len(titles)):
        titles_enum.append( (str(i + 1), titles[i][1]) )
    form = MovieForm(choices=titles_enum)
    return render(request, 'ex06/update.html', {'form': form})
