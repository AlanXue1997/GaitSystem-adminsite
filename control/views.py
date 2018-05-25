from django.shortcuts import render, get_object_or_404

from .models import Person

def index(request):
    return render(request, 'control/index.html')

def newGait(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    return render(request,'control/newGait.html', { 'person': person })