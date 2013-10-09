from django.shortcuts import render
from members.models import Show

class Schedule(object):
    def __init__(self, name='', host='', genre='Empty', description='', rowspan=1):
        self.name = name
        self.host = host
        self.genre = genre
        self.description = description
        self.rowspan = rowspan

def home(request):
    return render(request, 'public/home.html')

def schedule(request):
    shows = [[] for x in range(24)]
    rowspan = [[False for x in range(7)] for x in range(24)] 
    for i in range(24):
        for j in range(7):
            show = Show.objects.filter(scheduled=True, day=j, start_time=i)
            if show:
                shows[i].append(Schedule(show[0].name, show[0].host, show[0].get_genre_display, show[0].description, rowspan=show[0].end_time - show[0].start_time))
                for k in range(i, i + shows[i][j].rowspan):
                    rowspan[k][j] = True
            else:
                if not rowspan[i][j]:
                    shows[i].append(Schedule())
    return render(request, 'public/schedule.html', { 'shows': shows })
