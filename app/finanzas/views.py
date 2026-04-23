from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Pago

@login_required
@permission_required('finanzas.puede_gestionar_pagos', raise_exception=True)
def estado_cuenta(request):
    # Si es admin o tiene permiso de gestion ve todos los registros. 
    # Si es alumno, solo ve los suyos.
    if request.user.has_perm('finanzas.puede_gestionar_pagos'):
        pagos = Pago.objects.all()
    else:
        pagos = Pago.objects.filter(usuario=request.user)
    
    return render(request, 'finanzas/estado_cuenta.html', {'pagos': pagos})