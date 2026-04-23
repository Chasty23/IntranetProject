from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Ticket

@login_required
def lista_tickets(request):
    # Si tiene permiso de gestion (IT/Admin) ve todos, si no solo los suyos
    if request.user.has_perm('soporte_it.puede_gestionar_soporte') or request.user.is_superuser:
        tickets = Ticket.objects.all().order_by('-fecha_creacion')
    else:
        tickets = Ticket.objects.filter(solicitante=request.user).order_by('-fecha_creacion')
    return render(request, 'soporte_it/lista_tickets.html', {'tickets': tickets})

@login_required
def crear_ticket(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        prioridad = request.POST.get('prioridad', 'MED')
        Ticket.objects.create(
            solicitante=request.user,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
        )
        return redirect('lista_tickets')
    return render(request, 'soporte_it/crear_ticket.html')

@login_required
def detalle_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # Solo el solicitante, el tecnico asignado o admin pueden ver
    if ticket.solicitante != request.user and ticket.tecnico_asignado != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para ver este ticket.")
    return render(request, 'soporte_it/detalle_ticket.html', {'ticket': ticket})

@login_required
def editar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # Solo el solicitante o admin pueden editar
    if ticket.solicitante != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para editar este ticket.")
    if request.method == 'POST':
        ticket.titulo = request.POST.get('titulo')
        ticket.descripcion = request.POST.get('descripcion')
        ticket.prioridad = request.POST.get('prioridad')
        ticket.save()
        return redirect('detalle_ticket', id=ticket.id)
    return render(request, 'soporte_it/editar_ticket.html', {'ticket': ticket})

@login_required
def gestionar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # Solo IT (con permiso) o admin
    if not request.user.has_perm('soporte_it.puede_gestionar_soporte') and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para gestionar este ticket.")
    if request.method == 'POST':
        ticket.estado = request.POST.get('estado')
        tecnico_id = request.POST.get('tecnico_asignado')
        if tecnico_id:
            from django.contrib.auth.models import User
            ticket.tecnico_asignado = User.objects.get(id=tecnico_id)
        else:
            ticket.tecnico_asignado = None
        ticket.save()
        return redirect('detalle_ticket', id=ticket.id)
    from django.contrib.auth.models import User
    tecnicos = User.objects.filter(is_staff=True)
    return render(request, 'soporte_it/gestionar_ticket.html', {'ticket': ticket, 'tecnicos': tecnicos})

@login_required
def eliminar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # Solo el solicitante o admin
    if ticket.solicitante != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para eliminar este ticket.")
    if request.method == 'POST':
        ticket.delete()
        return redirect('lista_tickets')
    return render(request, 'soporte_it/eliminar_ticket.html', {'ticket': ticket})
