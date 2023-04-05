from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.logistics_dashboard, name='logistics-dashboard'),
#LOGISTICS
    path('hx/update-logistic-form/<str:logistic_id>', views.update_logistics_form, name='update-logistic-form'),
    path('hx/create-logistic-form', views.create_logistics_form, name='create-logistic-form'),
    path('update-logistic/<str:logistic_id>', views.update_logistics, name='update-logistic-data'),
    path('create-logistic', views.create_logistics, name='create-logistic-data'),
    path('logistics-list/<str:code>', views.logistics_list, name='logistics-list'),
    path('logistics-list-expanded', views.logistics_list_expanded, name='logistic-list-expanded'),
    path('delete-logistic/<str:id>', views.delete_logistics, name='delete-logistic-data'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)