import csv
import logging
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from courses.models import Ring
import datetime as dt

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
)

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='rings.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA_ROOT, options['filename']),
                newline='',
                encoding='utf8'
            ) as csv_file:
                data = csv.reader(csv_file)
                for row in data:
                    number, tst = row
                    t=dt.datetime.strptime(tst, '%H:%M')
                    Ring.objects.get_or_create(
                        number=int(number),
                        begin_at=t,
                        end_at=t+dt.timedelta(minutes=settings.DEFAULT_LESSON_DURATION)
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл rings в директорию data')
        logging.info('Successfully loaded all data into database')
