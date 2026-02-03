from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import MenuItem, Order, OrderItem, UserProfile
from .serializers import (
    MenuItemSerializer, 
    OrderSerializer, 
    OrderCreateSerializer,
    RegisterSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class AdminOrderUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({"error": "User already exists"}, status=400)
            user = User.objects.create_user(username=username, password=password)
            return Response({"message": "User created successfully"}, status=201)
        return Response({"error": "Invalid data"}, status=400)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    data = request.data

    payment_method = data.get('payment_method', 'cash')

    order = Order.objects.create(user=user, payment_method=payment_method)

    for item in data['items']:
        OrderItem.objects.create(
            order=order,
            menu_item_id=item['id'],
            quantity=item.get('quantity', 1),
        )

    return Response({'message': 'Order placed successfully'})

from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Tiffin API is running"})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

User = get_user_model()

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'No token provided'}, status=400)

        try:
            # ✅ Verify token with Google & client ID
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get('email')
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')

            # ✅ Get or create user
            user, created = User.objects.get_or_create(
                username=email,
                defaults={'email': email, 'first_name': name}
            )

            # ✅ Generate JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'profile_picture': picture,
                }
            })

        except ValueError as e:
            return Response({'error': 'Invalid Google token', 'details': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Google login failed', 'details': str(e)}, status=500)


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserNotificationView(APIView):
    authentication_classes = [JWTAuthentication]  # Add this line
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import MenuItem
from .serializers import MenuItemSerializer

# ADMIN: List + Create menu items
class AdminMenuListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('-id')
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]

# ADMIN: Update + Delete menu item
class AdminMenuUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]


from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Order, OrderItem

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status="PENDING").count()
        today_orders = Order.objects.filter(created_at__date=now().date()).count()

        revenue = 0
        for item in OrderItem.objects.select_related("menu_item"):
            revenue += item.menu_item.price * item.quantity

        return Response({
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "today_orders": today_orders,
            "total_revenue": revenue
        })

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from .models import Order
from .serializers import OrderSerializer

class AdminOrderListView(ListAPIView):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
