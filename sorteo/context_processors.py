from .models import Participante

def metricas_sorteo(request):
    # Contamos cuántos están marcados y desmarcados
    validados = Participante.objects.filter(participando=True).count()
    pendientes = Participante.objects.filter(participando=False).count()
    
    # Calculamos el dinero multiplicando por S/ 10.00
    recaudado = validados * 10
    dinero_pendiente = pendientes * 10
    
    # ==========================================
    # 🎯 MAGIA DE LA META (Barra de progreso)
    # ==========================================
    meta_boletos = 100  # <-- ¡Puedes cambiar este número cuando quieras!
    
    # Calculamos el porcentaje matemático
    porcentaje_meta = int((validados / meta_boletos) * 100) if meta_boletos > 0 else 0
    
    # Evitamos que la barra visual se rompa si pasas del 100% (si vendes más de 100)
    porcentaje_visual = min(porcentaje_meta, 100)
    
    # Calculamos cuántos faltan
    faltan_boletos = max(meta_boletos - validados, 0)
    
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
    }