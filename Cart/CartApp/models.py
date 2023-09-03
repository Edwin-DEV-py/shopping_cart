from django.db import models

class CartItem(models.Model):
    user = models.IntegerField()
    card = models.IntegerField()
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return '%s' % self.id
    
    def sub_total(self):
        return self.price * self.quantity
