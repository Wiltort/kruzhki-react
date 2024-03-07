from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import User
from courses.models import Message, Joining


class CurrentUserSerializer(UserSerializer):
    #study = serializers.ReadOnlyField(many = True, read_only = True)
    #work_groups = serializers.ReadOnlyField(source='work_groups')
    messages_number = serializers.SerializerMethodField(method_name='get_messages_number')
    class Meta:
        model = User
        fields = (
            'email',
            'id', 
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'messages_number',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True},
                        'messages_number': {'read_only': True}}

    def get_messages_number(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            if user.is_staff:
                return Message.objects.filter(to=user).count()+Joining.objects.filter(group__teacher=user).count()
            return Message.objects.filter(to=user).count()
        return 0
    

        #Добавить поля work_groups, student, joinings...

    