from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
import folium
from .models import Search
from .forms import SearchForm
import geocoder

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm
        
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat==None or lng==None:
        address.delete()
        return HttpResponse('Không hợp lệ!')
    #Tao Map
    m = folium.Map(location=[19,-12], zoom_start=2)
    folium.Marker([lat, lng], tooltip='Click for More',
                popup=country).add_to(m)
    #Trinh Chieu Map
    m = m._repr_html_()
    context={
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)