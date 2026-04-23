from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Inscripcion, CicloAcademico
from academico.models import ExpedienteEstudiante, Materia

@login_required
def lista_inscripciones(request):
    # Admin ve todas, usuario ve solo las propias
    if request.user.has_perm('registro.puede_gestionar_registro') or request.user.is_superuser:
        inscripciones = Inscripcion.objects.all().order_by('-fecha_inscripcion')
    else:
        try:
            expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
            inscripciones = Inscripcion.objects.filter(estudiante=expediente).order_by('-fecha_inscripcion')
        except ExpedienteEstudiante.DoesNotExist:
            inscripciones = Inscripcion.objects.none()
    return render(request, 'registro/lista_inscripciones.html', {'inscripciones': inscripciones})

@login_required
def crear_inscripcion(request):
    try:
        expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
    except ExpedienteEstudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes un expediente académico registrado.")
    
    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        ciclo_id = request.POST.get('ciclo')
        materia = get_object_or_404(Materia, id=materia_id)
        ciclo = get_object_or_404(CicloAcademico, id=ciclo_id)
        Inscripcion.objects.create(
            estudiante=expediente,
            materia=materia,
            ciclo=ciclo,
        )
        return redirect('lista_inscripciones')
    
    materias = Materia.objects.all()
    ciclos = CicloAcademico.objects.filter(activo=True)
    return render(request, 'registro/crear_inscripcion.html', {'materias': materias, 'ciclos': ciclos})

@login_required
def detalle_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    # Solo el alumno propietario o admin
    if not request.user.is_superuser:
        try:
            expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
            if inscripcion.estudiante != expediente:
                return HttpResponseForbidden("No tienes permiso para ver esta inscripción.")
        except ExpedienteEstudiante.DoesNotExist:
            return HttpResponseForbidden("No tienes permiso para ver esta inscripción.")
    return render(request, 'registro/detalle_inscripcion.html', {'inscripcion': inscripcion})

@login_required
def eliminar_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    # Solo el alumno propietario o admin
    if not request.user.is_superuser:
        try:
            expediente = ExpedienteEstudiante.objects.get(usuario=request.user)
            if inscripcion.estudiante != expediente:
                return HttpResponseForbidden("No tienes permiso para eliminar esta inscripción.")
        except ExpedienteEstudiante.DoesNotExist:
            return HttpResponseForbidden("No tienes permiso para eliminar esta inscripción.")
    
    if request.method == 'POST':
        inscripcion.delete()
        return redirect('lista_inscripciones')
    return render(request, 'registro/eliminar_inscripcion.html', {'inscripcion': inscripcion})

@login_required
@permission_required('registro.puede_gestionar_registro', raise_exception=True)
def lista_ciclos(request):
    ciclos = CicloAcademico.objects.all().order_by('-fecha_inicio')
    return render(request, 'registro/lista_ciclos.html', {'ciclos': ciclos})

@login_required
@permission_required('registro.puede_gestionar_registro', raise_exception=True)
def crear_ciclo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        activo = request.POST.get('activo') == 'on'
        CicloAcademico.objects.create(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            activo=activo,
        )
        return redirect('lista_ciclos')
    return render(request, 'registro/crear_ciclo.html')
