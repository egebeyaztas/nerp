from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from scripts.keygen import KeyGenerator
from datetime import datetime
import os
import time
from general.models import Client, Order, Product, ProductGroup

keygenerator = KeyGenerator(15)

jobOrder_status = (
    ('Açıldı','Açıldı'),
    ('Devam ediyor','Devam ediyor'),
    ('Tamamlandı','Tamamlandı'),
)

def file_path(instance, filename):
    try:
        return f'manufacturing/orders/{str(instance.order.id)}/{filename}'
    except Exception as e:
        print(e)

class JobOrder(models.Model):
    executive = models.ForeignKey(User, blank=False, null=True, related_name='ordered', limit_choices_to={'groups__name':'executive'}, on_delete=models.SET_NULL)

    status = models.CharField(max_length=250, choices=jobOrder_status, default=jobOrder_status[0][0])
    finished = models.BooleanField(default=False)
    product_quantity = models.IntegerField(null=False, blank=False, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL, related_name="job_orders")
    order = models.ForeignKey(Order, blank=True, null=True, related_name='job_orders', on_delete=models.SET_NULL)
    deadline = models.DateTimeField(blank=True, null=True)
    job_order_id = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self) -> str:
        return 'Job Order - ' + str(self.date_created) + ' - ' + str(self.id)

    def status_countinue(self):
        if len(self.workers.all()) > 0:
            self.status = jobOrder_status[1][1]
            self.save()
        else:
            return 'No worker assigned to this job order.'

    def status_finished(self):
        if len(self.workers.all()) == 0:
            self.status = jobOrder_status[2][2]
            self.finished = True
            self.save()
        else:
            return 'Order has not finished yet.'

    def calculate_end_time(self):
        if len(self.workers.all()) == 0:
            self.end_time = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
            self.save()
        else:
            return 'Order has not finished yet'

    def add_worker(self, worker):
        worker_group = Group.objects.get(name='worker')
        if worker in worker_group.user_set.all():
            if not worker in self.workers.all():
                self.workers.add(worker)
                self.save()
    
    def remove_worker(self, worker):
        if worker in self.workers.all():
            self.workers.remove(worker)

    def delete(self, *args, **kwargs):
        for file in self.files.all():
            file.file.delete()
        super().delete(*args, **kwargs)

class JobOrderFile(models.Model):
    file = models.FileField(upload_to=file_path, max_length=250, null=False, blank=False)
    order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='files')
    
    def __str__(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

class TaskFlow(models.Model):
    job_order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name="task_flow")

    def __str__(self):
        return self.job_order.job_order_id + ' - Görev Akışı'

class Task(models.Model):
    task = models.CharField(max_length=240, blank=False, null=False)
    taskflow = models.ForeignKey(TaskFlow, on_delete=models.CASCADE, blank=False, null=False, related_name="tasks")
    workers = models.ManyToManyField(User, blank=True, null=True, related_name='tasks', limit_choices_to={'groups__name':'worker'})
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(blank=True, null=True, auto_now_add=False)
    task_notes = models.TextField(max_length=1200, blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.taskflow.job_order.job_order_id + ' - Görev ' + self.id

