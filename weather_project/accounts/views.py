from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, CreateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.forms.utils import ErrorList
from accounts.models import AccountCity
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError
# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:cities')


class RegisterFormView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:cities')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class AccountCityListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/accountcity_list.html'
    model = AccountCity
    context_object_name = 'cities'

    def get_context_data(self, *args, **kwargs):
        # Enter your API key from OpenWeatherMap
        #api_key =
        context = super().get_context_data(*args, **kwargs)
        cities_list = list(context['cities'].filter(
            user=self.request.user).values_list('city_name'))
        context['object_list'] = context['object_list'].filter(
            user=self.request.user)
        context['cities'] = [cities_list[i][0] for i in range(len(cities_list))]
        for i in range(len(cities_list)):
            city_input = cities_list[i][0]

            city_input = city_input.strip()
            city_input = urllib.parse.quote(city_input)
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
                city_input + '&units=metric&appid=' + api_key

            try:
                response = urllib.request.urlopen(url)
                status_code = response.getcode()
            except HTTPError as e:
                error_data = {
                    'city': city_input,
                    'message': 'City not found',
                }
                error_data['cities_objects'] = context['object_list'][i]
                context['cities'][i] = error_data
                i += 1
                continue

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
                weather_data['cities_objects'] = context['object_list'][i]
                weather_data['city_input'] = city_input
                context['cities'][i] = weather_data
                i += 1

        return context


class AccountCityCreateView(LoginRequiredMixin, CreateView):
    model = AccountCity
    fields = ['city_name']
    success_url = reverse_lazy('accounts:cities')

    def form_valid(self, form):
        form.instance.user = self.request.user
        new_city = form.cleaned_data['city_name']
        city_count = AccountCity.objects.filter(
            city_name=new_city, user=self.request.user).count()
        if city_count > 0:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
                [u'City already exists'])
            return self.form_invalid(form)
        return super(AccountCityCreateView, self).form_valid(form)


class AccountCityDeleteView(LoginRequiredMixin, DeleteView):
    model = AccountCity
    context_object_name = 'city'
    success_url = reverse_lazy('accounts:cities')
