from django.urls import path
from phish import views

app_name = 'phish'
urlpatterns = [
    path('', views.index, name="index"),
    path('checkPhish/', views.check_phish, name='check_phish')
]