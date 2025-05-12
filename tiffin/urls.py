from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    MenuItemListView, 
    OrderCreateView, 
    UserOrderListView,
    AdminOrderUpdateView,
    RegisterUser
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('menu/', MenuItemListView.as_view(), name='menu'),
    path('orders/', OrderCreateView.as_view(), name='create_order'),
    path('orders/user/', UserOrderListView.as_view(), name='user_orders'),
    path('orders/<int:pk>/', AdminOrderUpdateView.as_view(), name='update_order'),
]
