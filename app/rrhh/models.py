from django.db import models

from django.db import models

# modelo que representa a un empleado en el sistema de RRHH
class Empleado(models.Model):
    TIPOS = [
        ('DOC', 'Docente'),
        ('ADM', 'Administrativo'),
        ('SER', 'Servicios'),
    ]
    nombre = models.CharField(max_length=150)
    dui = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=3, choices=TIPOS)
    puesto = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.puesto}"

    class Meta:
        # Permiso para los usuarios de "Modificación"
        permissions = [
            ("puede_gestionar_rrhh", "Puede editar datos de empleados"),
        ]