from django.contrib import admin
from django.urls.resolvers import URLPattern
from users.models import User
from .models import (
    Stud_Group, Lesson, Attending, 
    Schedule_template, Rubric, Schedule_item,
    Ring, Joining)
from django.urls import path
from django.shortcuts import redirect



class RubricInline(admin.TabularInline):
    model = Rubric.stud_groups.through
    extra = 1


class RubricAdmin(admin.ModelAdmin):
    inlines = (RubricInline,)
    list_display = ('pk', 'name', 'image', 'slug', 'groups')
    search_fields = ('pk', 'name')
    readonly_fields = ('groups',)

    def groups(self, instance):
        return ', '.join(
            [g.name for g in Stud_Group.objects.filter(rubric=instance)[:3]]
            )
    groups.short_description = 'Группы'


class Stud_GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title', 'teacher','rubrics')
    search_fields = ('name', 'teacher__username', 'title')
    list_filter = ('teacher', 'rubric')
    
    def rubrics(self, instance):
        return ', '.join([a.name for a in instance.rubric.all()])
    rubrics.short_description = 'Рубрики'

class RingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'begin_at', 'end_at')

#class StudentsAdmin(admin.ModelAdmin):
#    list_display = ('pk', 'user')
#    search_fields = ('pk', 'user')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'stud_group', 'ldate', 'topic')
    search_fields = ('stud_group', 'ldate')
    list_filter = ('stud_group__name', 'ldate')


class AttendingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'lesson', 'student_display', 'is_present', 'is_passed','points')
    search_fields = ('lesson', 'student')
    list_filter = ('lesson', 'student', 'lesson__stud_group')

    def student_display(self, instance):
        return f'{instance.student.first_name} {instance.student.last_name}'

    student_display.short_description = 'Студент'

class ScheduleItemsInline(admin.TabularInline):
    model = Schedule_item
    extra = 1

class ScheduleAdmin(admin.ModelAdmin):
    inlines = (ScheduleItemsInline,)
    list_display = ('pk', 'group', 'items')
    list_filter = ('group__name', 'group__title')

    def items(self,instance):
        return ', '.join([f'{a.day_of_week}: {a.btime}' for a in instance.items.all()])
    items.short_description = 'Расписание'
    
    def get_urls(self):
        urls = super(ScheduleAdmin, self).get_urls()
        custom_urls = [
            path('forming/', self.admin_site.admin_view(self.get_schedule),name='schedule_view'),
        ]
        return custom_urls + urls
    
    def get_schedule(self, request):
        # TODO
        return redirect(f'/admin/courses/schedule_template/')
    

class JoiningAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'group', 'date')
    search_fields = ('group',)
    list_filter = ('user', 'group', 'group__teacher')
    

admin.site.register(Stud_Group, Stud_GroupAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Attending, AttendingAdmin)
admin.site.register(Schedule_template, ScheduleAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Ring, RingAdmin)
admin.site.register(Joining, JoiningAdmin)

