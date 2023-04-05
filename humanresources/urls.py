from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.hr_dashboard, name='hr-dashboard'),
#----------------------------------------------------------------
    path('hx/update-posemp-form/<str:id>', views.update_possible_employee_form, name='update-posemp-form'),
    path('hx/create-posemp-form', views.create_possible_employee_form, name='create-posemp-form'),
    path('update-posemp/<str:id>', views.update_possible_employee, name='update-possible-employee'),
    path('create-posemp', views.create_possible_employee, name='create-possible-employee'),
    path('delete-posemp/<str:id>', views.delete_possible_employee, name='delete-possible-employee'),
    path('posemp-list', views.posemp_list, name='posemp-list'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)