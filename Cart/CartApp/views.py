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
    
    def post(self,request):
        user_id = request.data.get('user')  #Obtener el ID de usuario enviado desde Node.js
        cart_id = request.data.get('cart_id') #Obtener el ID de la carta enviado desde Node.js
        data = {
            'user': user_id,
            'title': request.data.get('title', ''),
            'description': request.data.get('description', '')
        }