from django.contrib import admin
from django.urls import path
from sorteo.views import landing_sorteo, ver_boleto, salir_sistema

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos la ruta principal con la función correcta: landing_sorteo
    path('', landing_sorteo, name='landing_sorteo'),
    # Ruta para los tickets digitales
    path('boleto/<int:participante_id>/', ver_boleto, name='ver_boleto'),
    # NUEVA RUTA DE SALIDA:
    path('salir/', salir_sistema, name='salir_sistema'),
]