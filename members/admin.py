from django.contrib import admin
from members.models import MeetingAttendance, WorkHour, ClassAttendance, Exam, Shadow, Show

class MeetingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'date')

class WorkHourAdmin(admin.ModelAdmin):
    list_display = ('member', 'hours', 'date', 'approved')

class ClassAttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'date')

class ExamAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'date', 'passed')

class ShadowAdmin(admin.ModelAdmin):
    list_display = ('member', 'show_name', 'date')
    def show_name(self, obj):
        return obj.show.name
    show_name.admin_order_field = 'show__name'

class ShowAdmin(admin.ModelAdmin):
    list_display = ('member', 'name', 'approved', 'scheduled')

admin.site.register(MeetingAttendance, MeetingAttendanceAdmin)
admin.site.register(WorkHour, WorkHourAdmin)
admin.site.register(ClassAttendance, ClassAttendanceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Shadow, ShadowAdmin)
admin.site.register(Show, ShowAdmin)
