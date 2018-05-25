from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newGait/<int:person_id>/', views.newGait, name='newGait'),
]