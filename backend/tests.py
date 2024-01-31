import pytest
import re
from django.contrib.auth import get_user_model


try:
    from courses.models import Stud_Group
except ImportError:
    assert False, 'Не найдена модель Stud_Group'