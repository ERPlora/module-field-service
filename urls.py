from django.urls import path
from . import views

app_name = 'field_service'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('work_orders/', views.work_orders, name='work_orders'),
    path('routes/', views.routes, name='routes'),
    path('settings/', views.settings, name='settings'),
]
