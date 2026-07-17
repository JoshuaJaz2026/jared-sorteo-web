from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.utils.html import format_html
import urllib.parse
import random
import csv
from .models import Participante

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    # Columnas que ves en la tabla
    list_display = ('nombre_completo', 'dni', 'celular', 'contactar_whatsapp', 'participando', 'fecha_registro')
    
    # Interruptor editable desde la tabla
    list_editable = ('participando',)
    
    # Filtros laterales
    list_filter = ('participando', 'fecha_registro')
    
    # Buscador superior
    search_fields = ('nombre_completo', 'dni', 'celular')
    
    # Ordenamiento inteligente: Los más recientes siempre arriba
    ordering = ('-fecha_registro',)
    
    # Acciones Mágicas
    actions = ['marcar_como_validados', 'elegir_ganador', 'exportar_a_csv', 'eliminar_participantes']

    # ==========================================
    # 🛡️ CANDADO ANTI-FRAUDE
    # ==========================================
    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return ('nombre_completo', 'dni', 'celular', 'fecha_registro')
        return ('fecha_registro',)

    # ==========================================
    # 💰 NUEVO: MÉTRICA DE DINERO RECAUDADO
    # ==========================================
    def changelist_view(self, request, extra_context=None):
        # 1. Contamos cuántos clientes tienen el check verde de pagado
        validados = Participante.objects.filter(participando=True).count()
        
        # 2. Multiplicamos por S/ 10.00 (el precio del boleto)
        total_recaudado = validados * 10
        
        # 3. Mostramos el mensaje solo si hay al menos una venta
        if validados > 0:
            mensaje = f"💰 TABLERO FINANCIERO: Tienes {validados} boletos validados. Total recaudado en este sorteo: S/ {total_recaudado}.00"
            # Usamos un truco para evitar que el mensaje se repita al recargar
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request, mensaje)
            
        return super().changelist_view(request, extra_context=extra_context)

    # ==========================================
    # 📲 MAGIA DE WHATSAPP
    # ==========================================
    @admin.display(description='Contactar')
    def contactar_whatsapp(self, obj):
        if obj.celular:
            mensaje = f"Hola {obj.nombre_completo}, vi tu registro para el Gran Sorteo Jared. 🇵🇪 Por favor, envíame la captura de tu Yape (S/ 10.00) por aquí para validar tu participación."
            mensaje_codificado = urllib.parse.quote(mensaje)
            enlace = f"https://wa.me/51{obj.celular}?text={mensaje_codificado}"
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #25D366; color: white; padding: 5px 12px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 11px; display: inline-block; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">💬 WhatsApp</a>',
                enlace
            )
        return "-"

    # ==========================================
    # ACCIONES MASIVAS
    # ==========================================
    @admin.action(description='✅ Marcar seleccionados como Validados (Participando)')
    def marcar_como_validados(self, request, queryset):
        actualizados = queryset.update(participando=True)
        self.message_user(request, f"¡Éxito! Se han validado {actualizados} participantes.", level=messages.SUCCESS)

    @admin.action(description='🎁 Elegir un ganador al azar (Solo Validados)')
    def elegir_ganador(self, request, queryset):
        candidatos = Participante.objects.filter(participando=True)
        if not candidatos.exists():
            self.message_user(request, "⚠️ Error: No hay participantes validados.", level=messages.ERROR)
            return
        ganador = random.choice(candidatos)
        mensaje_triunfal = f"🎉 ¡TENEMOS GANADOR! 🎉 {ganador.nombre_completo} (DNI: {ganador.dni}) - Cel: {ganador.celular}"
        self.message_user(request, mensaje_triunfal, level=messages.SUCCESS)

    @admin.action(description='📊 Descargar base de datos (Excel/CSV)')
    def exportar_a_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="participantes_jared.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre Completo', 'DNI', 'Celular', 'Validado', 'Fecha de Registro'])
        for p in queryset:
            writer.writerow([p.nombre_completo, p.dni, p.celular, 'Sí' if p.participando else 'No', p.fecha_registro.strftime("%d/%m/%Y %H:%M")])
        return response

    @admin.action(description='🗑️ Eliminar participantes seleccionados')
    def eliminar_participantes(self, request, queryset):
        cantidad, _ = queryset.delete()
        self.message_user(request, f"🗑️ ¡Listo! Se han eliminado {cantidad} participantes.", level=messages.SUCCESS)