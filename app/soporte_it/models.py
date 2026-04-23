from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    ESTADOS = [
        ('ABI', 'Abierto'),
        ('PRO', 'En proceso'),
        ('RES', 'Resuelto'),
        ('CER', 'Cerrado'),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    estado = models.CharField(max_length=3, choices=ESTADOS, default='ABI')
    solicitante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets_creados',
    )
    tecnico_asignado = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='tickets_asignados',
        null=True,
        blank=True,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        permissions = [
            ('puede_gestionar_tickets', 'Puede gestionar todos los tickets'),
            ('puede_atender_tickets', 'Puede atender tickets asignados'),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.solicitante.username}"

