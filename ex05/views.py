from django.shortcuts import render
from django.http import HttpResponse
from .models import Movies
from django.template import loader


# Create your views here.
def populate(request):
    movies = []
    if len(Movies.objects.filter(episode_nb=1)) == 0:
        movies.append(
            Movies(episode_nb=1,
                title="The Phantom Menace",
                director="George Lucas",
                producer="Rick McCallum",
                release_date="1999-05-19")
        )
    if len(Movies.objects.filter(episode_nb=2)) == 0:
        movies.append(
            Movies(episode_nb=2,
                title="Attack of the Clones",
                director="George Lucas",
                producer="Rick McCallum",
                release_date="2002-05-16")
        )
    if len(Movies.objects.filter(episode_nb=3)) == 0:
        movies.append(
            Movies(episode_nb=3,
                title="Revenge of the Sith",
                director="George Lucas",
                producer="Rick McCallum",
                release_date="2005-05-19")
        )
    if len(Movies.objects.filter(episode_nb=4)) == 0:
        movies.append(
            Movies(episode_nb=4,
                title="A New Hope",
                director="George Lucas",
                producer="Gary Kurtz, Rick McCallum",
                release_date="1977-05-25")
        )
    if len(Movies.objects.filter(episode_nb=5)) == 0:
        movies.append(
            Movies(episode_nb=5,
                title="The Empire Strikes Back",
                director="Irvin Kershner",
                producer="Gary Kurtz, Rick McCallum",
                release_date="1980-05-17")
        )
    if len(Movies.objects.filter(episode_nb=6)) == 0:
        movies.append(
            Movies(episode_nb=6,
                title="Return of the Jedi",
                director="Richard Marquand",
                producer="Howard G. Kazanjian, George Lucas, Rick McCallum",
                release_date="1983-05-25")
        )
    if len(Movies.objects.filter(episode_nb=7)) == 0:
        movies.append(
            Movies(episode_nb=7,
                title="The Force Awakens",
                director="J. J. Abrams",
                producer="Kathleen Kennedy, J. J. Abrams, Bryan Burk",
                release_date="2015-12-11")
        )
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
        return render(request, "ex05/page.html", {
            'title': "ex05 populate",
            'messages':  messages,
        })
    messages = []
    for m in movies:
        messages.append(str(m) + " OK")
    messages.append('Done')
    return render(request, "ex05/page.html", {
        'title': "ex05 populate",
        'messages':  messages,
    })


def display(request):
    movies = None

    try:
        movies = Movies.objects.all()
    except Exception as error:
        return render(request, "ex05/page.html", {
            'title': "ex05 populate",
            'messages':  ["No data available"],
        })

    if movies:
        return render(request, 'ex05/display.html', {'movies': movies})
    return render(request, "ex05/page.html", {
        'title': "ex05 populate",
        'messages':  ["No data available"],
    })


def remove(request):
    """

    :param request:
    :return:
    """
    movies = None
    try:
        if request.method == "POST":
            Movies.objects.filter(episode_nb=request.POST.get("episode_nb")).delete()

        movies = Movies.objects.all()
        if movies:
            template = loader.get_template('ex05/remove.html')
            context = {'movies': movies}
            return HttpResponse(template.render(context, request))
    except Exception as error:
        return render(request, "ex05/page.html", {
            'title': "ex05 populate",
            'messages':  ["No data available"],
        })

    return render(request, "ex05/page.html", {
        'title': "ex05 populate",
        'messages':  ["No data available"],
    })
