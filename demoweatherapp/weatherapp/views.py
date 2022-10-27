from django.views.generic import TemplateView
from django.contrib.gis.geoip2 import GeoIP2
import requests 
import json

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
class HomeView(TemplateView):
    template_name = "weatherapp/index.html"

    def get_context_data(self,**kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        g = GeoIP2()
        ip = get_client_ip(self.request)# for dynamic ip finding
        lon_lat_data = g.lon_lat('144.48.110.34')
        longitude = int(lon_lat_data[0])
        latitude = int(lon_lat_data[1])
        url = f"https://weather-proxy.freecodecamp.rocks/api/current?lat={latitude}&lon={longitude}"
        x = requests.get(url)
        data = json.loads(x.text)
        temparature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        icon_url = data["weather"][0]["icon"]
        city = data["name"]
        country_code = data["sys"]["country"]
        user_data = {
            'temparature':temparature,
            'temparature_feels_like' : feels_like,
            'humidity' : humidity,
            'icon_url': icon_url,
            'city' : city,
            'country_code' : country_code,
        }
        context['data']=user_data
        return context