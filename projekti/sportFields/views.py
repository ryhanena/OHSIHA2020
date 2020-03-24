from django.shortcuts import render, redirect, get_object_or_404
from .forms import fieldForm
from .models import sportField
import requests


#Jos haluaa limittiä ni perään esim. '&limit=int' 

url = 'https://data.tampere.fi/data/api/action/datastore_search?resource_id=cb796dcb-5a03-4b7b-8c4f-74145b356212'

def api(request):
    if request.method == 'POST':
        location = request.POST['location']
    else:
        location = 'all'
    location = location.upper() #Korjaa jos pieniä kirjaimia
    response = requests.get(url)
    fielddata = response.json()
    fielddata = fielddata['result']
    fielddata = fielddata['records']
    limitedData = []
    if location == "ALL":
        return render (request, 'sportFields/api.html', {'fielddata': fielddata})
    else:
        for field in fielddata:
            if field['KAUPUNGINOSA'] == location:
                limitedData.append(field)
        return render (request, 'sportFields/api.html', {'fielddata': limitedData})


def index(request):
    fields = sportField.objects.all()
    return render(request, 'sportFields/index.html', {'fields': fields})

def detail(request, pk):
    field = get_object_or_404(sportField, pk=pk)
    return render (request, 'sportFields/show.html', {'field': field})

def create(request):
    if request.method == 'POST':
        form = fieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = fieldForm()

    return render(request, 'sportFields/create.html', {'form': form})

def edit(request, pk):
    field = sportField.objects.get(pk=pk)
    form = fieldForm(request.POST, instance=field)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'sportFields/edit.html', {'form':form} )

def delete(request, pk):
    field = sportField.objects.get(pk=pk)
    field.delete()
    return redirect ("index")
