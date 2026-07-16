from django.contrib import admin
from .models import Participante

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    # Columnas que se verán en la tabla
    list_display = ('nombre_completo', 'dni', 'celular', 'participando', 'fecha_registro')
    # Filtros laterales
    list_filter = ('participando', 'fecha_registro')
    # Buscador por texto
    search_fields = ('nombre_completo', 'dni', 'celular')
    # ¡Magia! Permite a la contadora marcar el check de "participando" sin entrar al registro
    list_editable = ('participando',)