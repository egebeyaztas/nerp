from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.marketing_dashboard, name='marketing-dashboard'),
#MARKETING
    path('hx/update-marketing-form/<str:id>', views.update_marketing_data_form, name='update-marketing-form'),
    path('update-marketing/<str:id>', views.update_marketing_data, name='update-marketing-data'),
    path('create-potential-client', views.create_potential_client, name='create-potential-client'),
    path('update-potential-client/<str:pclient_id>', views.update_potential_client, name='update-potential-client'),
    path('get-potential-client-list', views.get_potential_client_list, name='get-potential-client-list'),
    path('create-ads', views.create_ads, name='create-ads'),
    path('update-ads/<str:ad_id>', views.update_ads, name='update-ads'),
    path('get-ads-list', views.get_ads_list, name='get-ads-list'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)