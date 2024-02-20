from django.db import models
from users.models import User
import datetime
from django.core.validators import MinValueValidator
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


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
        verbose_name='Изображение'
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
            MinValueValidator(1, 'Минимальное значение: 1 час')
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
    begin_at = models.DateTimeField(
        verbose_name='Начало обучения',
        db_index=True
    )
    
    class Meta:
        verbose_name = 'Группа обучения'
        verbose_name_plural = 'Группы обучения'
        ordering = ('begin_at')
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    stud_group = models.ForeignKey(Stud_Group, related_name='lessons',
                                   verbose_name='Занятия', 
                                   on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Время и дата')
    topic = models.CharField(max_length=150)
    

class Attending(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='attending', 
                               on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='attending',
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

    class Rings(models.IntegerChoices):
    

    group = models.ForeignKey(Stud_Group, related_name='schedule',
                              on_delete=models.CASCADE)
    day_of_week = models.SmallIntegerField(choices=Days.choices)
    duration = models.DurationField(default=datetime.timedelta(minutes=45))
    begin_at = models.TimeField()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('group', 'day_of_week', 'begin_at')
            )
        )


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