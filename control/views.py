import datetime

from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

import numpy as np
from sklearn import neighbors

from .models import Person, Door

def index(request):
    return render(request, 'control/index.html')

def logout(request):
    return auth_views.logout_then_login(request,login_url='/control/login')

# --------------------
# Gait
# --------------------
def newGait(request, person_id):
    if request.user.is_authenticated:
        person = get_object_or_404(Person, pk=person_id)
        return render(request, 'control/newGait.html', {'person': person})
    else:
        return render(request, 'control/login.html', {'next': request })

# --------------------
# Person
# --------------------
@login_required(login_url='/control/login/')
def persons(request):
    persons = Person.objects.all()
    return render(request, 'control/persons.html', {'persons': persons })

@login_required(login_url='/control/login/')
def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    table = dict(
        zip(
            [timezone.now() - datetime.timedelta(hours=i * 4 + 150) for i in range(1, 25)]
            ,
            [[person.dooropen_set.filter(Q(dt__gte=timezone.now() - datetime.timedelta(hours=i * 4 + 150)) & Q(dt__lt=timezone.now() - datetime.timedelta(hours=(i - 1) * 4 + 150)) & Q(door__level=str(j))).count() for j in range(1, 4)] for i in range(1, 25)]
        )
    )
    doors = person.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3 + 6)).values('door__id', 'door__name').annotate(num=Count('door__id')).order_by('-num')
    logs = person.dooropen_set.all().order_by('-dt')[:10]
    methods = list(person.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3 + 6)).values('method').annotate(num=Count('method')))
    if len(methods) == 1:
        if methods[0]['method'] == '0':
            methods.append({'method': '1', 'num': 0})
        else:
            methods.insert(0, {'method': '0', 'num': 0})

    return render(request, 'control/person.html', {'person':person, 'table': table, 'doors':doors, 'logs': logs, 'methods': methods})

# --------------------
# Door
# --------------------
@login_required(login_url='/control/login/')
def doors(request):
    doors = Door.objects.all()
    return render(request, 'control/doors.html', {'doors': doors})

@login_required(login_url='/control/login/')
def door(request, door_id):
    door = get_object_or_404(Door, pk=door_id)
    table = dict(
        zip(
            [timezone.now() - datetime.timedelta(hours=i*4+144) for i in range(1, 25)]
        ,
            [ [door.dooropen_set.filter(Q(dt__gte=timezone.now() - datetime.timedelta(hours=i*4+144)) & Q(dt__lt=timezone.now() - datetime.timedelta(hours=(i-1)*4+144)) & Q(person__privilege=str(j))).count() for j in range(1,4)] for i in range(1, 25)]
        )
    )
    persons = door.dooropen_set.filter(dt__gte=timezone.now()-datetime.timedelta(days=3+6)).values('person__id', 'person__name').annotate(num=Count('person__id')).order_by('-num')[:5]
    logs = door.dooropen_set.all().order_by('-dt')[:10]
    methods = list(door.dooropen_set.filter(dt__gte=timezone.now()-datetime.timedelta(days=3+6)).values('method').annotate(num=Count('method')))
    if len(methods) == 1:
        if methods[0]['method'] == '0':
            methods.append({'method': '1', 'num': 0})
        else:
            methods.insert(0, {'method': '0', 'num': 0})

    return render(request, 'control/door.html', {'door': door, 'table': table, 'persons': persons, 'logs': logs, 'methods':methods})

@login_required(login_url='/control/login/')
def door2(request, door_id, x, y):
    door = get_object_or_404(Door, pk=door_id)
    table = dict(
        zip(
            [timezone.now() - datetime.timedelta(hours=i*x) for i in range(1, y+1)]
        ,
            [ [door.dooropen_set.filter(Q(dt__gte=timezone.now() - datetime.timedelta(hours=i*x)) & Q(dt__lt=timezone.now() - datetime.timedelta(hours=(i-1)*x)) & Q(person__privilege=str(j))).count() for j in range(1,4)] for i in range(1, y+1)]
        )
    )
    persons = door.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3)).values('person__id','person__name').annotate(num=Count('person__id')).order_by('-num')[:5]
    logs = door.dooropen_set.all().order_by('-dt')[:10]
    methods = list(
        door.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3)).values('method').annotate(
            num=Count('method')))
    if len(methods) == 1:
        if methods[0]['method'] == '0':
            methods.append({'method': '1', 'num': 0})
        else:
            methods.insert(0, {'method': '0', 'num': 0})
    return render(request, 'control/door.html', {'door': door, 'table': table, 'persons': persons, 'logs': logs, 'methods': methods})

# --------------------
# API
# --------------------
@csrf_exempt
def doorQuery(request, door_id):
    door = get_object_or_404(Door, pk=door_id)
    if request.method == 'POST':
        st1 = request.POST['st1']
        sts = st1.split(' ')
        sts.pop()
        f = open("data.txt")
        data = np.loadtxt(f)

        X = data[:, :66]
        y = data[:, 66]

        testX = [[float(i) for i in sts]]

        n_neighbors = 3
        h = .02  # step size in the mesh

        weights = 'uniform'
        # we create an instance of Neighbours Classifier and fit the data.
        clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
        clf.fit(X, y)

        return HttpResponse(str(int(clf.predict(testX)[0])))
    else:
        return HttpResponse(str(door.name)+ ' (it\'s not a POST)')
