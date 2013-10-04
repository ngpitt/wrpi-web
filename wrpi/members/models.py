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
    approved = models.BooleanField()

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
    approved = models.BooleanField()

class Exam(models.Model):
    EXAMS = (
        (0, 'Tech'),
        (1, 'Policy'),
        (2, 'Logs'),
    )
    member = models.ForeignKey(User)
    type = models.IntegerField(max_length=1, choices=EXAMS)
    date = models.DateField()
    score = models.IntegerField(max_length=3)
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
        (0, '0500'),
        (1, '0600'),
        (2, '0700'),
        (3, '0800'),
        (4, '0900'),
        (5, '1000'),
        (6, '1100'),
        (7, '1200'),
        (8, '1300'),
        (9, '1400'),
        (10, '1500'),
        (11, '1600'),
        (12, '1700'),
        (13, '1800'),
        (14, '1900'),
        (15, '2000'),
        (16, '2100'),
        (17, '2200'),
        (18, '2300'),
        (19, '2400'),
        (20, '2500'),
        (21, '2600'),
        (22, '2700'),
        (23, '2800'),
        (24, '2900'),
    )
    GENRES = (
        (1, 'Satellite Program'),
        (2, 'Variety'),
        (3, 'News/Talk Radio'),
        (4, 'Rock'),
        (5, 'Indie/Electronic'),
        (6, 'Jazz/Blues'),
        (7, 'Hip Hop/Reggae/Funk'),
        (8, 'Folk/Americana/Jam Band'),
        (9, 'Religious/Spiritual/Cultural'),
    )
    member = models.ForeignKey(User)
    show_name = models.CharField(max_length=64)
    host_name = models.CharField(max_length=64)
    description = models.TextField()
    genre = models.IntegerField(max_length=1, choices=GENRES)
    day = models.IntegerField(max_length=1, choices=DAYS)
    start_time = models.IntegerField(max_length=2, choices=TIMES)
    end_time = models.IntegerField(max_length=2, choices=TIMES)
    approved = models.BooleanField()
    scheduled = models.BooleanField()
