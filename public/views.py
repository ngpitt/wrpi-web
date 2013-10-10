from django.shortcuts import render
from django.db.models import F
from members.models import Show

class TimeSlot():
    def __init__(self, time, shows):
        self.time = time
        self.shows = shows

class ScheduleItem():
    def __init__(self, name='', host='', genre='Empty', description='', row_span=1):
        self.name = name
        self.host = host
        self.genre = genre
        self.description = description
        self.row_span = row_span

def home(request):
    return render(request, 'public/home.html')

def schedule(request):
    schedule = []
    span_mask = [[False for i in range(7)] for i in range(48)]
    span_shows = Show.objects.filter(scheduled=True).exclude(start_day=F('end_day'))
    for current_time in range(48):
        shows = []
        for current_day in range(7):
            if current_time == 0:
                for show in span_shows:
                    if show.start_day < current_day and show.end_day > current_day:
                        shows.append(ScheduleItem(show.name, show.host, show.get_genre_display, show.description, row_span=48))
                        for time in range(shows[current_day].row_span):
                            span_mask[time][current_day] = True
                    if show.end_day == current_day:
                        shows.append(ScheduleItem(show.name, show.host, show.get_genre_display, show.description, row_span=show.end_time))
                        for time in range(shows[current_day].row_span):
                            span_mask[time][current_day] = True
            if not span_mask[current_time][current_day]:
                show = Show.objects.filter(scheduled=True, start_day=current_day, start_time=current_time)
                if show:
                    if show[0].start_day != show[0].end_day:
                        shows.append(ScheduleItem(show[0].name, show[0].host, show[0].get_genre_display, show[0].description, row_span=48 - show[0].start_time))
                    else:
                        shows.append(ScheduleItem(show[0].name, show[0].host, show[0].get_genre_display, show[0].description, row_span=show[0].end_time - show[0].start_time))
                    for time in range(current_time, current_time + shows[current_day].row_span):
                        span_mask[time][current_day] = True
                else:
                    shows.append(ScheduleItem())
        if current_time % 2:
            schedule.append(TimeSlot('', shows=shows))
        else:
            schedule.append(TimeSlot(time=Show.TIMES[current_time][1], shows=shows))
    return render(request, 'public/schedule.html', { 'schedule': schedule })
