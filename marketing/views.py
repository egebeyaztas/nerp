import re
from django.shortcuts import render, redirect
from .forms import MarketingForm, PotentialClientForm, AdForm
from .models import Marketing, PotentialClient, Ad
from django.http import HttpResponse

class Route_data:
    def __init__(self):
        self.DASHBOARD = 'marketing-dashboard'

route = Route_data()

def marketing_dashboard(request):
    marketing = Marketing.objects.first()
    form = MarketingForm(instance=marketing)
    return render(request, 'marketing/dashboard.html', {'marketing': marketing, 'form': form})

def update_marketing_data_form(request, id):
    marketing = Marketing.objects.get(id=id)
    form = MarketingForm(instance=marketing)

    context = {
        'form': form,
        'marketing': marketing,
        'editview': True
    }

    return render(request, 'marketing/partials/marketing-form.html', context)

def update_marketing_data(request, id):
    if request.method == 'POST':
        marketing = Marketing.objects.get(id=id)
        form = MarketingForm(request.POST, instance=marketing)
        if form.is_valid():
            form.save()
            return redirect(route.DASHBOARD)
        else:
            form = MarketingForm()
            context = {'form': form}
            return render(request, 'marketing/partials/marketing-form.html',context)

def create_potential_client(request):
    form = PotentialClientForm()
    if request.method == 'POST':
        form = PotentialClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'potentialClientChanged'})
    else:
        return render(request, 'marketing/partials/potential-client-form.html', {'form': form})

def update_potential_client(request, pclient_id):
    potential_client = PotentialClient.objects.get(id=pclient_id)
    form = PotentialClientForm(instance=potential_client)
    if request.method == 'POST':
        form = PotentialClientForm(request.POST, instance=potential_client)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'potentialClientChanged'})
    else:
        return render(request, 'marketing/partials/potential-client-form.html', {'form': form, 'potential_client':potential_client, 'editview':True})

def get_potential_client_list(request):
    p_clients = PotentialClient.objects.all()
    return render(request, 'marketing/partials/potential-client-list.html', {'potential_clients':p_clients})

def create_ads(request):
    form = AdForm()
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'adChanged'})
    else:
        return render(request, 'marketing/partials/ad-form.html', {'form': form})
def update_ads(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    form = AdForm(instance=ad)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'adChanged'})
    else:
        return render(request, 'marketing/partials/ad-form.html', {'form': form, 'ad':ad, 'editview':True})
def get_ads_list(request):
    ads = Ad.objects.all()
    return render(request, 'marketing/partials/ad-list.html', {'ads':ads})