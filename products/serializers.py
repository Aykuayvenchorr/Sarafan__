from rest_framework import serializers

from products.models import Category, Subcategory, Product, User, CartItem


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'slug', 'image', 'subcategories']

    def get_subcategories(self, obj):
        return [subcategory.name for subcategory in obj.subcategory_set.all()]


class ProductSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'image_1', 'image_2', 'image_3', 'category_name', 'subcategory_name']

    def get_subcategory_name(self, obj):
        return obj.subcategory.name

    def get_category_name(self, obj):
        return obj.subcategory.category.name


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('product_name', 'quantity')

    def get_product_name(self, obj):
        return obj.product.name


class UserSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'cart')

    def get_cart(self, obj):
        cart_items = obj.cartitem_set.all()
        cart = []
        for cart_item in cart_items:
            product_serializer = ProductSerializer(cart_item.product)
            cart.append({'product': product_serializer.data, 'quantity': cart_item.quantity})
        return cart


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
