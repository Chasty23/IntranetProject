from django.db import models
from academico.models import ExpedienteEstudiante

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    existencias = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

class Prestamo(models.Model):
    estudiante = models.ForeignKey(ExpedienteEstudiante, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        estado = "Devuelto" if self.devuelto else "Prestado"
        return f"{self.libro.titulo} → {self.estudiante.carnet} ({estado})"

    class Meta:
        permissions = [
            ("puede_gestionar_biblioteca", "Puede gestionar libros y prestamos"),
        ]
