from django.shortcuts import render, redirect
from .models import Car
from .forms import CarForm

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})

def car_edit(request,pk):
    print(f" pk : {pk}")
    car = Car.objects.get(pk=pk)
    print(f" car : {car.model}")
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'add_car.html', {'form': form, 'car': car})

def car_delete(request, pk):
    Car.objects.get(pk=pk).delete()
    return redirect('car_list')

