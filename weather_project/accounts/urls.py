from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('',views.AccountCityListView.as_view(),name='cities'),
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='weather_app:weather'), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('create-city/', views.AccountCityCreateView.as_view(), name = 'create'),
    path('delete-city/<int:pk>', views.AccountCityDeleteView.as_view(), name = 'delete'),
]
