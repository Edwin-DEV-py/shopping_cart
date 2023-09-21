from django.urls import path
from .views import CartItemAPIView,RemoveSameItem,DeleteCard,VaciarCarrito

urlpatterns = [
    path('cart/', CartItemAPIView.as_view(),name='carrito'),
    path('cartshop/', CartItemAPIView.as_view(),name='carrito_comprar'),
    path('cart/remove/',RemoveSameItem,name='removecard'),
    path('cart/delete/',DeleteCard,name='deletecard'),
    path('cart/vaciar/',VaciarCarrito,name='vaciar'),
]