from multiprocessing import context
from django.shortcuts import render, redirect
from .models import JobOrder, JobOrderFile, TaskFlow, Task
from .forms import JobOrderModelForm, FileModelForm, TaskForm
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django import template
from qualitycontrol.models import Quality
from scripts.keygen import KeyGenerator
from django.contrib.auth.models import User

keygenerator = KeyGenerator()

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def manufacturing_dashboard(request):

    
    qc_orders = Quality.objects.all()

    context = {
        'qc_orders': qc_orders
    }
    return render(request, 'manufacturing/dashboard.html', context)

def job_order_list(request):
    orders = JobOrder.objects.all()
    
    return render(request, 'manufacturing/partials/job-order-list.html',{'orders':orders})

def create_job_order_form(request):

    form = JobOrderModelForm()
    file_form = FileModelForm()
    workers = User.objects.filter(groups__name='worker')
    context = {'form': form, 'file_form': file_form, 'workers': workers}
    return render(request, 'manufacturing/partials/create-job-order-form.html', context)

def edit_job_order_form(request, job_id):
    order = JobOrder.objects.get(id=job_id)
    form = JobOrderModelForm(instance=order)
    file_form = FileModelForm()
    workers = User.objects.filter(groups__name='worker')
    context = {'form': form, 'order': order, 'file_form': file_form, 'workers': workers, 'editview': True}
    return render(request, 'manufacturing/partials/create-job-order-form.html', context)

def create_job_order(request):
    user = request.user
    if request.method == 'POST':
        form = JobOrderModelForm(request.POST)
        file_form = FileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        print(form.is_valid())
        workers = request.POST.getlist('workers')
        if form.is_valid() and file_form.is_valid():
            job_order_instance = form.save(commit=False)
            job_order_instance.job_order_id = keygenerator.generate_unique_key('IE-'+job_order_instance.client.name[:2].upper()+'-')
            #If there is no executive selected, request.user has to be the executive
            if not job_order_instance.executive:
                job_order_instance.executive = user
            job_order_instance.save()
            #Create Task Flow
            task_flow = TaskFlow(job_order=job_order_instance)
            task_flow.save()
            #Attaching files to the job order
            for f in files:
                file_instance = JobOrderFile(file=f, order=job_order_instance)
                file_instance.save()
            return HttpResponse(status=204,headers={'HX-Trigger':'joborderChanged'})
        else:
            return redirect('manufacturing-dashboard')
    else:
        form = JobOrderModelForm()
        file_form = FileModelForm()

        return render(request, 'manufacturing/partials/create-job-order-form.html', {'form':form, 'file_form': file_form})

def job_order_detail_view(request, job_id):
    order = JobOrder.objects.get(id=job_id)
    file_form = upload_document(request, job_id)
    taskflow = TaskFlow.objects.get(job_order__id=job_id)
    return render(request, 'manufacturing/order-detail.html', {'order':order, 'file_form':file_form, 'taskflow': taskflow})

def edit_job_order_detail(request, job_id):
    order = JobOrder.objects.get(id=job_id)
    user = request.user
    if order.executive.username == user.username or user.groups.first().name == 'admin':
        if request.method == 'POST':
            workers = request.POST.getlist('workers')
            form = JobOrderModelForm(request.POST, instance=order)
            print(form.is_valid())
            if form.is_valid():
                job_order_instance = form.save(commit=False)
                job_order_instance.save()
                return HttpResponse(status=204,headers={'HX-Trigger':'joborderChanged'})
        else:
            form = JobOrderModelForm(instance=order,
                initial = {
                    'executive': order.executive,
                    'client': order.client,
                    'deadline': order.deadline,
                }
                )
            return render(request, 'manufacturing/edit-order.html', {'form': form, 'order': order})
    
    form = JobOrderModelForm(instance=order,
                initial = {
                    'executive': order.executive,
                    'client': order.client,
                    'deadline': order.deadline,
                }
                )
    return render(request, 'manufacturing/dashboard.html', {'form': form, 'order': order})

def delete_job_order(request, job_id): 
    order = JobOrder.objects.get(id=job_id)
    order.delete()
    orders = JobOrder.objects.all()
    return render(request, 'manufacturing/partials/job-order-list.html', {'orders': orders})

def upload_document(request, job_id):
    user = request.user
    order = JobOrder.objects.get(id=job_id)
    if order.executive.username == user.username or user.groups.first().name == 'admin':
        if request.method == 'POST':
            file_form = FileModelForm(request.POST, request.FILES)
            print(file_form.is_valid())
            if file_form.is_valid():
                files = request.FILES.getlist('file')
                print(files)
                for f in files:
                    file_instance = JobOrderFile(file=f, order=order)
                    print('file-instance: ', file_instance.file.url)
                    file_instance.save()
                return HttpResponse(status=204,headers={'HX-Trigger':'joborderChanged'})
            else:
                return redirect('manufacturing-dashboard')
        else:
            file_form = FileModelForm()
            return file_form
    else:
        file_form = FileModelForm()
        return file_form

def delete_job_order_file(request, document_id):
    if request.method == 'POST':
        document = JobOrderFile.objects.get(id=document_id)
        order_instance_id = JobOrder.objects.get(files__id=document.id).id
        document.delete()
    return redirect('order-detail', order_instance_id)

def personel_list(request):
    workers = User.objects.filter(groups__name='worker')
    context = {'workers': workers}
    return render(request, 'manufacturing/partials/personel-list.html', context)

def create_task(request, taskflow_id):
    taskflow = TaskFlow.objects.get(id=taskflow_id)
    form = TaskForm()
    workers = User.objects.filter(groups__name='worker')
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        workers = request.POST.getlist('workers')
        if task_form.is_valid():
            task_instance = task_form.save(commit=False)
            for worker_id in workers:
                task_instance.workers.add(User.objects.get(id=worker_id))
            if not task_instance.taskflow:
                task_instance.taskflow = taskflow
            task_instance.save()
            return HttpResponse(status=204)
    else:
        context = {'taskflow': taskflow, 'form': form, 'workers': workers}
        return render(request, 'manufacturing/partials/task-form.html', context)

def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    form = TaskForm(instance=task)
    workers = User.objects.filter(groups__name='worker')
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        workers = request.POST.getlist('workers')
        if task_form.is_valid():
            task_instance = task_form.save(commit=False)
            for worker_id in workers:
                if not User.objects.get(id=worker_id) in task_instance.workers.all():
                    task_instance.workers.add(User.objects.get(id=worker_id))
            task_instance.save()
            return HttpResponse(status=204)
    else:
        context = {'form': form, 'task':task, 'editview': True, 'workers': workers}
        return render(request, 'manufacturing/partials/task-form.html', context)

def delete_task(request, task_id, taskflow_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    tasks = Task.objects.filter(taskflow__id=taskflow_id)
    return render(request, 'manufacturing/partials/task-list.html', {'tasks': tasks})

def task_list(request, taskflow_id):
    tasks = Task.objects.filter(taskflow__id=taskflow_id)
    return render(request, 'manufacturing/partials/task-list.html', {'tasks': tasks})