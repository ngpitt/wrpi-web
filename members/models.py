from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class Valid(models.Model):

    @property
    def valid_through(self):
        if self.date.month <= 6:
            return date(self.date.year, 12, 31)
        else:
            return date(self.date.year + 1, 6, 30)
    @property
    def valid(self):
        return True if date.today() <= self.valid_through else False

    class Meta:
        abstract = True

class Member(AbstractUser):

    rin = models.IntegerField(max_length=9, null=True, blank=True)
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class MeetingAttendance(Valid):

    MEETINGS = (
        (0, 'General'),
        (1, 'E-Comm'),
    )

    member = models.ForeignKey(Member)
    type = models.IntegerField(max_length=1, choices=MEETINGS)
    date = models.DateField()

    def __unicode__(self):
        return u'%s on %s' % (MeetingAttendance.MEETINGS[self.type][1], self.date)

class WorkHour(Valid):

    member = models.ForeignKey(Member)
    hours = models.DecimalField(max_digits=3, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    approved = models.BooleanField()

    def __unicode__(self):
        return u'%s on %s' % (self.hours, self.date)

class ClassAttendance(models.Model):

    CLASSES = (
        (0, 'Tech'),
        (1, 'Policy'),
        (2, 'Logs'),
    )

    member = models.ForeignKey(Member)
    type = models.IntegerField(max_length=1, choices=CLASSES)
    date = models.DateField()

    def __unicode__(self):
        return u'%s on %s' % (ClassAttendance.CLASSES[self.type][1], self.date)

class Exam(Valid):

    EXAMS = (
        (0, 'Tech'),
        (1, 'Policy'),
        (2, 'Logs'),
    )

    member = models.ForeignKey(Member)
    type = models.IntegerField(max_length=1, choices=EXAMS)
    date = models.DateField()
    passed = models.BooleanField()

    @property
    def valid_through(self):
        return date(self.date.year + 2, self.date.month, self.date.day)

    def __unicode__(self):
        return u'%s on %s' % (Exam.EXAMS[self.type][1], self.date)

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
        (1, '5:30 AM'),
        (2, '6:00 AM'),
        (3, '6:30 AM'),
        (4, '7:00 AM'),
        (5, '7:30 AM'),
        (6, '8:00 AM'),
        (7, '8:30 AM'),
        (8, '9:00 AM'),
        (9, '9:30 AM'),
        (10, '10:00 AM'),
        (11, '10:30 AM'),
        (12, '11:00 AM'),
        (13, '11:30 AM'),
        (14, '12:00 PM'),
        (15, '12:30 PM'),
        (16, '1:00 PM'),
        (17, '1:30 PM'),
        (18, '2:00 PM'),
        (19, '2:30 PM'),
        (20, '3:00 PM'),
        (21, '3:30 PM'),
        (22, '4:00 PM'),
        (23, '4:30 PM'),
        (24, '5:00 PM'),
        (25, '5:30 PM'),
        (26, '6:00 PM'),
        (27, '6:30 PM'),
        (28, '7:00 PM'),
        (29, '7:30 PM'),
        (30, '8:00 PM'),
        (31, '8:30 PM'),
        (32, '9:00 PM'),
        (33, '9:30 PM'),
        (34, '10:00 PM'),
        (35, '10:30 PM'),
        (36, '11:00 PM'),
        (37, '11:30 PM'),
        (38, '12:00 AM'),
        (39, '12:30 AM'),
        (40, '1:00 AM'),
        (41, '1:30 AM'),
        (42, '2:00 AM'),
        (43, '2:30 AM'),
        (44, '3:00 AM'),
        (45, '3:30 AM'),
        (46, '4:00 AM'),
        (47, '4:30 AM'),
        (48, '5:00 AM'),
    )
    GENRES = (
        (0, 'External Programming'),
        (1, 'Variety'),
        (2, 'Rock/Pop'),
        (3, 'Electronic'),
        (4, 'Metal'),
        (5, 'Alternative/Punk'),
        (6, 'Jazz'),
        (7, 'Blues'),
        (8, 'Classical'),
        (9, 'Experimental'),
        (10, 'Folk/Bluegrass/Roots'),
        (11, 'Hip Hop/Reggae/Funk'),
        (12, 'Religious/Spiritual/Cultural'),
        (13, 'News/Talk Radio'),
    )

    member = models.ForeignKey(Member)
    name = models.CharField(max_length=64)
    host = models.CharField(max_length=64)
    description = models.TextField()
    genre = models.IntegerField(max_length=1, choices=GENRES)
    start_day = models.IntegerField(max_length=1, choices=DAYS)
    start_time = models.IntegerField(max_length=2, choices=TIMES)
    end_day = models.IntegerField(max_length=1, choices=DAYS)
    end_time = models.IntegerField(max_length=2, choices=TIMES)
    submitted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField()
    scheduled = models.BooleanField()
    shadowable = models.BooleanField()

    def __unicode__(self):
        return self.name

class Shadow(models.Model):

    member = models.ForeignKey(Member)
    show = models.ForeignKey(Show)
    date = models.DateField()
    approved = models.BooleanField()

    def __unicode__(self):
        return u'%s on %s' % (self.show, self.date)
