from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=11)
    
    def __str__(self):
        return self.firstname

class OrderPost(models.Model):
    ordered = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models. DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Post{self.post_id} in Order {self.ordered.id}"