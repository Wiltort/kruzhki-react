from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from Groups.filters import IngredientFilter, TagFilter
from Groups.models import (Favorite, Ingredient, IngredientsInGroup, Group,
                            ShoppingCart)
from Groups.pagination import CustomPagination
from Groups.permissions import IsOwnerOrReadOnly
from Groups.serializers import (AddGroupSerializer, IngredientSerializer,
                                 GroupSerializer, ShortGroupSerializer)
from Groups.utils import convert_txt


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientFilter


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GroupSerializer
        return AddGroupSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_Group(Favorite, request, pk)
        else:
            return self.delete_Group(Favorite, request, pk)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientsInGroup.objects.filter(
            Group__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        return convert_txt(ingredients)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_Group(ShoppingCart, request, pk)
        else:
            return self.delete_Group(ShoppingCart, request, pk)

    def add_Group(self, model, request, pk):
        Group = get_object_or_404(Group, pk=pk)
        user = self.request.user
        if model.objects.filter(Group=Group, user=user).exists():
            raise ValidationError('Рецепт уже добавлен')
        model.objects.create(Group=Group, user=user)
        serializer = ShortGroupSerializer(Group)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_Group(self, model, request, pk):
        Group = get_object_or_404(Group, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, Group=Group, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
