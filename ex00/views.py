"""
Views
"""
from django.http import HttpResponse
import psycopg2
from psycopg2 import Error
from django.shortcuts import render


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

        create_table_query = '''CREATE TABLE IF NOT EXISTS ex00_movies (
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

        print("WTF?")

    except (Exception, Error) as e:
        return render(request, "ex00/page.html", {
            'title': "ex00 init",
            'message': "Database error: " + str(e),
        })
    finally:
        if cursor and connection:
            cursor.close()
            connection.close()
    return render(request, "ex00/page.html", {
        'title': "ex00 init",
        'message':  "Ok",
    })
