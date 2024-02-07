from django.db import models
from django.contrib.auth.models import AbstractUser


from django.contrib.auth import get_user_model


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)

    def is_administrator(self):
        return self.job_title and self.job_title.lower() == 'administrator'

    def is_employee(self):
        return self.job_title and self.job_title.lower() == 'pracownik'

    def is_client(self):
        return self.job_title and self.job_title.lower() == 'klient'
    

# Model zadania
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    client_name = models.CharField(max_length=100)
    time_spent = models.DecimalField(max_digits=5, decimal_places=2)
    creation_date = models.DateField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.name

# Model załącznika
class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.file.name


    
    
import uuid 
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Oczekujące'),
        ('Completed', 'Zrealizowane'),
        ('Needs Review', 'Niezakceptowany'),
    ]
    
    order_id = models.CharField(max_length=20, unique=True)  # ID zlecenia
    name = models.CharField(max_length=100)  # Nazwa zlecenia
    street = models.CharField(max_length=100)  # Ulica
    city = models.CharField(max_length=50)  # Miasto
    postal_code = models.CharField(max_length=10)  # Kod pocztowy
    client = models.CharField(max_length=100)  # Klient
    wojewodztwo = models.CharField(max_length=20,null=True, blank=True)  # wojewodztwo
    inicjaly= models.CharField(max_length=20,null=True, blank=True)# inicjaly
    execution_date = models.DateField(null=True, blank=True) # Data realizacji zlecenia
    time_spent = models.DecimalField(max_digits=5, decimal_places=2)  # Czas poświęcony na zlecenie
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Użytkownik przypisany do zlecenia
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Status zlecenia

    def __str__(self):
        return f"Order {self.order_id} - {self.name}"

class OrderPhoto(models.Model):
    order = models.ForeignKey(Order, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='order_photos/')

    def __str__(self):
        return f"Photo for Order {self.order.order_id}"
