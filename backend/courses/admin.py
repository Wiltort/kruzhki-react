from django.contrib import admin
from users.models import User
from .models import (
    Stud_Group, Lesson, Attending, 
    Schedule_template, Rubric, Schedule_item,
    Ring)


class RubricInline(admin.TabularInline):
    model = Rubric.stud_groups.through
    extra = 1


class RubricAdmin(admin.ModelAdmin):
    inlines = (RubricInline,)
    list_display = ('pk', 'name', 'image', 'slug', 'groups')
    search_fields = ('pk', 'name')
    readonly_fields = ('groups',)

    def groups(self, instance):
        return instance.stud_groups.all()


class Stud_GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title', 'teacher','rubrics')
    search_fields = ('name', 'teacher__username', 'title')
    list_filter = ('teacher', 'rubric')
    
    def rubrics(self, instance):
        return instance.rubric.all()

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
    list_display = ('pk', 'lesson', 'student', 'is_present', 'is_passed')
    search_fields = ('lesson', 'student')
    list_filter = ('lesson',)


class ScheduleItemsInline(admin.TabularInline):
    model = Schedule_item
    extra = 1

class ScheduleAdmin(admin.ModelAdmin):
    inlines = (ScheduleItemsInline,)
    list_display = ('pk', 'group', 'items')
    list_filter = ('group__name', 'group__title')

    def items(self,instance):
        return instance.items.all()


admin.site.register(Stud_Group, Stud_GroupAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Attending, AttendingAdmin)
admin.site.register(Schedule_template, ScheduleAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Ring, RingAdmin)

