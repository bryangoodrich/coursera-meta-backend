from django.urls import path
from .views import MenuItemsView, CartView, OrdersView

urlpatterns = [
    # path('users', views.djoser?)
    path('menu-items', MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemsView.as_view()),
    path('cart', CartView.as_view()),
    path('orders', OrdersView.as_view()),
]
