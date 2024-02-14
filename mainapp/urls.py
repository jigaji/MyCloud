from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('create-folder/', views.create_new_folder, name='create_new_folder'),
    path('folder/<str:pk>/', views.open_folder, name='open_folder'),
]
