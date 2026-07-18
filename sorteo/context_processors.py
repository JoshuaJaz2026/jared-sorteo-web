from django.utils import timezone
from datetime import timedelta
import json
from .models import Participante

def metricas_sorteo(request):
    # 1. TARJETAS Y FINANZAS
    validados = Participante.objects.filter(participando=True).count()
    pendientes = Participante.objects.filter(participando=False).count()
    
    recaudado = validados * 10
    dinero_pendiente = pendientes * 10
    
    # 2. MAGIA DE LA META (Barra de progreso)
    meta_boletos = 100
    porcentaje_meta = int((validados / meta_boletos) * 100) if meta_boletos > 0 else 0
    porcentaje_visual = min(porcentaje_meta, 100)
    faltan_boletos = max(meta_boletos - validados, 0)

    # ==========================================
    # 📊 NUEVO: LÓGICA DEL GRÁFICO (Últimos 7 días)
    # ==========================================
    hoy = timezone.now().date()
    fechas = []
    registros = []
    
    # Retrocedemos 6 días hacia atrás hasta llegar a hoy (7 días en total)
    for i in range(6, -1, -1):
        fecha_busqueda = hoy - timedelta(days=i)
        # Contamos los clientes cuya fecha de registro coincida con ese día
        cantidad = Participante.objects.filter(fecha_registro__date=fecha_busqueda).count()
        
        # Guardamos la fecha en formato "Día/Mes" (ej. 16/07) y su cantidad
        fechas.append(fecha_busqueda.strftime("%d/%m"))
        registros.append(cantidad)

    # Enviamos todo al diseño
    return {
        'dash_validados': validados,
        'dash_recaudado': recaudado,
        'dash_pendientes': pendientes,
        'dash_dinero_pendiente': dinero_pendiente,
        'meta_boletos': meta_boletos,
        'porcentaje_meta': porcentaje_meta,
        'porcentaje_visual': porcentaje_visual,
        'faltan_boletos': faltan_boletos,
        # Variables convertidas a formato JSON para que Chart.js las lea
        'chart_fechas': json.dumps(fechas),
        'chart_registros': json.dumps(registros),
    }