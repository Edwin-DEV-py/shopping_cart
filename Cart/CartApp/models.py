from django.db import models

class CartItem(models.Model):
    user = models.CharField(max_length=100)
    id_carta = models.CharField(max_length=24)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return '%s' % self.id
    
    def sub_total(self):
        return self.price * self.quantity
