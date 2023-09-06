from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

#agregar y ver items del carrito
class CartItemAPIView(APIView):
    def get(self, request):
        user_id = request.data.get('user') 
        items = CartItem.objects.filter(user=user_id)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        user_id = request.data.get('user')  #Obtener el ID de usuario enviado desde Node.js
        id_carta = request.data.get('id_carta') #Obtener el ID de la carta enviado desde Node.js
        price = request.data.get('price')
        data = {
            'user': user_id,
            'id_carta':id_carta,
            'price':price
        }
        
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#anadir mas cantidad de la misma carta
@api_view(['POST'])
def AddMoreCard(request):
    #obtener datos desde el front
    user_id = request.data.get('user')
    id_carta = request.data.get('id_carta')
    
    #verificar el item en el carrito
    card = get_object_or_404(CartItem,id_carta=id_carta)
    
    #validar que el item si sea del usuario y exista en la abse de datos
    if card.user == user_id and card.id_carta == id_carta:
        card.quantity += 1
        card.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#remover cantidad de la misma carta
@api_view(['POST'])
def RemoveSameItem(request):
    #obtener datos desde el front
    user_id = request.data.get('user')
    id_carta = request.data.get('id_carta')
    
    #verificar el item en el carrito
    card = get_object_or_404(CartItem,id_carta=id_carta)
    
    #validar que el item si sea del usuario
    if card.user == user_id:
        if card.quantity > 1:
            card.quantity -= 1
            card.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "No tienes permiso para eliminar este elemento del carrito."}, status=status.HTTP_403_FORBIDDEN)
    

#eliminar carta del carrito
@api_view(['POST'])
def DeleteCard(request):
    #obtener datos desde el front
    user_id = request.data.get('user')
    id_carta = request.data.get('id_carta')
    
    #verificar el item en el carrito
    card = get_object_or_404(CartItem,id_carta=id_carta)
    
    #validar que el item si sea del usuario
    if card.user == user_id:
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "No tienes permiso para eliminar este elemento del carrito."}, status=status.HTTP_403_FORBIDDEN)
    
