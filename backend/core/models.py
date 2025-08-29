from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class MembershipLevel(models.Model):
    class Level(models.IntegerChoices):
        FREE = 0, '免費會員'
        SILVER = 1, '銀級會員'
        GOLD = 2, '金級會員'
        PLATINUM = 3, '白金會員'
    id = models.IntegerField(primary_key=True, choices=Level.choices)
    description = models.TextField()

    def __str__(self):
        return self.get_id_display()

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    membership_level = models.ForeignKey(MembershipLevel, on_delete=models.PROTECT)

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    introduction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class Service(models.Model):
    description = models.TextField()

class Order(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=1)
    status = models.CharField(max_length=50)
    issued_time = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)