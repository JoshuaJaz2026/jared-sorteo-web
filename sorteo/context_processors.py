from .models import Participante

def metricas_sorteo(request):
    # Calculamos los datos en tiempo real
    validados = Participante.objects.filter(participando=True).count()
    pendientes = Participante.objects.filter(participando=False).count()
    recaudado = validados * 10
    
    # Enviamos estas variables al diseño del panel
    return {
        'dash_validados': validados,
        'dash_pendientes': pendientes,
        'dash_recaudado': recaudado,
    }