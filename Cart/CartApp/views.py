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
        id_carta = request.data.get('id_carta') #Obtener el ID de la carta enviado desde Node.js
        data = {
            'user': user_id,
            'id_carta':id_carta,
            'title': request.data.get('title', ''),
            'description': request.data.get('description', '')
        }
        
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)