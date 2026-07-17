from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
import random
import csv
from .models import Participante

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    # Columnas que ves en la tabla
    list_display = ('nombre_completo', 'dni', 'celular', 'participando', 'fecha_registro')
    
    # Filtros laterales
    list_filter = ('participando', 'fecha_registro')
    
    # Buscador superior
    search_fields = ('nombre_completo', 'dni', 'celular')
    
    # ¡AQUÍ REGISTRAMOS NUESTRAS 2 ACCIONES MÁGICAS!
    actions = ['elegir_ganador', 'exportar_a_csv']

    @admin.action(description='🎁 Elegir un ganador al azar (Solo Validados)')
    def elegir_ganador(self, request, queryset):
        candidatos = Participante.objects.filter(participando=True)
        
        if not candidatos.exists():
            self.message_user(
                request, 
                "⚠️ Error: No hay participantes con el pago validado para hacer el sorteo.", 
                level=messages.ERROR
            )
            return
        
        ganador = random.choice(candidatos)
        mensaje_triunfal = f"🎉 ¡TENEMOS GANADOR! 🎉 El afortunado es {ganador.nombre_completo} (DNI: {ganador.dni}) - Llámalo ya al {ganador.celular}"
        self.message_user(request, mensaje_triunfal, level=messages.SUCCESS)

    @admin.action(description='📊 Descargar base de datos (Excel/CSV)')
    def exportar_a_csv(self, request, queryset):
        # 1. Preparamos el archivo descargable
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="participantes_jared.csv"'
        
        # 2. Creamos el "escritor" del archivo
        writer = csv.writer(response)
        
        # 3. Escribimos la primera fila (Los títulos de las columnas)
        writer.writerow(['Nombre Completo', 'DNI', 'Celular', 'Validado (Participando)', 'Fecha de Registro'])
        
        # 4. Escribimos los datos de cada cliente seleccionado
        for participante in queryset:
            writer.writerow([
                participante.nombre_completo,
                participante.dni,
                participante.celular,
                'Sí' if participante.participando else 'No',
                participante.fecha_registro.strftime("%d/%m/%Y %H:%M")
            ])
            
        return response