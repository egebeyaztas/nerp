from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ProductForm, OrderForm,OrderLineFormSet, StockForm, SupplierForm
from .models import Product, Client, Order, ProductGroup, Stock, Supplier
from scripts.keygen import KeyGenerator
from manufacturing.models import JobOrder
import json
from datetime import datetime, date
from django.core import serializers

keygenerator = KeyGenerator()

def create_product_form(request, joborder_id):
    form = ProductForm()
    order = JobOrder.objects.get(id=joborder_id)
    context = {
        'form': form,
        'order': order
    }

    return render(request, 'general/partials/create-product-form.html', context)

def create_product(request, joborder_id):
    order = JobOrder.objects.get(id=joborder_id)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            for i in range(order.product_quantity):
                product = Product(
                    name = form.cleaned_data['name'],
                    product_id = keygenerator.generate_unique_key(form.cleaned_data['client'].name[:2]+'-'+form.cleaned_data['name'][:2]+'-'),
                    description = form.cleaned_data['description'],
                    client = form.cleaned_data['client'],
                    price = form.cleaned_data['price'],
                    job_order = order,
                )
                product.save()
            return redirect('manufacturing-dashboard')
        else:
            return redirect('logistics-dashboard')

def product_list_from_order(request, order_id):
    if request.method == 'POST':
        print('Product list from order')
        order = Order.objects.get(id=order_id)
        products = order.products.all()
        return render(request, 'general/partials/product-list-from-order.html', {'products':products})

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type is not serializable")

def get_orders_from_client(request, client_id):
    if request.POST:
        orders = Order.objects.filter(client__id=client_id)
        response = serializers.serialize("json", orders)
        return HttpResponse(response, content_type='application/json')

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'general/partials/order-list.html', {'orders': orders})

def create_order(request):
    form = OrderForm()
    formset = OrderLineFormSet()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderLineFormSet(request.POST)
        print(formset)
        if form.is_valid() and formset.is_valid():
            obj_instance = form.save(commit=False)
            obj_instance.name = f'{obj_instance.client.name}-{obj_instance.created_at} Siparişi'
            obj_instance.order_id = keygenerator.generate_unique_key(f'{obj_instance.client.name[:2]}-{obj_instance.client.location[:2]}-SP-')
            obj_instance.save()
            for form in formset:
                inline_obj = form.save(commit=False)
                inline_obj.order = obj_instance
                inline_obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'orderChanged'})
    else:
        context = {'form': form, 'formset': formset}
        return render(request, 'general/partials/order-form.html', context)

def update_order(request, orderid):
    order = Order.objects.get(id=orderid)
    product_group = ProductGroup.objects.first()
    form = OrderForm(instance=order)
    qs = order.orderlines.all()
    formset = OrderLineFormSet(queryset=qs, instance=order)
    if request.method == 'POST':
        order = Order.objects.get(id=orderid)
        form = OrderForm(request.POST, instance=order)
        qs = order.orderlines.all()
        formset = OrderLineFormSet(request.POST, queryset=qs, instance=order)
        print(formset.errors)
        print(formset.non_form_errors())
        print(formset.cleaned_data)
        print(formset.is_valid())
        if form.is_valid() and formset.is_valid():
            obj_instance = form.save(commit=False)
            print('continue')
            obj_instance.save()
            print('progress')
            for form in formset:
                print('we')
                if form.cleaned_data != {}:
                    inline_obj = form.save(commit=False)
                    if inline_obj.order is None:
                        inline_obj.order = obj_instance
                    inline_obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'orderChanged'})
    else:    
        context = {'form': form, 'formset': formset, 'order':order, 'editview': True}
        return render(request, 'general/partials/order-form.html', context)

def get_stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'general/partials/stock-list.html', {'stocks':stocks})

def create_stock(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'stockChanged'})
    else:
        return render(request, 'general/partials/stock-form.html', {'form': form})

def update_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    form = StockForm(instance=stock)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock_ins = form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'stockChanged'})
    else:
        return render(request, 'general/partials/stock-form.html', {'form': form, 'stock': stock, 'editview': True})

def get_supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'general/partials/supplier-list.html', {'suppliers':suppliers})

def create_supplier(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'supplierChanged'})
    else:
        return render(request, 'general/partials/supplier-form.html', {'form': form})

def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    form = SupplierForm(instance=supplier)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'supplierChanged'})
    else:
        return render(request, 'general/partials/supplier-form.html', {'supplier': supplier, 'form': form, 'editview': True})