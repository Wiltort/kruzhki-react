from django.contrib import admin
from .models import User
from courses.models import Stud_Group

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_superuser',
        'is_staff',
        'work_or_study_at_group',
        )
    
    def work_or_study_at_group(self, instance):
        if instance.is_staff:
            return Stud_Group.objects.filter(teacher=instance)
        else:
            return Stud_Group.objects.filter(students=instance)
        
admin.site.register(User, UserAdmin)
            