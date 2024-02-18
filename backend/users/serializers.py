from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import User


class CurrentUserSerializer(UserSerializer):
    #study = serializers.ReadOnlyField(many = True, read_only = True)
    #work_groups = serializers.ReadOnlyField(source='work_groups')

    class Meta:
        model = User
        fields = (
            'email',
            'id', 
            'username',
            'first_name',
            'last_name',
        )

        #Добавить поля work_groups, student, joinings...

    