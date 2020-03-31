from django.shortcuts import render, redirect, get_object_or_404
from .forms import fieldForm
from .models import sportField
from openrouteservice.directions import directions
from openrouteservice import convert
import urllib
import requests
import openrouteservice 
import json
import geocoder

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

    if location != "ALL":
        for field in fielddata:
            if field['KAUPUNGINOSA'] == location:
                limitedData.append(field)
    else:
        limitedData = fielddata


    #https://simpleisbetterthancomplex.com/tutorial/2018/04/03/how-to-integrate-highcharts-js-with-django.html
    allFields = list()
    winter = list()
    hockey = list()
    
    for field in limitedData:
        allFields.append(field['ALUE_NIMI'])
        if field['ERITYISKAYTTO'] == 'JÄÄKIEKKO':
            hockey.append(field['ALUE_NIMI'])
        if field['KP_KAUSI'] == 'KESÄ / TALVI':
            winter.append(field['ALUE_NIMI'])

    all_use = {
        'name': 'Kaikki urheilukentät',
        'data': [len(allFields)],
        'color': 'green'
    }
    winter_use = {
        'name': 'Talvikäyttöön soveltuvat',
        'data': [len(winter)],
        'color': 'blue'
    }
    hockey_use = {
        'name': 'Jääkiekkoon soveltuvat',
        'data': [len(hockey)],
        'color': 'red'
    }
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Kenttien käyttö'},
        'series': [all_use, winter_use, hockey_use]    
        }
    dump = json.dumps(chart)

    return render (request, 'sportFields/api.html', {'fielddata': limitedData, 'chart': dump})

def map(request, fName, kOsa):
    mapUrl = 'https://nominatim.openstreetmap.org/?addressdetails=1&q='+fName+'+'+kOsa+'&format=json&limit=1'
    response = requests.get(mapUrl)
    data = response.json()
    lat = []
    lon = []
    if data == []:
        print ("Kenttaa ei loytynyt kartalta")
        return redirect ('api')
    else:
        for field in data:
            lat = field['lat'] 
            lon = field['lon']

    # https://openrouteservice-py.readthedocs.io/en/latest/
    myLocation = geocoder.ip('me').latlng
    coords = ((myLocation[1],myLocation[0]),(lon, lat))
    client = openrouteservice.Client(key='5b3ce3597851110001cf624802b884428e944a01b97a52106fc5f74f') # Specify your personal API key
    routes = client.directions(coords)
    geometry =  routes['routes'][0]['geometry'] #Geometriatiedot
    decoded = convert.decode_polyline(geometry) #Hakee 'coordinates': [[lon, lan][lon,lan] yms...]
    route = decoded['coordinates'] #Lista koordinaateista
    for point in route:
        point.reverse() # [lon, lat] -> [lat, lon]

    return render(request, 'sportFields/map.html', {'lat': lat, 'lon': lon, 'fName': fName, 'route': route, 'myLocation': myLocation})


# Ei toteutusta
# def index(request):
#     fields = sportField.objects.all()
#     return render(request, 'sportFields/index.html', {'fields': fields})

# def create(request):
#     if request.method == 'POST':
#         form = fieldForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     form = fieldForm()

#     return render(request, 'sportFields/create.html', {'form': form})

# def edit(request, pk):
#     field = sportField.objects.get(pk=pk)
#     form = fieldForm(request.POST, instance=field)
#     if form.is_valid():
#         form.save()
#         return redirect('index')
#     return render(request, 'sportFields/edit.html', {'form':form} )

# def delete(request, pk):
#     field = sportField.objects.get(pk=pk)
#     field.delete()
#     return redirect ("index")
