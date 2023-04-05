from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.purchasing_dashboard, name='purchasing-dashboard'),
#PURCHASING
    path('create-purchase-offer', views.create_purchase_offer, name='create-purchase-offer'),
    path('update-purchase-offer/<str:offer_id>', views.update_purchase_offer, name='update-purchase-offer'),
    path('delete-purchase-offer', views.delete_purchase_offer, name='delete-purchase-offer'),
    path('get-purchase-list', views.get_purchase_list, name='get-purchase-list'),
    path('get-purchase-offers', views.get_purchase_offers, name='get-purchase-offers'),
    path('get-purchase-formset', views.get_purchase_formset, name='get-purchase-formset'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)