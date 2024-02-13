from rest_framework import serializers
from django.contrib.auth import get_user_model
#from courses.serializers import Stud_GroupSerializer, StudentSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    #study = serializers.ReadOnlyField(many = True, read_only = True)
    #work_groups = serializers.ReadOnlyField(source='work_groups')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_superuser')