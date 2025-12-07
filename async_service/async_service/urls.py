from django.contrib import admin
from django.urls import path
from app.views import calculate_energy, health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculate/', calculate_energy, name='calculate-energy'),
    path('health/', health_check, name='health-check'),
]