from django.db import models

class Participante(models.Model):
    nombre_completo = models.CharField(max_length=255)
    dni = models.CharField(max_length=15, unique=True)
    celular = models.CharField(max_length=20)
    correo = models.EmailField(max_length=255, blank=True, null=True)
    participando = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sorteo_participantes' # Conecta exactamente con la tabla de Neon
        managed = False # Le dice a Django que la tabla ya fue creada por ti manualmente

    def __str__(self):
        return f"{self.nombre_completo} - {self.dni}"