from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    """ Category Serializer """
    class Meta:
        model = Category
        fields = ['id','title']


class MenuItemSerializer(serializers.ModelSerializer):
    """ Menu Item Serializer """
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory', 'category', 'category_id']


class CartSerializer(serializers.ModelSerializer):
    """ Cart Serializer """
    class Meta:
        model = Cart
        fields = '__ALL__'


class OrderSerializer(serializers.ModelSerializer):
    """ Order Serializer """
    class Meta:
        model = Order
        fields = '__ALL__'


class OrderItemSerializer(serializers.ModelSerializer):
     """ Order Item Serializer """
     class Meta:
        model = OrderItem
        fields = '__ALL__'
