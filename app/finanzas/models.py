from django.db import models
from django.contrib.auth.models import User

class Pago(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('PAG', 'Pagado'),
        ('MOR', 'Mora'),
    ]
    # Relacionamos con el usuario para saber de quien es el pago
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=200) # Ej: Matricula Ciclo 01-2026
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')

    def __str__(self):
        return f"{self.usuario.username} - {self.concepto} (${self.monto})"
    # permisos para gestionar pagos
    class Meta:
        permissions = [
            ("puede_gestionar_pagos", "Puede registrar y editar pagos"),
        ]
