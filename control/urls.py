from django.urls import path

from . import views

app_name = 'control'
urlpatterns = [
    path('', views.index, name='index'),

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