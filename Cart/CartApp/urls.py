from django.urls import path
from .views import CartItemAPIView

urlpatterns = [
    path('cart/', CartItemAPIView.as_view(),name='carrito'),
]