from django.db import models


class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=120)
    isbn = models.CharField(max_length=20, unique=True)
    ejemplares_totales = models.PositiveIntegerField(default=1)
    ejemplares_disponibles = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['titulo']
        permissions = [
            ('puede_gestionar_biblioteca', 'Puede gestionar libros y prestamos'),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Prestamo(models.Model):
    ESTADOS = [
        ('ACT', 'Activo'),
        ('DEV', 'Devuelto'),
        ('ATR', 'Atrasado'),
    ]

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='prestamos',
    )
    expediente = models.ForeignKey(
        'academico.ExpedienteEstudiante',
        on_delete=models.CASCADE,
        related_name='prestamos_biblioteca',
    )
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.CharField(max_length=3, choices=ESTADOS, default='ACT')

    class Meta:
        ordering = ['-fecha_prestamo']

    def __str__(self):
        return f"{self.expediente.carnet} - {self.libro.titulo}"

