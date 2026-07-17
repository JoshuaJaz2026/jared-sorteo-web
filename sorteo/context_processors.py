from .models import Participante

def metricas_sorteo(request):
    # Contamos cuántos están marcados y desmarcados
    validados = Participante.objects.filter(participando=True).count()
    pendientes = Participante.objects.filter(participando=False).count()
    
    # Calculamos el dinero multiplicando por S/ 10.00
    recaudado = validados * 10
    dinero_pendiente = pendientes * 10
    
    # Enviamos todo al diseño
    return {
        'dash_validados': validados,
        'dash_recaudado': recaudado,
        'dash_pendientes': pendientes,
        'dash_dinero_pendiente': dinero_pendiente,
    }