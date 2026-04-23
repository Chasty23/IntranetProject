# config/nav.py
from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem


class MainNav(Nav):
    template_name = "main_nav.html"
    items = [
        NavItem(title="Home", url="/"),
        NavItem(title="Academico", url="/academico/notas/"),
        NavItem(title="RRHH", url="/rrhh/personal/"),
        NavItem(title="Finanzas", url="/finanzas/estado-cuenta/"),
        NavItem(title="Soporte IT", url="/soporte-it/tickets/"),
        NavItem(title="Registro", url="/registro/inscripciones/"),
        NavItem(title="Biblioteca", url="/biblioteca/libros/"),
    ]
