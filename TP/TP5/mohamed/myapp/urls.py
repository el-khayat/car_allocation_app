from django.urls import path
from .views import car_list, add_car, car_edit, car_delete

urlpatterns = [
    path('', car_list, name='car_list'),
    path('add_car/', add_car, name='add_car'),
    path('<int:pk>/edit/', car_edit, name='car_edit'),
    path('<int:pk>/delete/', car_delete, name='car_delete'),
]
