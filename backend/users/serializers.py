from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.serializers import Stud_GroupSerializer, StudentSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    study = StudentSerializer(many = True, read_only = True)
    work_groups = Stud_GroupSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_superuser','study', 'work_groups')