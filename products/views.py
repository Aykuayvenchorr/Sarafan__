from django.db.models import Sum, F
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Category, Subcategory, Product, User, CartItem
from products.serializers import CategorySerializer, SubcategorySerializer, ProductSerializer, UserSerializer, \
    CartItemSerializer, UserCreateSerializer


class CategoryViewSet(ModelViewSet):
    """Эндпоинт для просмотра всех категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(ModelViewSet):
    """Эндпоинт для просмотра всех подкатегорий"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ProductViewSet(ModelViewSet):
    """Эндпоинт для просмотра всех продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserCartViewSet(ModelViewSet):
    """Эндпоинт для работы с корзиной юзера"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def add_or_create_product_to_cart(self, request, user_id, product_id, quantity):
        """Метод добавления или изменений количества продуктов в корзине"""
        user = User.objects.get(id=int(user_id))
        product = Product.objects.get(id=int(product_id))
        # Проверяем, есть ли такой продукт уже в корзине пользователя
        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        # Если продукт уже есть в корзине, изменяем его количество
        if not created:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            # Если продукта еще нет в корзине, создаем новую запись
            CartItem.objects.create(user=user, product=product, quantity=quantity)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def remove_product_from_cart(self, request, user_id, product_id):
        """Метод удаления продукта из корзины"""
        user = User.objects.get(id=int(user_id))
        product = Product.objects.get(id=int(product_id))
        cart_item = get_object_or_404(CartItem, user=user, product=product)

        # Удаляем объект корзины
        cart_item.delete()
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_cart_contents(self, request, user_id):
        """Метод, который выводит содержимое корзины, цену и количество товаров"""
        user = User.objects.get(id=int(user_id))
        cart_items = user.cartitem_set.all()
        # Подсчитываем общее количество товаров в корзине
        total_quantity = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        # Подсчитываем общую стоимость товаров в корзине
        total_price = cart_items.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price'] or 0

        cart_serializer = CartItemSerializer(cart_items, many=True)
        return Response({
            'user': self.get_serializer(user).data,
            'cart_contents': cart_serializer.data,
            'total_quantity': total_quantity,
            'total_price': total_price
        })

    def clear_cart(self, request, user_id):
        """Метод, который очищает корзину полностью"""
        user = User.objects.get(id=int(user_id))
        user.cartitem_set.all().delete()
        return Response("Cart cleared successfully")


class UserCreateView(CreateAPIView):
    """Метод для создания пользователя"""
    model = User
    serializer_class = UserCreateSerializer
