import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count



from .models import Person, Door

def index(request):
    return render(request, 'control/index.html')

# --------------------
# Gait
# --------------------
def newGait(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    return render(request,'control/newGait.html', { 'person': person })

# --------------------
# Person
# --------------------
def persons(request):
    persons = Person.objects.all()
    return render(request, 'control/persons.html', {'persons': persons })

def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    table = dict(
        zip(
            [timezone.now() - datetime.timedelta(hours=i * 4) for i in range(1, 25)]
            ,
            [[person.dooropen_set.filter(Q(dt__gte=timezone.now() - datetime.timedelta(hours=i * 4)) & Q(dt__lt=timezone.now() - datetime.timedelta(hours=(i - 1) * 4)) & Q(door__level=str(j))).count() for j in range(1, 4)] for i in range(1, 25)]
        )
    )
    doors = person.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3)).values('door__id', 'door__name').annotate(num=Count('door__id')).order_by('-num')
    logs = person.dooropen_set.all().order_by('-dt')[:10]
    methods = person.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3)).values('method').annotate(num=Count('method'))
    return render(request, 'control/person.html', {'person':person, 'table': table, 'doors':doors, 'logs': logs, 'methods': methods})

# --------------------
# Door
# --------------------
def doors(request):
    doors = Door.objects.all()
    return render(request, 'control/doors.html', {'doors' : doors })

def door(request, door_id):
    door = get_object_or_404(Door, pk=door_id)
    table = dict(
        zip(
            [timezone.now() - datetime.timedelta(hours=i*4) for i in range(1, 25)]
        ,
            [ [door.dooropen_set.filter(Q(dt__gte=timezone.now() - datetime.timedelta(hours=i*4)) & Q(dt__lt=timezone.now() - datetime.timedelta(hours=(i-1)*4)) & Q(person__privilege=str(j))).count() for j in range(1,4)] for i in range(1, 25)]
        )
    )
    persons = door.dooropen_set.filter(dt__gte=timezone.now()-datetime.timedelta(days=3)).values('person__id', 'person__name').annotate(num=Count('person__id')).order_by('-num')[:5]
    logs = door.dooropen_set.all().order_by('-dt')[:10]
    methods = door.dooropen_set.filter(dt__gte=timezone.now()-datetime.timedelta(days=3)).values('method').annotate(num=Count('method'))
    return render(request, 'control/door.html', {'door': door, 'table': table, 'persons': persons, 'logs': logs, 'methods':methods})

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
    methods = door.dooropen_set.filter(dt__gte=timezone.now() - datetime.timedelta(days=3)).values('method').annotate(num=Count('method'))
    return render(request, 'control/door.html', {'door': door, 'table': table, 'persons': persons, 'logs': logs, 'methods': methods})

# --------------------
# API
# --------------------
@csrf_exempt
def doorQuery(request, door_id):
    door = get_object_or_404(Door, pk=door_id)
    if request.method == 'POST':
        st1 = request.POST['st1']
        st2 = request.POST['st2']
        return HttpResponse(st1)
    else:
        return HttpResponse(str(door.name)+ ' (it\'s not a POST)')
