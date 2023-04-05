from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manufacturing/', include('manufacturing.urls')),
    path('accounting/', include('accountance.urls')),
    path('marketing/', include('marketing.urls')),
    path('hr/', include('humanresources.urls')),
    path('logistics/', include('logistics.urls')),
    path('qc/', include('qualitycontrol.urls')),
    path('general/', include('general.urls')),
    path('purchasing/', include('purchasing.urls')),
]
