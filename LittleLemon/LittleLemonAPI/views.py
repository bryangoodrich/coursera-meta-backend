"""
Little Lemon API Views

Custom IsManagerOrAdminUser permissions class used to validate
whether requestor is authenticated and is either Staff (Admin)
or part of the Manager group. 

Global AnonRateThrottle and UserRateThrottle are applied.
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer


class IsManagerOrAdminUser(BasePermission):
    """
    Validtes User is Admin or Manager Group User
    """
    def has_permission(self, request, view):
        """
        Checks the IsAdminUser properties and if Manager Group exists

        The IsAdminUser permissions class checks that the user is 
        authenticated and is Staff enabled. This also validates that 
        the user has the Manager group membership.

        Alternatively, one could just validate group membership
        and do a bitwise check in the `permission_classes` like
        
        `permission_classes = [IsManagerUser | IsAdminUser]`
        """
        user = request.user
        is_manager = user.groups.filter(name='Manager').exists()
        return user.is_authenticated and (user.is_staff or is_manager)


class IsDeliveryCrewUser(BasePermission):
    """
    Checks if the user is authenticated and belongs to Delivery Crew
    """
    def has_permission(self, request, view):
        user = request.user
        is_delivery_crew = user.groups.filter(name='Delivery Crew').exists()
        return user.is_authenticated and is_delivery_crew


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsManagerOrAdminUser()]
        else:
            return []


class MenuItemsListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title', 'category__title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsManagerOrAdminUser()]
        else:
            return []


class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsManagerOrAdminUser()]
        else:
            return []


class CartView(generics.ListCreateAPIView):
    """
    View your Cart
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=request.user).delete()
        return Response("Cart emptied", status.HTTP_204_NO_CONTENT)


class CartDeleteView(generics.DestroyAPIView):
    """
    Destroy the Cart
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)
    
    def get_permissions(self):
        method = self.request.method
        if method in ('DELETE', 'PUT'):
            permission_classes = [IsManagerOrAdminUser]
        elif method == 'PATCH':
            permission_classes = [IsDeliveryCrewUser]
        elif method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        order = serializer.instance
        cart = Cart.objects.filter(user=self.request.user)
        items = [create_order_item(order, item) for item in cart]
        order.total = sum(item.price for item in items)
        order.save()
        cart.delete()
    


class OrderItemsView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        order = self.kwargs['pk']

        if user.groups.filter(name='Manager').exists():
            return OrderItem.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            return OrderItem.objects.filter(order__delivery_crew=user)
        elif Order.objects.filter(user=user, id=order).exists():
            return OrderItem.objects.filter(order__id=order)
        
        raise PermissionDenied("You are not allowed to access this order")

    def patch(self, request, *args, **kwargs):
        """
        Modify Order

        This PATCH request has 2 scenarios, when the manager
        submits a delivery crew member assignment and when
        a delivery crew member updates the order status.
        """
        order = self.get_object()
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            delivery_crew = request.data.get('delivery_crew')
            if delivery_crew is not None:
                try:
                    delivery_crew = User.objects.get(id=delivery_crew, groups__name='Delivery Crew')
                    order.delivery_crew = delivery_crew
                    order.save()
                    serializer = self.get_serializer(order)
                    return Response(serializer.data)
                except User.DoesNotExist:
                    return Response({'detail': 'Invalid delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
        elif user.groups.filter(name='Delivery Crew').exists():
            status_value = request.data.get('status')
            if status_value is not None:
                order.status = status_value
                order.save()
                serializer = self.get_serializer(order)
                return Response(serializer.data)
        
        raise PermissionDenied("You are not allowed to modify this order.")


class ManagerGroupView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    Handles adding and removing users from Manager group
    """
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManagerOrAdminUser]

    def post(self, request, *args, **kwargs):
        """
        Adds user to Manager group by username in POST
        """
        username = self.request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                f"User {username} does not exist",
                status.HTTP_404_NOT_FOUND
            )
        
        if user.groups.filter(name='Manager').exists():
            return Response(
                f"User {user} is already a Manager",
                status.HTTP_200_OK
            )
        
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        print(managers)
        print(type(managers))
        return Response(
            f'User {user} added to Managers',
            status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """
        Removes user from Manager group based on <int:pk> URI
        """
        user = self.get_object()  # Retrieve user based on URL pk
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return Response(
            f'User {user} removed from Managers',
            status.HTTP_204_NO_CONTENT
        )


class DeliveryGroupView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    Handles adding and removing users from Delivery group
    """
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsManagerOrAdminUser]

    def post(self, request, *args, **kwargs):
        """
        Adds user to Delivery group by username in POST
        """
        username = self.request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                f"User {username} does not exist",
                status.HTTP_404_NOT_FOUND
            )

        if user.groups.filter(name='Delivery Crew').exists():
            return Response(
                f"User {user} is already in Delivery Crew",
                status.HTTP_200_OK
            )
        
        managers = Group.objects.get(name='Delivery Crew')
        managers.user_set.add(user)
        print(managers)
        print(type(managers))
        return Response(
            f'User {user} added to Delivery Crew',
            status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """
        Removes user from Delivery group based on <int:pk> URI
        """
        user = self.get_object()  # Retrieve user based on URL pk
        managers = Group.objects.get(name='Delivery Crew')
        managers.user_set.remove(user)
        return Response(
            f'User {user} removed from Delivery Crew',
            status.HTTP_204_NO_CONTENT
        )


def create_order_item(order, item):
    order_item = OrderItem.objects.create(
            order=order,
            menuitem=item.menuitem,
            quantity = item.quantity,
            unit_price = item.unit_price,
            price = item.price)
    order_item.save()
    return order_item