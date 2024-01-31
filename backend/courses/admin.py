from django.contrib import admin
from .models import Stud_Group, Student, Lesson, Attending, Schedule


class Stud_GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title', 'teacher')
    search_fields = ('name', 'teacher')
    list_filter = ('teacher',)


class StudentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'in_group')
    search_fields = ('pk', 'user', 'in_group')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'stud_group', 'date', 'topic')
    search_fields = ('stud_group', 'date')


class AttendingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'lesson', 'student', 'is_present', 'is_passed')
    search_fields = ('lesson', 'student')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group', 'day_of_week', 'duration', 'begin_at')


admin.site.register(Stud_Group, Stud_GroupAdmin)
admin.site.register(Student, StudentsAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Attending, AttendingAdmin)
admin.site.register(Schedule, ScheduleAdmin)
