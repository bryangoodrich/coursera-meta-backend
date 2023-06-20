from django.urls import path
from . import views

urlpatterns = [
    # path('users', views.djoser?)
    path('menu-categories', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart', views.CartView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('groups/manager/users', views.ManageGroupView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManageGroupDeleteView.as_view())
]
