from django.urls import path
from . import views

urlpatterns = [
    path('menu-categories', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsListView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemView.as_view(),  name='menu-items-detail'),
    path('cart/menu-items', views.CartView.as_view()),
    path('cart/menu-items/<int:pk>', views.CartView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('orders/<int:pk>', views.OrderItemsView.as_view()),
    path('groups/manager/users', views.ManagerGroupView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerGroupView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryGroupView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryGroupView.as_view()),
]
