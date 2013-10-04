from django.contrib import admin
from wrpi.members.models import MeetingAttendance, WorkHour, ClassAttendance, Exam, Show

class MeetingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'date', 'approved')

class WorkHourAdmin(admin.ModelAdmin):
    list_display = ('member', 'hours', 'date', 'approved')

class ClassAttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'date', 'approved')

class ExamAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'date', 'passed')

class ShowAdmin(admin.ModelAdmin):
    list_display = ('member', 'show_name', 'approved', 'scheduled')

admin.site.register(MeetingAttendance, MeetingAttendanceAdmin)
admin.site.register(WorkHour, WorkHourAdmin)
admin.site.register(ClassAttendance, ClassAttendanceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Show, ShowAdmin)
