from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError
# Create your views here.


class WeatherTemplateView(TemplateView):
    template_name = 'weather_app/weather.html'

    def get_context_data(self, *args, **kwargs):
        # Enter your API key from OpenWeatherMap
        #api_key =
        context = super().get_context_data(*args, **kwargs)

        search_input = self.request.GET.get('search-area')
        if search_input:
            search_input = search_input.strip()
            search_input = urllib.parse.quote(search_input)
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
                search_input + '&units=metric&appid=' + api_key

            try:
                response = urllib.request.urlopen(url)
                status_code = response.getcode()
            except HTTPError as e:

                context['error_message'] = {'message': 'City not found'}
                return context

            if status_code == 200:
                data = json.loads(response.read())
                weather_data = {
                    'city': str(data['name']),
                    'description': str(data['weather'][0]['description']),
                    'icon': str(data['weather'][0]['icon']),
                    'temperature': str(data['main']['temp']),
                    'pressure': str(data['main']['pressure']),
                    'humidity': str(data['main']['temp']),
                    'wind': str(data['wind']['speed']),
                    'country': str(data['sys']['country']),
                }
                context['data'] = weather_data
                return context
