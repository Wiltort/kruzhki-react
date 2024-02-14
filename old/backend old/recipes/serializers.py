from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators
import users.serializers as users
from Groups.models import (Favorite, Ingredient, IngredientsInGroup, Group,
                            ShoppingCart)
from tags.models import Tag
from tags.serializers import TagField


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInGroupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInGroup
        fields = ('id', 'name', 'measurement_unit', 'amount')

    validators = (
        validators.UniqueTogetherValidator(
            queryset=IngredientsInGroup.objects.all(),
            fields=('ingredient', 'Group')
        ),
    )

    def __str__(self):
        return f'{self.ingredient} in {self.Group}'


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInGroup
        fields = ('id', 'amount')


class GroupSerializer(serializers.ModelSerializer):
    author = users.CurrentUserSerializer()
    tags = TagField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientInGroupSerializer(
        source='ingredient_in_Group',
        read_only=True, many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Group
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def in_list(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, Group=obj).exists()

    def get_is_favorited(self, obj):
        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.in_list(obj, ShoppingCart)


class AddGroupSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Group
        fields = (
            'tags',
            'name',
            'ingredients',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        serializer = GroupSerializer(instance)
        return serializer.data

    def create_ingredients(self, ingredients, Group):
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = ingredient['id']
            ingredients, created = IngredientsInGroup.objects.get_or_create(
                Group=Group,
                ingredient=ingredient,
                amount=amount
            )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Group = Group.objects.create(**validated_data)
        Group.tags.set(tags)
        Group.save()
        self.create_ingredients(ingredients, Group)
        return Group

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        instance.tags.clear()
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def validate(self, data):
        ings = data['ingredients']
        if not ings:
            raise serializers.ValidationError(
                'Поле с ингредиентами не может быть пустым'
            )
        unique_ings = []
        for ingredient in ings:
            name = ingredient['id']
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    f'Не корректное количество для {name}'
                )
            if not isinstance(ingredient['amount'], int):
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть целым числом'
                )
            if name not in unique_ings:
                unique_ings.append(name)
            else:
                raise serializers.ValidationError(
                    'В рецепте не может быть повторяющихся ингредиентов'
                )
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 минуты'
            )
        return data


class ShortGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'image', 'cooking_time')