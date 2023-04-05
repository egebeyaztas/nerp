from django.shortcuts import render
from django.http import HttpResponse
from .forms import PurchaseOfferForm, PurchaseLineFormSet
from .models import PurchaseOffer, PurchaseOfferLine
from scripts.keygen import KeyGenerator
from general.models import Stock, StockGroup, Supplier
from django.template import RequestContext
from django.forms import inlineformset_factory

keygenerator = KeyGenerator()

def purchasing_dashboard(request):
    in_purchase_list_count = Stock.objects.filter(in_purchase_list=True).count()
    offer_count = PurchaseOffer.objects.filter(approve_status='Bekliyor').count()
    offer_order_count = PurchaseOffer.objects.filter(approve_status='Onaylandı').count()
    context = {
        'in_purchase_list_count': in_purchase_list_count,
        'offer_count': offer_count,
        'offer_order_count': offer_order_count,
    }
    return render(request, 'purchasing/dashboard.html', context)

def create_purchase_offer(request):
    form = PurchaseOfferForm()
    if request.method == 'POST':
        stocks = request.POST.getlist('stocks')
        form = PurchaseOfferForm(request.POST)
        formset = PurchaseLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            offer_instance = form.save(commit=False)
            offer_instance.offer_id = keygenerator.generate_unique_key('SA-' + offer_instance.supplier.name[:2].upper() + '-')
            for stock in stocks:
                offer_instance.add(stock)
            offer_instance.save()
            for form in formset:
                line_obj = form.save(commit=False)
                line_obj.offer = offer_instance
                line_obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'purchaseOffer'})
    else:
        return render(request, 'purchasing/partials/purchase-offer-form.html', {'form': form})

def get_purchase_formset(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        supplier = Supplier.objects.get(id=supplier_id)
        qs = Stock.objects.filter(suppliers=supplier)
        
        def get_field_qs(field, **kwargs):
            formfield = field.formfield(**kwargs)
            if field.name == 'stock':
                formfield.queryset = formfield.queryset.filter(suppliers=supplier)
            return formfield
        
        OfferFormset = inlineformset_factory(
            parent_model=PurchaseOffer,
            model=PurchaseOfferLine,
            form=PurchaseOfferForm,
            extra=1,
            can_delete=False,
            formfield_callback=get_field_qs,
        )
        return render(request, 'purchasing/partials/purchase-formset.html', {'formset': OfferFormset})


def update_purchase_offer(request, offer_id):
    offer = PurchaseOffer.objects.get(id=offer_id)
    form = PurchaseOfferForm(instance=offer)
    qs = offer.lines.all()
    formset = PurchaseLineFormSet(queryset=qs, instance=offer)
    if request.method == 'POST':
        print(request.POST)
        form = PurchaseOfferForm(request.POST, instance=offer)
        formset = PurchaseLineFormSet(request.POST, queryset=qs, instance=offer)
        print(form.is_valid())
        print(formset.is_valid())
        if form.is_valid() and formset.is_valid():
            offer_instance = form.save(commit=False)
            for form in formset:
                if form.cleaned_data != {}:
                    line_obj = form.save(commit=False)
                    if line_obj.offer is None:
                        line_obj.offer = offer_instance
                    line_obj.save()
            offer_instance.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'purchaseOffer'})
        else:
            return HttpResponse('error')
    else:
        return render(request, 'purchasing/partials/purchase-offer-form.html', {'form': form, 'offer':offer, 'editview': True, 'formset': formset})

def delete_purchase_offer(request, offer_id):
    pass

def get_purchase_list(request):
    purchase_list_stocks = Stock.objects.filter(in_purchase_list=True).order_by('-quantity')
    return render(request, 'purchasing/partials/purchase-list.html', {'purchase_list_stocks': purchase_list_stocks})

def get_purchase_offers(request):
    if request.method == 'POST':
        if request.POST.get('data_attr') == 'purchase-offer-list':
            purchase_offers = PurchaseOffer.objects.filter(approve_status='Bekliyor')
            return render(request, 'purchasing/partials/purchase-offer-list.html', {'purchase_offers': purchase_offers})
        elif request.POST.get('data_attr') == 'purchase-order-list':
            purchase_offers = PurchaseOffer.objects.filter(approve_status='Onaylandı')
            return render(request, 'purchasing/partials/purchase-offer-list.html', {'purchase_offers': purchase_offers})
        