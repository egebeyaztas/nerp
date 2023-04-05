from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.manufacturing_dashboard, name='manufacturing-dashboard'),
        path('hx/create-job-order-form', views.create_job_order_form, name='create-job-order-form'),
        path('hx/edit-job-order-form/<str:job_id>', views.edit_job_order_form, name='edit-job-order-form'),
        path('job-order-list', views.job_order_list, name='job-order-list'),
        path('personel-list', views.personel_list, name='manufacturing-personel-list'),
        path('create-job-order', views.create_job_order, name='create-job-order'),
        path('edit-job-order/<str:job_id>', views.edit_job_order_detail, name='edit-job-order'),
        path('delete-order/<str:job_id>', views.delete_job_order, name='delete-order'),
        path('order-detail/<str:job_id>', views.job_order_detail_view, name='order-detail'),
        path('upload-document/<str:job_id>', views.upload_document, name='upload-document'),
        path('delete-job-order-file/<str:document_id>', views.delete_job_order_file, name='delete-job-order-file'),
        path('create-task/<str:taskflow_id>', views.create_task, name='create-task'),
        path('update-task/<str:task_id>', views.update_task, name='update-task'),
        path('update-task/<str:task_id>/<str:taskflow_id>', views.delete_task, name='delete-task'),
        path('task-list/<str:taskflow_id>', views.task_list, name='task-list'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    