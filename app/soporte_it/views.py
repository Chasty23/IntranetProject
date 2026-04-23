from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketForm, TicketGestionForm
from .models import Ticket


def puede_ver_ticket(usuario, ticket):
    return (
        usuario.is_superuser
        or usuario.has_perm('soporte_it.puede_gestionar_tickets')
        or ticket.solicitante == usuario
        or ticket.tecnico_asignado == usuario
    )


def puede_gestionar_ticket(usuario, ticket):
    return (
        usuario.is_superuser
        or usuario.has_perm('soporte_it.puede_gestionar_tickets')
        or (
            usuario.has_perm('soporte_it.puede_atender_tickets')
            and ticket.tecnico_asignado == usuario
        )
    )



@permission_required('soporte_it.view_ticket', raise_exception=True)
def lista_tickets(request):
    if request.user.is_superuser or request.user.has_perm(
        'soporte_it.puede_gestionar_tickets'
    ):
        tickets = Ticket.objects.select_related(
            'solicitante', 'tecnico_asignado'
        ).all()
    elif request.user.has_perm('soporte_it.puede_atender_tickets'):
        tickets = Ticket.objects.select_related(
            'solicitante', 'tecnico_asignado'
        ).filter(tecnico_asignado=request.user)
    else:
        tickets = Ticket.objects.select_related(
            'solicitante', 'tecnico_asignado'
        ).filter(solicitante=request.user)

    return render(request, 'soporte_it/lista_tickets.html', {'tickets': tickets})


@login_required
@permission_required('soporte_it.add_ticket', raise_exception=True)
def crear_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.solicitante = request.user
            ticket.save()
            return redirect('lista_tickets_soporte')
    else:
        form = TicketForm()

    return render(
        request,
        'soporte_it/form_ticket.html',
        {'form': form, 'titulo_pagina': 'Crear ticket'},
    )


@permission_required('soporte_it.view_ticket', raise_exception=True)
def detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket.objects.select_related('solicitante', 'tecnico_asignado'),
        id=ticket_id,
    )
    if not puede_ver_ticket(request.user, ticket):
        return HttpResponseForbidden('No tienes acceso a este ticket.')

    return render(
        request,
        'soporte_it/detalle_ticket.html',
        {'ticket': ticket},
    )


@login_required
@permission_required('soporte_it.change_ticket', raise_exception=True)
def editar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    puede_editar = (
        request.user.is_superuser
        or request.user.has_perm('soporte_it.puede_gestionar_tickets')
        or ticket.solicitante == request.user
    )
    if not puede_editar:
        return HttpResponseForbidden('No puedes editar este ticket.')

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('detalle_ticket_soporte', ticket_id=ticket.id)
    else:
        form = TicketForm(instance=ticket)

    return render(
        request,
        'soporte_it/form_ticket.html',
        {'form': form, 'titulo_pagina': 'Editar ticket', 'ticket': ticket},
    )


@login_required
@permission_required('soporte_it.change_ticket', raise_exception=True)
def gestionar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not puede_gestionar_ticket(request.user, ticket):
        return HttpResponseForbidden('No puedes gestionar este ticket.')

    if request.method == 'POST':
        form = TicketGestionForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            if (
                request.user.has_perm('soporte_it.puede_atender_tickets')
                and not request.user.has_perm('soporte_it.puede_gestionar_tickets')
                and not request.user.is_superuser
            ):
                ticket.tecnico_asignado = request.user
            ticket.save()
            return redirect('detalle_ticket_soporte', ticket_id=ticket.id)
    else:
        form = TicketGestionForm(instance=ticket)
        if (
            request.user.has_perm('soporte_it.puede_atender_tickets')
            and not request.user.has_perm('soporte_it.puede_gestionar_tickets')
            and not request.user.is_superuser
        ):
            form.fields['tecnico_asignado'].disabled = True

    return render(
        request,
        'soporte_it/gestionar_ticket.html',
        {'form': form, 'ticket': ticket},
    )


@login_required
@permission_required('soporte_it.delete_ticket', raise_exception=True)
def eliminar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    puede_eliminar = (
        request.user.is_superuser
        or request.user.has_perm('soporte_it.puede_gestionar_tickets')
        or ticket.solicitante == request.user
    )
    if not puede_eliminar:
        return HttpResponseForbidden('No puedes eliminar este ticket.')

    if request.method == 'POST':
        ticket.delete()
        return redirect('lista_tickets_soporte')

    return render(
        request,
        'soporte_it/eliminar_ticket.html',
        {'ticket': ticket},
    )

