from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User


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
        fields = ['id', 'title', 'featured', 'price', 'category', 'category_id']


class CartSerializer(serializers.ModelSerializer):
    """ Cart Serializer """

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'unit_price': {'read_only': True},
            'price': {'read_only': True},
            'user': {'read_only': True}
        }
    
    def create(self, validated_data):
        """
        Create a new Cart instance record

        Honestly I spent hours trying to use the OOP components
        to build this automagically and it failed every which way.
        I tried GPT to help and that went down many useless paths.

        In the end, the easiest solution was simply to build the
        object entirely with all the data I have direct access
        to given the information (menuitem and quantity) provided
        in the POST request. 

        I'm sure there is an easier way, and I hope to learn it 
        someday! 
        """
        menuitem = validated_data.get('menuitem')
        unit_price = menuitem.price
        quantity = validated_data.get('quantity')
        cart = Cart.objects.create(
            user = self.context['request'].user,
            menuitem = menuitem,
            quantity = quantity,
            unit_price = unit_price,
            price = unit_price * quantity
        )
        return cart
    
    


class OrderSerializer(serializers.ModelSerializer):
    """ Order Serializer """
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
     """ Order Item Serializer """
     class Meta:
        model = OrderItem
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Display users generically
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
