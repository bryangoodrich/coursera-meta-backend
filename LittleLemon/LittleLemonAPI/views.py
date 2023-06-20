from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import generics, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title', 'category__title']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = MenuItemSerializer
    
    def get_queryset(self, request, pk):
        return get_object_or_404(MenuItem, pk=pk)


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemsView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ManageGroupView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name__in=['Manager'])
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        """
        Assign a user to the manager group or lists all managers
        """
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return Response(UserSerializer(user).data, status.HTTP_201_CREATED)

        return Response(status.HTTP_404_NOT_FOUND)


class ManageGroupDeleteView(generics.RetrieveDestroyAPIView):
    """
    Remove a manager for a given pk in URL path
    """
    queryset = Group.objects.get(name='Manager')
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        response = Response(
            {
                "message": f"user {user.username} removed from Manager group"
            }, 
            status.HTTP_200_OK)
        return response

