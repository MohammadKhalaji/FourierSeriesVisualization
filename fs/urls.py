from . import views
from django.urls import path


urlpatterns = [
    path('', views.signalSubmit),
    path('fourier/<int:pk>', views.fourier, name='fourier'),


]