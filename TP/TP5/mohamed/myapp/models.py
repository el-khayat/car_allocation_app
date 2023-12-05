from django.db import models
from django.apps import AppConfig

class Car(models.Model):
    class Meta:
        app_label = 'myapp'
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    is_despo = models.CharField(max_length=20)
    nbr_place = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'   

