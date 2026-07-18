from django.contrib import admin
from django.urls import path
from sorteo.views import guardar_participante, ver_boleto # Agregamos ver_boleto aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', guardar_participante, name='landing'),
    # NUEVA RUTA PARA EL BOLETO:
    path('boleto/<int:participante_id>/', ver_boleto, name='ver_boleto'),
]