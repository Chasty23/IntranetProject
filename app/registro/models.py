from django.db import models
from academico.models import ExpedienteEstudiante, Materia

class CicloAcademico(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: "Ciclo 01-2026"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(ExpedienteEstudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(CicloAcademico, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.carnet} - {self.materia.nombre} ({self.ciclo.nombre})"

    class Meta:
        permissions = [
            ("puede_gestionar_registro", "Puede gestionar inscripciones y ciclos"),
        ]
