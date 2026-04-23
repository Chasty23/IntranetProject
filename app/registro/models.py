from django.db import models


class CicloAcademico(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_inicio']
        permissions = [
            ('puede_gestionar_registro', 'Puede gestionar inscripciones y ciclos'),
        ]

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    expediente = models.ForeignKey(
        'academico.ExpedienteEstudiante',
        on_delete=models.CASCADE,
        related_name='inscripciones',
    )
    materia = models.ForeignKey(
        'academico.Materia',
        on_delete=models.CASCADE,
        related_name='inscripciones',
    )
    ciclo = models.ForeignKey(
        CicloAcademico,
        on_delete=models.CASCADE,
        related_name='inscripciones',
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_registro']
        constraints = [
            models.UniqueConstraint(
                fields=['expediente', 'materia', 'ciclo'],
                name='unique_inscripcion_por_ciclo',
            ),
        ]

    def __str__(self):
        return f"{self.expediente.carnet} - {self.materia.nombre} - {self.ciclo.nombre}"

