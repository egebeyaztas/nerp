from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#QUALITY CONTROL
    path('', views.qc_dashboard, name='qc-dashboard'),
    path('create-qc-order', views.create_quality_control_order, name='create-qc-order'),
    path('update-qc-order/<str:qid>', views.update_quality_control_order, name='update-qc-order'),
    path('approve-product/<str:qid>/<str:product_id>', views.approve_product, name='approve-product'),
    path('get-qc-lists', views.get_qc_lists, name='get-qc-lists'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)