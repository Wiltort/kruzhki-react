from django.contrib import admin
from users.models import User
from .models import Stud_Group, Lesson, Attending, Schedule, Rubric

class RubricAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'image', 'slug')
    search_fields = ('pk', 'name')


    def stud_groups(self, instance):
        return Stud_Group.objects.filter(rubric = instance)


class Stud_GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title', 'teacher')
    search_fields = ('name', 'teacher')
    list_filter = ('teacher', 'rubric')


#class StudentsAdmin(admin.ModelAdmin):
#    list_display = ('pk', 'user')
#    search_fields = ('pk', 'user')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'stud_group', 'date', 'topic')
    search_fields = ('stud_group', 'date')


class AttendingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'lesson', 'student', 'is_present', 'is_passed')
    search_fields = ('lesson', 'student')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group', 'day_of_week', 'duration', 'begin_at')


admin.site.register(Stud_Group, Stud_GroupAdmin)
#admin.site.register(Student, StudentsAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Attending, AttendingAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Rubric, RubricAdmin)

