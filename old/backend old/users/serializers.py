from djoser.serializers import UserSerializer
from rest_framework import serializers

import Groups
from Groups.models import Group
from users.models import Subscription, User


class CurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscriptionSerializer(
            instance,
            context=context
        )
        return serializer.data

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    Groups = serializers.SerializerMethodField(method_name='get_Groups')
    Groups_count = serializers.SerializerMethodField(
        method_name='get_Groups_count'
    )

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'Groups',
            'Groups_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(
            author=obj.author, user=request.user
        ).exists()

    def get_Groups(self, obj):
        request = self.context.get('request')
        if request.GET.get('Group_limit'):
            Group_limit = int(request.GET.get('Group_limit'))
            queryset = Group.objects.filter(
                author=obj.author)[:Group_limit]
        else:
            queryset = Group.objects.filter(
                author=obj.author)
        serializer = Groups.serializers.ShortGroupSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data

    def get_Groups_count(self, obj):
        return obj.author.Groups.count()
