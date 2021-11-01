from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Movies
from .forms import MovieForm

# Create your views here.
def populate(request):
    movies = [
        Movies(episode_nb=1,
               title="The Phantom Menace",
               director="George Lucas",
               producer="Rick McCallum",
               release_date="1999-05-19"),
        Movies(episode_nb=2,
               title="Attack of the Clones",
               director="George Lucas",
               producer="Rick McCallum",
               release_date="2002-05-16"),
        Movies(episode_nb=3,
               title="Revenge of the Sith",
               director="George Lucas",
               producer="Rick McCallum",
               release_date="2005-05-19"),
        Movies(episode_nb=4,
               title="A New Hope",
               director="George Lucas",
               producer="Gary Kurtz, Rick McCallum",
               release_date="1977-05-25"),
        Movies(episode_nb=5,
               title="The Empire Strikes Back",
               director="Irvin Kershner",
               producer="Gary Kurtz, Rick McCallum",
               release_date="1980-05-17"),
        Movies(episode_nb=6,
               title="Return of the Jedi",
               director="Richard Marquand",
               producer="Howard G. Kazanjian, George Lucas, Rick McCallum",
               release_date="1983-05-25"),
        Movies(episode_nb=7,
               title="The Force Awakens",
               director="J. J. Abrams",
               producer="Kathleen Kennedy, J. J. Abrams, Bryan Burk",
               release_date="2015-12-11"),
    ]
    error_index = 0
    try:
        for m in movies:
            m.save()
            error_index += 1
    except Exception as error:
        messages = []
        for i in range(len(movies)):
            if i != error_index:
                messages.append(str(movies[i]) + " OK")
            else:
                messages.append(str(movies[i]) + " ERROR")
                messages.append(str(error))
                break
        return render(request, "ex07/page.html", {
            'title': "ex07 populate",
            'messages':  messages,
        })
    messages = []
    for m in movies:
        messages.append(str(m) + " OK")
    return render(request, "ex07/page.html", {
        'title': "ex07 populate",
        'messages':  messages,
    })


def display(request):
    movies = None

    try:
        movies = Movies.objects.all()
    except Exception as error:
        return render(request, "ex07/page.html", {
            'title': "ex07 populate",
            'messages':  ["No data available"],
        })

    if movies:
        return render(request, 'ex07/display.html', {'movies': movies})
    return render(request, "ex07/page.html", {
        'title': "ex07 populate",
        'messages':  ["No data available"],
    })


def update(request):
    movies = []
    try:
        movies = Movies.objects.all()
    except Exception as error:
        return render(request, "ex06/page.html", {
            'title': "ex06 display",
            'messages':  ["No data available"],
        })

    if request.method == "POST":
        movie_ep = request.POST.get('movie_name')
        opening_crawl = request.POST.get('opening_crawl')
        try:
            movie = movies.filter(episode_nb = movie_ep)
            movie.update(opening_crawl = opening_crawl)
        except Exception as error:
            print(error)
            return render(request, "ex06/page.html", {
                'title': "ex06 display",
                'messages':  ["No data available"],
            })

    titles_enum = []
    for m in movies:
       titles_enum.append((str(m.episode_nb), m.title))
    form = MovieForm(choices=titles_enum)
    return render(request, 'ex06/update.html', {'form': form})

