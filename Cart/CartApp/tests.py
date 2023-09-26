from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CartItem
from .serializers import CartItemSerializer

#Prueba #1: ver carrito
class CartView(TestCase):
    
    #este metodo setUp se ejecuta antes de las pruebas para configurar el entorno
    def setUp(self):
        self.client = APIClient() #usamos el cliente de pruebas que trae DRF
    
    #prueba de ver el carrito
    def test_view_cart(self):
        #para la prueba usamos la url de login
        url = reverse('carrito')
        
        #datos de prueba
        user = {'user':'monoconchudo'}
        data = {
            'id_carta':'650c817f277ca6e30412135a',
            'user':'monoconcudo',
            'price':10,
            'nombre_carta':'Carta de prueba'
        }
        
        #agregar las cartas
        CartItem.objects.create(**data)
        
        #Enviar el get
        response = self.client.get(url, user, format='json')
        
        #verificar que la respuesta sea correcta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Prueba para obtener el carrito')
        print('Prueba exitosa')
        print('---------------------------------------------------')
        
    def test_add_cart(self):
        #para la prueba usamos la url de login
        url = reverse('carrito')
        
        #datos de prueba
        data = {
            'user':'monoconchudo',
            'id_carta':'650c817f277ca6e30412135a',
            'price':10,
            'nombre_carta':'Carta de prueba'
        }
        
        #Enviar el post
        response = self.client.post(url, data, format='json')
        
        #verificar que la respuesta sea correcta
        print('Prueba par agregar al carrito')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('---------------------------------------------------')
        
    def test_NoView_cart(self):
        #para la prueba usamos la url de login
        url = reverse('carrito')
        
        #datos de prueba
        data = {
            
        }
        
        #Enviar el get
        response = self.client.post(url, data, format='json')
        
        #verificar que la respuesta sea correcta
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('Prueba para verificar que no agrego al carrito')
        print(response)
        print('---------------------------------------------------')
        
    def test_remove_same_item(self):
        #Crear un usuario y una carta de carrito de prueba
        user_id = 'usuario_prueba'
        id_carta = 'carta_prueba'
        carta_prueba = CartItem.objects.create(user=user_id, id_carta=id_carta, quantity=3,price=10)

        #url
        url = reverse('removecard')

        #Datos de prueba
        data = {'user': user_id, 'id_carta': id_carta}

        #Enviar POST
        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea un 204
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar que la cantidad de la carta se haya reducido en 1
        carta_prueba.refresh_from_db()
        self.assertEqual(carta_prueba.quantity, 2)
        print('Prueba para remover items del carrito')
        print(response.data)
        print('---------------------------------------------------')
        
    def test_delete_card(self):
        #Crear un usuario y una carta de carrito de prueba
        user_id = 'usuario_prueba'
        id_carta = 'carta_prueba'
        CartItem.objects.create(user=user_id, id_carta=id_carta, quantity=1,price=10)

        #url
        url = reverse('deletecard')

        #Datos de prueba
        data = {'user': user_id, 'id_carta': id_carta}

        #Enviar POST
        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar que la carta se haya eliminado del carrito
        self.assertFalse(CartItem.objects.filter(user=user_id, id_carta=id_carta).exists())
        print('Prueba para borrar item del carrito')
        print(response.data)
        print('---------------------------------------------------')
        
    def test_vaciar_carrito(self):
        #Crear un usuario y cartas de carrito de prueba
        user_id = 'usuario_prueba'
        id_carta1 = 'carta_prueba1'
        id_carta2 = 'carta_prueba2'
        CartItem.objects.create(user=user_id, id_carta=id_carta1, quantity=1,price=10)
        CartItem.objects.create(user=user_id, id_carta=id_carta2, quantity=2,price=20)

        #url
        url = reverse('vaciar')

        #Datos de prueba
        data = {'user': user_id}

        #Enviar POST
        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que todos los elementos del carrito se hayan eliminado
        self.assertFalse(CartItem.objects.filter(user=user_id).exists())
        print('Prueba para vaciar el carrito')
        print(response.data)
        print('---------------------------------------------------')
