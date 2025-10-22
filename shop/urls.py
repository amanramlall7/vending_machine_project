from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vending/', views.vending_machine, name='vending_machine'),
    path('process-purchase/', views.process_purchase, name='process_purchase'),
    path('history/', views.purchase_history, name='purchase_history'),

    # Admin panel routes
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<int:id>/', views.update_product, name='update_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
]