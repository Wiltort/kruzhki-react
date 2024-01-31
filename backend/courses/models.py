from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Rubric(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='rubric/', blank=True, null = True)

    def __str__(self):
        return self.name


class Stud_Group(models.Model):
    name = models.CharField(verbose_name='Группа', unique=True, max_length=50)
    title = models.CharField(verbose_name='Название курса', max_length=150)
    image = models.ImageField(upload_to='group/', blank=True, null = True)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, 
                                related_name='work_groups', 
                                verbose_name='Преподаватель', 
                                limit_choices_to={'is_staff': True})
    description = models.TextField(verbose_name='Описание', 
                                   blank=True)
    number_of_lessons = models.SmallIntegerField()
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, 
                               related_name='stud_groups')
    

class Student(models.Model):
    user = models.ForeignKey(User, related_name='study',
                             limit_choices_to={'is_staff': False},
                             on_delete=models.PROTECT)
    in_group = models.ForeignKey(Stud_Group, related_name='students', 
                                 on_delete=models.PROTECT)


class Lesson(models.Model):
    stud_group = models.ForeignKey(Stud_Group, related_name='lessons',
                                   verbose_name='Занятия', 
                                   on_delete=models.PROTECT)
    date = models.DateTimeField(verbose_name='Время и дата')
    topic = models.CharField(max_length=150)
    

class Attending(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='attending', 
                               on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='attending',
                                on_delete=models.DO_NOTHING)
    is_present = models.BooleanField(verbose_name='Посещение')
    is_passed = models.BooleanField(verbose_name='Зачет')
    points = models.SmallIntegerField(verbose_name='Оценка', 
                                      blank=True, null=True)


class Schedule(models.Model):
    class Days(models.IntegerChoices):
        MONDAY = 0, 'Понедельник'
        TUESDAY = 1, 'Вторник'
        WEDNESDAY = 2, 'Среда'
        THURSDAY = 3, 'Четверг'
        FRIDAY = 4, 'Пятница'
        SATURDAY = 5, 'Суббота'
        SUNDAY = 6, 'Воскресенье'

    import datetime
    group = models.ForeignKey(Stud_Group, related_name='schedule',
                              on_delete=models.PROTECT)
    day_of_week = models.SmallIntegerField(choices=Days.choices)
    duration = models.DurationField(default=datetime.timedelta(minutes=45))
    begin_at = models.TimeField()
