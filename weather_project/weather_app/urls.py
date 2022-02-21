from django.urls import path
from weather_app import views

app_name = 'weather_app'

urlpatterns = [
    path('',views.WeatherTemplateView.as_view(),name='weather'),
]
