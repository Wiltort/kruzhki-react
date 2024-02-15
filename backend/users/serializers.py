from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
#from courses.serializers import Stud_GroupSerializer, StudentSerializer


User = get_user_model()


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

    