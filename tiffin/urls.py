from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    MenuItemListView, 
    OrderCreateView, 
    UserOrderListView,
    AdminOrderUpdateView,
    RegisterUser,
    GoogleLoginView,
    UserNotificationView,
    CustomTokenObtainPairView,
    AdminStatsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('menu/', MenuItemListView.as_view(), name='menu'),
    path('orders/', OrderCreateView.as_view(), name='create_order'),
    path('orders/user/', UserOrderListView.as_view(), name='user_orders'),
    path('orders/<int:pk>/', AdminOrderUpdateView.as_view(), name='update_order'),
    path('notifications/', UserNotificationView.as_view(), name='user_notifications'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

from .views import (
    AdminMenuListCreateView,
    AdminMenuUpdateDeleteView,
    AdminOrderListView
)

urlpatterns += [
    path('admin/menu/', AdminMenuListCreateView.as_view(), name="admin_menu_list"),
    path('admin/menu/<int:pk>/', AdminMenuUpdateDeleteView.as_view(), name="admin_menu_detail"),
    path("admin/stats/", AdminStatsView.as_view()),
    path("admin/orders/", AdminOrderListView.as_view(), name="admin_orders"),
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
