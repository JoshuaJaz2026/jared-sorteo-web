from django.shortcuts import render
from django.db import IntegrityError
from .models import Participante

def landing_sorteo(request):
    if request.method == 'POST':
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
            # Lo atrapamos y devolvemos a la landing con un mensaje de error.
            return render(request, 'sorteo/landing.html', {
                'error': 'Este DNI ya se encuentra participando en el sorteo.'
            })

    # Si solo entra a mirar, le mostramos la página normal
    return render(request, 'sorteo/landing.html')