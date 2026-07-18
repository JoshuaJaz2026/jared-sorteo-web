from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import logout
from .models import Participante

def landing_sorteo(request):
    # 🛑 MAGIA DE AUTO-CIERRE: Verificamos el límite
    meta_boletos = 100 # <-- Cambia este número temporalmente a 1 o 0 para probar
    validados_actuales = Participante.objects.filter(participando=True).count()
    
    sorteo_agotado = validados_actuales >= meta_boletos

    if request.method == 'POST':
        # Si alguien intenta mandar datos cuando ya está agotado, lo bloqueamos
        if sorteo_agotado:
            return redirect('landing_sorteo')

        nombre = request.POST.get('nombre_completo')
        dni = request.POST.get('dni')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')

        try:
            # Intentamos guardarlo en la base de datos
            Participante.objects.create(
                nombre_completo=nombre,
                dni=dni,
                celular=celular,
                correo=correo
            )
            # Si tiene éxito, va a la pantalla de Yape
            return render(request, 'sorteo/exito.html', {'dni': dni})
            
        except IntegrityError:
            # Si el DNI ya existe, la BD lanza un IntegrityError.
            return render(request, 'sorteo/landing.html', {
                'error': 'Este DNI ya se encuentra participando en el sorteo.',
                'sorteo_agotado': sorteo_agotado
            })

    # Si solo entra a mirar, le mostramos la página normal enviándole el estado del sorteo
    return render(request, 'sorteo/landing.html', {'sorteo_agotado': sorteo_agotado})


def ver_boleto(request, participante_id):
    # Buscamos al participante por su ID
    participante = get_object_or_404(Participante, id=participante_id)
    
    # Renderizamos el diseño del ticket enviando los datos
    return render(request, 'sorteo/boleto.html', {'p': participante})

# 🚪 NUEVO: Función para cerrar sesión a la fuerza
def salir_sistema(request):
    logout(request)
    return redirect('/admin/') # Lo devuelve a la pantalla de login