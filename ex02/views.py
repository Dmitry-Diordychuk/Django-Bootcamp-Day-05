"""
Ex02 views
"""
from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
from psycopg2 import Error


# Create your views here.
def init(request):
    """
    Create ex00_movies table in djangotraining database.
    episode_nb      INT             UNIQUE NOT NULL,       <-KEY
    title           VARCHAR(64)     UNIQUE NOT NULL,
    opening_crawl   TEXT,
    director        VARCHAR(32)     NOT NULL,
    producer        VARCHAR(128)    NOT NULL,
    release_date    DATE            NOT NULL,
    :param request: HttpRequest
    :return: 'OK' or Error description Http Response
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="djangouser",
                                      password="secret",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="djangotraining")
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS ex02_movies (
                                  episode_nb INT UNIQUE NOT NULL,
                                  title VARCHAR(64) UNIQUE NOT NULL,
                                  opening_crawl TEXT,
                                  director VARCHAR(32) NOT NULL,
                                  producer VARCHAR(128) NOT NULL,
                                  release_date DATE NOT NULL,
                                  PRIMARY KEY (episode_nb)
                                );'''
        cursor.execute(create_table_query)
        connection.commit()

    except (Exception, Error) as error:
        return render(request, "ex02/page.html", {
            'title': "ex00 init",
            'messages': ["Database error: " + str(error)],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()
    return render(request, "ex02/page.html", {
        'title': "ex00 init",
        'messages':  ["Ok"],
    })


def populate(request):
    """

    :param request: HttpRequest
    :return:
    """
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
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
               VALUES (1, 'The Phantom Menace', 'George Lucas', 'Rick McCallum', '1999-05-19')
            """,
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
               VALUES (2, 'Attack of the Clones', 'George Lucas', 'Rick McCallum', '2002-05-16')
            """,
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
               VALUES (3, 'Revenge of the Sith', 'George Lucas', 'Rick McCallum', '2005-05-19')
            """,
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
               VALUES (4, 'A New Hope', 'George Lucas', 'Gary Kurtz, Rick McCallum', '1977-05-25')
            """,
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
               VALUES (5, 'The Empire Strikes Back', 'Irvin Kershner', 'Gary Kurtz, Rick McCallum', '1980-05-17')
            """,
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
               VALUES (6, 'Return of the Jedi', 'Richard Marquand', 'Howard G. Kazanjian, George Lucas, Rick McCallum', '1983-05-25')
            """,
            """INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
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
            return render(request, "ex02/page.html", {
                'title': "ex02 populate",
                'messages':  messages,
            })
        return render(request, "ex02/page.html", {
            'title': "ex02 populate",
            'messages': ["Database error: " + str(error)],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()
    messages = []
    for q in insert_queries:
        messages.append(q + " OK")
    return render(request, "ex02/page.html", {
        'title': "ex02 populate",
        'messages':  messages,
    })


def display(request):
    """

    :param request: HttpRequest
    :return:
    """
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

        cursor.execute("SELECT * from ex02_movies")
        records = cursor.fetchall()

    except (Exception, Error) as error:
        return render(request, "ex02/page.html", {
            'title': "ex02 display",
            'messages':  ["No data available"],
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()

    if records:
        return render(request, 'ex02/display.html', {'records': records})
    else:
        return render(request, "ex02/page.html", {
            'title': "ex02 display",
            'messages':  ["No data available"],
        })
