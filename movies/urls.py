from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.search, name='search'),
    path('', views.index, name='index'),
]
