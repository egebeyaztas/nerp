from django.shortcuts import render,redirect
from .forms import QualityForm, ApproveForm
from .models import Quality
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from general.models import Product

def qc_dashboard(request):
    return render(request, 'qc/dashboard.html')

def create_quality_control_order(request):
    form = QualityForm()
    if request.method == 'POST':
        form = QualityForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'qcOrderChanged'})
    else:
        return render(request, 'qc/partials/create-qc-order-form.html', {'form': form} ) 

def update_quality_control_order(request, qid):
    qc_order = Quality.objectcs.get(id=qid)
    form = QualityForm(instance=qc_order)
    if request.method == 'POST':
        form = QualityForm(request.POST, instance=qc_order)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'qcOrderChanged'})
    else:
        return render(request, 'qc/partials/create-qc-order-form.html', {'form': form,  'qc_order': qc_order, 'editview': True} ) 

#def create_qc_order_from_product(self, product_id):
    

def approve_product(request, qid, product_id):
    form = ApproveForm()
    if request.method == 'POST':
        form = ApproveForm(request.POST)
        qc = Quality.objects.get(id=qid)
        print(request.POST)
        if request.POST.get('approve-checkbox') == 'approved':
            product = qc.job_order.products.get(id=product_id)
            product.approved = True
            product.save()
            return redirect('qc-order-detail', qid)
        else:
            product = qc.job_order.products.get(id=product_id)
            product.approved = False
            product.save()
            return redirect('qc-order-detail', qid)
    else:
        return redirect('manufacturing-dashboard')

def get_qc_lists(request):
    if request.htmx:
        qc_orders = Quality.objects.filter(active=True)
        return render(request, 'qc/partials/qc-order-list.html', {'qc_orders': qc_orders})
    if request.method == 'POST':
        if request.POST.get('data_attr') == 'active-qc-list':
            qc_orders = Quality.objects.filter(active=True)
            return render(request, 'qc/partials/qc-order-list.html', {'qc_orders': qc_orders})
        elif request.POST.get('data_attr') == 'passive-qc-list':
            qc_orders = Quality.objects.filter(active=False)
            return render(request, 'qc/partials/qc-order-list.html', {'qc_orders': qc_orders})
        elif request.POST.get('data_attr') == 'qc-product-list':
            products = Product.objects.filter(approved=None)
            return render(request, 'qc/partials/qc-product-list.html', {'products': products})