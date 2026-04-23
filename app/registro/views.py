from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from academico.models import ExpedienteEstudiante

from .forms import CicloAcademicoForm, InscripcionForm, InscripcionGestionForm
from .models import CicloAcademico, Inscripcion


def puede_ver_inscripcion(usuario, inscripcion):
    return (
        usuario.is_superuser
        or usuario.has_perm('registro.puede_gestionar_registro')
        or inscripcion.expediente.usuario == usuario
    )



@permission_required('registro.view_inscripcion', raise_exception=True)
def lista_inscripciones(request):
    if request.user.is_superuser or request.user.has_perm(
        'registro.puede_gestionar_registro'
    ):
        inscripciones = Inscripcion.objects.select_related(
            'expediente__usuario', 'materia', 'ciclo'
        ).all()
    else:
        inscripciones = Inscripcion.objects.select_related(
            'expediente__usuario', 'materia', 'ciclo'
        ).filter(expediente__usuario=request.user)

    ciclos = CicloAcademico.objects.all()
    return render(
        request,
        'registro/lista_inscripciones.html',
        {'inscripciones': inscripciones, 'ciclos': ciclos},
    )


@login_required
@permission_required('registro.add_inscripcion', raise_exception=True)
def crear_inscripcion(request):
    if request.user.is_superuser or request.user.has_perm(
        'registro.puede_gestionar_registro'
    ):
        form_class = InscripcionGestionForm
        expediente = None
    else:
        expediente = ExpedienteEstudiante.objects.filter(usuario=request.user).first()
        if expediente is None:
            messages.error(
                request,
                'Tu usuario no tiene expediente academico vinculado.',
            )
            return redirect('lista_inscripciones_registro')
        form_class = InscripcionForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            if expediente is not None:
                inscripcion.expediente = expediente
            inscripcion.save()
            return redirect('lista_inscripciones_registro')
    else:
        form = form_class()

    return render(
        request,
        'registro/form_inscripcion.html',
        {'form': form},
    )


@login_required
@permission_required('registro.view_inscripcion', raise_exception=True)
def detalle_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(
        Inscripcion.objects.select_related('expediente__usuario', 'materia', 'ciclo'),
        id=inscripcion_id,
    )
    if not puede_ver_inscripcion(request.user, inscripcion):
        return HttpResponseForbidden('No tienes acceso a esta inscripcion.')

    return render(
        request,
        'registro/detalle_inscripcion.html',
        {'inscripcion': inscripcion},
    )


@login_required
@permission_required('registro.delete_inscripcion', raise_exception=True)
def eliminar_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    puede_eliminar = (
        request.user.is_superuser
        or request.user.has_perm('registro.puede_gestionar_registro')
        or inscripcion.expediente.usuario == request.user
    )
    if not puede_eliminar:
        return HttpResponseForbidden('No puedes eliminar esta inscripcion.')

    if request.method == 'POST':
        inscripcion.delete()
        return redirect('lista_inscripciones_registro')

    return render(
        request,
        'registro/eliminar_inscripcion.html',
        {'inscripcion': inscripcion},
    )


@login_required
@permission_required('registro.puede_gestionar_registro', raise_exception=True)
def lista_ciclos(request):
    ciclos = CicloAcademico.objects.all()
    return render(request, 'registro/lista_ciclos.html', {'ciclos': ciclos})


@login_required
@permission_required('registro.puede_gestionar_registro', raise_exception=True)
def crear_ciclo(request):
    if request.method == 'POST':
        form = CicloAcademicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ciclos_registro')
    else:
        form = CicloAcademicoForm()

    return render(request, 'registro/form_ciclo.html', {'form': form})

