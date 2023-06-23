from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from datetime import date


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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    unit_price = serializers.ReadOnlyField(source='menuitem.price')
    price = serializers.DecimalField(6, 2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
    
    def create(self, validated_data):
        """
        Create a new Cart instance record

        Honestly I spent hours trying to use the OOP components
        to build this automagically and it failed every which way.
        I tried GPT to help and that went down many useless paths.

        In the end, the easiest solution was simply to build the
        object entirely with all the data I have direct access
        to given the information (menuitem and quantity) provided
        in the POST request. SerializerMethodField DOES NOT WORK
        in this case. So I'm not sure what the intended solution
        was for this class. Maybe I'll find out grading!

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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total = serializers.DecimalField(6, 2, read_only=True)
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
    
    def create(self, validated_data):
        """
        Create an Order on POST from user's Cart

        The POST request should have no payload. The
        Order attributes derive from the existing Cart.
        The rest have defaults.
        """

        user = self.context['request'].user
        cart = Cart.objects.filter(user=user)
        total = sum((item.price for item in cart))
        order = Order.objects.create(user=user, total=total, date=date.today())
        return order


class OrderItemSerializer(serializers.ModelSerializer):
     """ Order Item Serializer """
     class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
    
    


class UserSerializer(serializers.ModelSerializer):
    """
    Display users generically
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
