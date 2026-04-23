from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Empleado

@login_required
@permission_required('rrhh.view_empleado', raise_exception=True)
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'rrhh/lista.html', {'empleados': empleados})

@permission_required('rrhh.puede_gestionar_rrhh', raise_exception=True)
def detalle_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    return render(request, 'rrhh/detalle.html', {'empleado': empleado})