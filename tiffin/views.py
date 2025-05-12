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



