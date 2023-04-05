from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#GENERAL
    path('hx/create-product-form/<str:joborder_id>', views.create_product_form, name='create-product-form'),
    path('create-product/<str:joborder_id>', views.create_product, name='create-product'),
    path('product-list-from-order/<str:order_id>', views.product_list_from_order, name='product-list-from-order'),
    path('get-orders-from-client/<str:client_id>', views.get_orders_from_client, name='get-orders-from-client'),
    path('create-order', views.create_order, name='create-order'),
    path('update-order/<str:orderid>', views.update_order, name='update-order'),
    path('order-list', views.order_list, name='order-list'),
    path('get-stock-list', views.get_stock_list, name='get-stock-list'),
    path('create-stock', views.create_stock, name='create-stock'),
    path('update-stock/<str:stock_id>', views.update_stock, name='update-stock'),
    path('get-supplier-list', views.get_supplier_list, name='get-supplier-list'),
    path('create-supplier/', views.create_supplier, name='create-supplier'),
    path('edit-supplier/<str:supplier_id>', views.edit_supplier, name='edit-supplier'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)