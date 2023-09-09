from django.urls import path
from .views import CartItemAPIView,RemoveSameItem,DeleteCard

urlpatterns = [
    path('cart/<str:user_id>/', CartItemAPIView.as_view(),name='carrito'),
    path('cart/remove/',RemoveSameItem,name='removecard'),
    path('cart/delete/',DeleteCard,name='deletecard'),
]