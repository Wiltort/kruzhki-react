from django.db import models
from users.models import User
import datetime as dt
from django.core.validators import MinValueValidator
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class Rubric(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name = 'Название',
        help_text='Введите название рубрики'
        )
    image = models.ImageField(
        upload_to='rubric/', 
        blank=True, 
        null = True,
        verbose_name='Изображение',
        help_text='Загрузите изображение для рубрики'
        )
    slug = models.SlugField(
        max_length = 50,
        unique = True,
        verbose_name = 'Слаг',
        help_text = 'Введите слаг'
    )
    
    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return self.name


class Stud_Group(models.Model):
    name = models.CharField(
        verbose_name='Номер', 
        unique=True, 
        max_length=50,
        help_text='Введите номер группы'
        )
    title = models.CharField(
        verbose_name='Название курса',
        max_length=150,
        help_text='Введите название курса'
        )
    image = models.ImageField(
        upload_to='groups/',
        verbose_name='Изображение',
        default='../media/groups/1706241413450.jpeg'
        )
    teacher = models.ForeignKey(
        User, on_delete=models.PROTECT, 
        related_name='work_groups', 
        verbose_name='Преподаватель', 
        limit_choices_to={'is_staff': True}
        )
    description = models.TextField(verbose_name='Описание', 
                                   blank=True)
    number_of_lessons = models.SmallIntegerField(
        null=False,
        verbose_name='Количество часов',
        help_text='Введите количество часов',
        validators=(
            MinValueValidator(1, 'Минимальное значение: 1 час'),
        ),
    )
    rubric = models.ManyToManyField(
        Rubric,
        db_index=True,
        related_name='stud_groups',
        verbose_name='Рубрика')
    students = models.ManyToManyField(
        User, 
        related_name='stud_groups',
        verbose_name='Студенты',
        limit_choices_to={'is_staff': False})
    begin_at = models.DateField(
        verbose_name='Начало обучения',
        db_index=True,
        default=now().date()
    )
    
    class Meta:
        verbose_name = 'Группа обучения'
        verbose_name_plural = 'Группы обучения'
        ordering = ('begin_at',)
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    stud_group = models.ForeignKey(Stud_Group, related_name='lessons',
                                   verbose_name='Урок', 
                                   on_delete=models.CASCADE)
    ldate = models.DateTimeField(verbose_name='Время и дата')
    topic = models.CharField(
        max_length=250, 
        default = 'Введите тему урока',
        verbose_name='Тема')
    
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('stud_group', 'ldate'),
                name='un_lesson'
            ),
        )
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('ldate',)
    
    def __str__(self):
        return f'{self.ldate}'
    

class Attending(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='attending', 
                               on_delete=models.CASCADE,db_index=True)
    student = models.ForeignKey(User, related_name='attending',
                                on_delete=models.DO_NOTHING)
    is_present = models.BooleanField(verbose_name='Посещение',
                                     default=True)
    is_passed = models.BooleanField(verbose_name='Зачет',
                                    default=False)
    points = models.SmallIntegerField(verbose_name='Оценка', 
                                      blank=True, null=True)
    
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('lesson', 'student'),
                name='unique_attending'
            ),
        )
        verbose_name = 'Отметки'
        verbose_name_plural = 'Отметки'
        ordering = ('student',)


class Ring(models.Model):
    number = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name='Номер урока',
        validators=(
            MinValueValidator(1, message='Номер урока начинается с 1'),
            ),
        )
    begin_at = models.TimeField(verbose_name='Начало урока')
    end_at = models.TimeField('Конец урока')
    
    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Звонки'
        ordering = ('number',)

    def __str__(self):
        return f'{self.number}. {self.begin_at} - {self.end_at}'

    
class Schedule_item(models.Model):
    class Days(models.IntegerChoices):
        MONDAY = 0, 'Понедельник'
        TUESDAY = 1, 'Вторник'
        WEDNESDAY = 2, 'Среда'
        THURSDAY = 3, 'Четверг'
        FRIDAY = 4, 'Пятница'
        SATURDAY = 5, 'Суббота'
        SUNDAY = 6, 'Воскресенье'

    day_of_week = models.SmallIntegerField(
        choices=Days.choices,
        verbose_name='День недели'
    )
    btime = models.ForeignKey(
        Ring, 
        on_delete=models.DO_NOTHING,
        related_name='planned_lessons',
        verbose_name='Время урока'
    )
    template = models.ForeignKey(
        'Schedule_template',
        on_delete = models.CASCADE,
        verbose_name='Шаблон',
        related_name='items'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('day_of_week', 'btime','template'),
                name='unique_item'
            ),
        )
        ordering = ('day_of_week', 'btime')
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Schedule_template(models.Model):
    group = models.ForeignKey(
        Stud_Group,
        on_delete=models.CASCADE,
        related_name='schedule_templates',
        verbose_name='Группа'
        )
    
    def create_lessons(self, delete_lessons_not_in_template=True):
        items = Schedule_item.objects.filter(template=self).all()
        if not items:
            return None
        d = self.group.begin_at
        wd = d.weekday()
        items = sorted(items, key=lambda x: x.day_of_week < wd)
        N = len(items)
        if delete_lessons_not_in_template:
            Lesson.objects.filter(stud_group=self.group).filter(ldate__bte=now().date()).delete()
        students=self.group.students.all()
        for i in range(self.group.number_of_lessons):
            j = i%N
            if wd == items[j].day_of_week and j==0 and i!=0:
                days = 7
            else:
                days=(items[j].day_of_week-wd)%7
            d += dt.timedelta(days=days)
            wd = d.weekday()
            lesson = Lesson.objects.create(
                stud_group=self.group,
                ldate=dt.datetime.combine(d,items[j].btime.begin_at)
            )
            for student in students:
                Attending.objects.get_or_create(
                    lesson=lesson,
                    student=student,
                )
        return Lesson.objects.prefetch_related('attending').filter(stud_group=self.group)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('group',),
                name='unique_schedule_template'
            ),
        )
        verbose_name = 'Недельное расписание'
        verbose_name_plural = 'Недельные расписания'
        ordering = ('group',)
            

class Joining(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'joining_to',
        verbose_name='Заявки на курсы',
        limit_choices_to={'is_staff': False}
        )
    group = models.ForeignKey(
        Stud_Group,
        on_delete=models.CASCADE,
        related_name='join_requests',
        verbose_name='Заявки на курс'
    )
    date = models.DateTimeField(
        'Дата заявления',
        auto_now_add=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'group'),
                name='unique_joining'
            ),
        )
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    
    def clean(self):
        errors = {}
        if self.group.students.objects.filter(pk=self.user.pk).exists():
            errors[NON_FIELD_ERRORS] = ValidationError('Уже в группе')
        if errors:
            raise ValidationError(errors)


    def __str__(self):
        return f'{self.user} submitted a request to join {self.group}'