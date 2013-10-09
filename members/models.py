from django.db import models
from django.contrib.auth.models import User

class MeetingAttendance(models.Model):
    MEETINGS = (
        (0, 'General'),
        (1, 'Ecomm'),
    )
    member = models.ForeignKey(User)
    type = models.IntegerField(max_length=1, choices=MEETINGS)
    date = models.DateField()

class WorkHour(models.Model):
    member = models.ForeignKey(User)
    hours = models.DecimalField(max_digits=3, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    approved = models.BooleanField()

class ClassAttendance(models.Model):
    CLASSES = (
        (0, 'Tech'),
        (1, 'Policy'),
        (2, 'Logs'),
    )
    member = models.ForeignKey(User)
    type = models.IntegerField(max_length=1, choices=CLASSES)
    date = models.DateField()

class Exam(models.Model):
    EXAMS = (
        (0, 'Tech'),
        (1, 'Policy'),
        (2, 'Logs'),
    )
    member = models.ForeignKey(User)
    type = models.IntegerField(max_length=1, choices=EXAMS)
    date = models.DateField()
    passed = models.BooleanField()

class Show(models.Model):
    DAYS = (
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    )
    TIMES = (
        (0, '5:00 AM'),
        (1, '6:00 AM'),
        (2, '7:00 AM'),
        (3, '8:00 AM'),
        (4, '9:00 AM'),
        (5, '10:00 AM'),
        (6, '11:00 AM'),
        (7, '12:00 PM'),
        (8, '1:00 PM'),
        (9, '2:00 PM'),
        (10, '3:00 PM'),
        (11, '4:00 PM'),
        (12, '5:00 PM'),
        (13, '6:00 PM'),
        (14, '7:00 PM'),
        (15, '8:00 PM'),
        (16, '9:00 PM'),
        (17, '10:00 PM'),
        (18, '11:00 PM'),
        (19, '12:00 AM'),
        (20, '1:00 AM'),
        (21, '2:00 AM'),
        (22, '3:00 AM'),
        (23, '4:00 AM'),
    )
    GENRES = (
        (0, 'Satellite Program'),
        (1, 'Variety'),
        (2, 'News/Talk Radio'),
        (3, 'Rock'),
        (4, 'Indie/Electronic'),
        (5, 'Jazz/Blues'),
        (6, 'Hip Hop/Reggae/Funk'),
        (7, 'Folk/Americana/Jam Band'),
        (8, 'Religious/Spiritual/Cultural'),
    )
    member = models.ForeignKey(User)
    name = models.CharField(max_length=64)
    host = models.CharField(max_length=64)
    description = models.TextField()
    genre = models.IntegerField(max_length=1, choices=GENRES)
    day = models.IntegerField(max_length=1, choices=DAYS)
    start_time = models.IntegerField(max_length=2, choices=TIMES)
    end_time = models.IntegerField(max_length=2, choices=TIMES)
    approved = models.BooleanField()
    scheduled = models.BooleanField()
    def __unicode__(self):
        return u'%s' % (self.name)

class Shadow(models.Model):
    member = models.ForeignKey(User)
    show = models.ForeignKey(Show)
    date = models.DateField()
