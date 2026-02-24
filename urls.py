from django.urls import path
from . import views

app_name = 'field_service'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # WorkOrder
    path('work_orders/', views.work_orders_list, name='work_orders_list'),
    path('work_orders/add/', views.work_order_add, name='work_order_add'),
    path('work_orders/<uuid:pk>/edit/', views.work_order_edit, name='work_order_edit'),
    path('work_orders/<uuid:pk>/delete/', views.work_order_delete, name='work_order_delete'),
    path('work_orders/bulk/', views.work_orders_bulk_action, name='work_orders_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
