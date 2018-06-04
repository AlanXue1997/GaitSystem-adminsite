from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'control'
urlpatterns = [
    path('', views.index, name='index'),

    # log in / log out
    path('login/', auth_views.LoginView.as_view(template_name='control/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),

    # Gait
    path('newGait/<int:person_id>/', views.newGait, name='newGait'),

    # Person
    path('persons/', views.persons, name='persons'),
    path('person/<int:person_id>/', views.person, name='person'),

    # Door
    path('doors/', views.doors, name='doors'),
    path('door/<int:door_id>', views.door, name='door'),
    path('door2/<int:door_id>/<int:x>/<int:y>/', views.door2, name='door2'),

    # API
    path('doorquery/<int:door_id>/', views.doorQuery, name='doorQuery'),
]