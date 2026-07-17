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
    
    # Interruptor editable desde la tabla
    list_editable = ('participando',)
    
    # Filtros laterales
    list_filter = ('participando', 'fecha_registro')
    
    # Buscador superior
    search_fields = ('nombre_completo', 'dni', 'celular')
    
    # ¡NUEVO! Ordenamiento inteligente: Los más recientes siempre arriba
    ordering = ('-fecha_registro',)
    
    # Acciones Mágicas
    actions = ['marcar_como_validados', 'elegir_ganador', 'exportar_a_csv']

    # --- FUNCIÓN: VALIDACIÓN MASIVA ---
    @admin.action(description='✅ Marcar seleccionados como Validados (Participando)')
    def marcar_como_validados(self, request, queryset):
        actualizados = queryset.update(participando=True)
        self.message_user(
            request, 
            f"¡Éxito! Se han validado {actualizados} participantes correctamente.", 
            level=messages.SUCCESS
        )

    # --- FUNCIÓN: ELEGIR GANADOR ---
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

    # --- FUNCIÓN: EXPORTAR A EXCEL ---
    @admin.action(description='📊 Descargar base de datos (Excel/CSV)')
    def exportar_a_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="participantes_jared.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nombre Completo', 'DNI', 'Celular', 'Validado (Participando)', 'Fecha de Registro'])
        
        for participante in queryset:
            writer.writerow([
                participante.nombre_completo,
                participante.dni,
                participante.celular,
                'Sí' if participante.participando else 'No',
                participante.fecha_registro.strftime("%d/%m/%Y %H:%M")
            ])
            
        return response