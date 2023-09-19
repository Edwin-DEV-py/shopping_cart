from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import requests

#agregar y ver items del carrito
class CartItemAPIView(APIView):
    def get(self, request):
        user_id = request.data.get('user') 
        
        response = requests.get('https://cards.thenexusbattles2.cloud/api/all/')
        #response = requests.get('http://prime.bucaramanga.upb.edu.co/api/all/')
        cards = response.json()
        
        #filtrar por usuario y serializar datos
        items = CartItem.objects.filter(user=user_id)
        cart_item_serializer = CartItemSerializer(items, many=True)
        cart_item_data = cart_item_serializer.data  #datos serializados

        #guardamos los datos de las cartas
        response_data = []
        for item_data in cart_item_data:
            id_carta = item_data["id_carta"]
            nombre_carta = item_data["nombre_carta"]
            price = item_data['price']
            quantity = item_data["quantity"]
            
            for card in cards:
                if card['_id'] == id_carta:
                    response_data.append({
                        "user": user_id,
                        "id_carta": id_carta,
                        "nombre_carta":nombre_carta,
                        "price":price,
                        "quantity": quantity,
                        **card
                    })
            
        return Response(response_data)
    
    def post(self,request):
        user_id = request.data.get('user')  #Obtener el ID de usuario enviado desde Node.js
        id_carta = request.data.get('id_carta') #Obtener el ID de la carta enviado desde Node.js
        price = request.data.get('price')
        nombre_carta = request.data.get('nombre_carta')
        data = {
            'user': user_id,
            'nombre_carta':nombre_carta,
            'id_carta':id_carta,
            'price':price
        }
        
        
        
        try:
            #agregar mas cantidad a la misma carta si ya existe
            item = CartItem.objects.get(id_carta=id_carta,user=user_id)
            item.quantity +=1
            item.save()
            serializer = CartItemSerializer(item)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            #crear la carta en el carrito sino existe
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
        else:
            card.delete()
        cart_items = CartItem.objects.filter(user=user_id)
        updated_cart_serializer = CartItemSerializer(cart_items, many=True)
        updated_cart_data = updated_cart_serializer.data
        return Response(updated_cart_data, status=status.HTTP_204_NO_CONTENT)
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
    cart_items = CartItem.objects.filter(user=user_id)
    updated_cart_serializer = CartItemSerializer(cart_items, many=True)
    updated_cart_data = updated_cart_serializer.data
    return Response(updated_cart_data, status=status.HTTP_204_NO_CONTENT)

    
