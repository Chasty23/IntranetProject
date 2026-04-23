from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    PRIORIDADES = [
        ('BAJ', 'Baja'),
        ('MED', 'Media'),
        ('ALT', 'Alta'),
        ('CRI', 'Critica'),
    ]
    ESTADOS = [
        ('ABI', 'Abierto'),
        ('PRO', 'En Proceso'),
        ('RES', 'Resuelto'),
        ('CER', 'Cerrado'),
    ]
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_solicitados')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=3, choices=PRIORIDADES, default='MED')
    estado = models.CharField(max_length=3, choices=ESTADOS, default='ABI')
    tecnico_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.titulo}"

    class Meta:
        permissions = [
            ("puede_gestionar_soporte", "Puede gestionar tickets de soporte"),
        ]
