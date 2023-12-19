from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('surfting/', views.surfting, name='surfting'),
    path('check_task_status/', views.check_task_status, name='check_task_status'),
    path('surfting/<int:surfter_task_id>/', views.surfting, name='surfting'),
    path('results/', views.results, name='results'),
    path('savedsurfts/', views.savedsurfts, name='savedsurfts')
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)