from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Logistic
from .forms import LogisticForm
from general.forms import ProductForm
from general.models import Order

class Route_data:
    def __init__(self):
        self.DASHBOARD = 'logistics-dashboard'

route = Route_data()

def logistics_list(request, code):
    mokoko = ''
    if code == 'x':
        mokoko = 'Yolda'
        logistics = Logistic.objects.filter(status=mokoko)
    elif code == 'y':
        mokoko = 'Teslim edildi'
        logistics = Logistic.objects.filter(status=mokoko)
    elif code == 'z':
        mokoko = 'Termin Bekliyor'
        logistics = Logistic.objects.filter(status=mokoko)
    return render(request, 'logistics/partials/logistics-list.html', {'logistics':logistics})

def logistics_list_expanded(request):
    logistics = Logistic.objects.all()
    return render(request, 'logistics/partials/logistics-list-expanded.html', {'logistics':logistics})

def logistics_dashboard(request):
    product_form = ProductForm()
    context = {
        'product_form': product_form,
        'x': 'x',
        'y': 'y',
        'z': 'z',
    }
    return render(request, 'logistics/dashboard.html', context)

def create_logistics_form(request):
    form = LogisticForm()
    orders = Order.objects.all()
    context = {'form': form, 'editview': False, 'orders': orders}

    return render(request, 'logistics/partials/logistics-form.html', context)

def update_logistics_form(request, logistic_id):
    logistic = Logistic.objects.get(id=logistic_id)
    form = LogisticForm(instance=logistic)
    print('send')
    context = {
        'form': form,
        'logistic': logistic,
        'editview': True
    }

    return render(request, 'logistics/partials/logistics-form.html', context)

def create_logistics(request):
    print('this is active')
    if request.method == 'POST':
        form = LogisticForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'logisticsChanged'})
        else:
            form = LogisticForm()
            context = {'form': form}
            return render(request, 'logistics/partials/logistics-form.html', context)

def update_logistics(request, logistic_id):
    if request.method == 'POST':
        temp = Logistic.objects.get(id=logistic_id)
        form = LogisticForm(request.POST, request.FILES, instance=temp)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'logisticsChanged'})
        else:
            form = LogisticForm()
            context = {'form': form, 'editview': True}
            return render(request, 'logistics/partials/logistics-form.html', context)

def delete_logistics(request, id):
    temp = Logistic.objects.get(id=id)
    temp.delete()
    logistics = Logistic.objects.all()
    return render(request, 'logistics/partials/logistics-list.html', {'logistics':logistics})
