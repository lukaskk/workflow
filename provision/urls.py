"""
URL configuration for provision project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app.views import upload_excel
from app.views import order_list
from app.views import generate_pdf
from app.views import update_database
from app.views import user_list
from app.views import filter_orders_by_pod





urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-task/', views.create_task, name='create_task'),
    path('task-list/', views.task_list, name='task_list'),
    path('edit-task/', views.edit_task, name='edit_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('orders/', order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('orders/filter/<str:name>/', views.filter_orders_by_name, name='filter_orders_by_name'),
    path('orders/by-pod/<str:inicjaly>/', filter_orders_by_pod, name='filter_orders_by_pod'),
    path('orders/<str:order_id>/pdf/', generate_pdf, name='generate_pdf'),
    path('download_photo/<int:photo_id>/', views.download_photo, name='download_photo'),
    path('update-database/', update_database, name='update_database'),
    path('delete-photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/', views.user_list, name='user_list'),
    path('download-orders-excel/<str:name>/', views.download_orders_excel, name='download_orders_excel'),
    path('download-photos/<str:name>/', views.download_photos, name='download_photos'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('download/<str:name>/', views.download_photos_and_excel, name='download_photos_and_excel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
