from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer

class CartItemAPIView(APIView):
    def get(self, request, user_id):
        items = CartItem.objects.filter(user=user_id)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)