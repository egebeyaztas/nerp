from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PossibleEmployee
from .forms import PossibleEmployeeForm

class Route_data:
    def __init__(self):
        self.DASHBOARD = 'hr-dashboard'

route = Route_data()

def hr_dashboard(request):

    posemp = PossibleEmployee.objects.all()

    context = {
        'posemp': posemp,
    }

    return render(request, 'hr/dashboard.html', context)

def posemp_list(request):
    posemp = PossibleEmployee.objects.all()
    context = {
        'posemp': posemp,
    }
    return render(request, 'hr/partials/pos-emp-list.html', context)


def create_possible_employee_form(request):
    form = PossibleEmployeeForm()
    context = {'form': form, 'editview': False}

    return render(request, 'hr/partials/update-hr-form.html', context)

def update_possible_employee_form(request, id):
    temp = PossibleEmployee.objects.get(id=id)
    form = PossibleEmployeeForm(instance=temp)

    context = {
        'form': form,
        'temp': temp,
        'editview': True
    }

    return render(request, 'hr/partials/update-hr-form.html', context)

def create_possible_employee(request):
    if request.method == 'POST':
        form = PossibleEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'onEmpChange'})
        else:
            form = PossibleEmployeeForm()
            context = {'form': form}
            return render(request, 'hr/partials/update-hr-form.html', context)

def update_possible_employee(request, id):
    if request.method == 'POST':
        temp = PossibleEmployee.objects.get(id=id)
        form = PossibleEmployeeForm(request.POST, request.FILES, instance=temp)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'onEmpChange'})
        else:
            form = PossibleEmployeeForm()
            context = {'form': form}
            return render(request, 'hr/partials/update-hr-form.html', context)

def delete_possible_employee(request, id):
    temp = PossibleEmployee.objects.get(id=id)
    temp.delete()
    posemp = PossibleEmployee.objects.all()
    return render(request, 'hr/partials/pos-emp-list.html', {'posemp': posemp})