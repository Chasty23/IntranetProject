from django.db import models
from django.contrib.auth.models import User

# Representacion de una materia en el sistema academico
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.nombre

# representacion del expediente academico de un estudiante, relacionado con el usuario de Django para autenticacion y autorizacion
class ExpedienteEstudiante(models.Model):
    # se relaciona con el usuario de Django para el login
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    carnet = models.CharField(max_length=12, unique=True)
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.carnet} - {self.usuario.get_full_name()}"

class Nota(models.Model):
    estudiante = models.ForeignKey(ExpedienteEstudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        # Permiso personalizado para usuarios que pueden modificar notas, etc
        permissions = [
            ("puede_modificar_notas", "Puede editar calificaciones de estudiantes"),
        ]