from django.contrib import admin
from django.urls import path
from sorteo.views import landing_sorteo  # Importamos tu nueva función

urlpatterns = [
    path('admin/', admin.site.urls),  # Tu panel secreto para la contadora
    path('', landing_sorteo, name='landing_sorteo'),  # Tu Landing Page pública
]