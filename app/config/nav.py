# config/nav.py
from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem


class MainNav(Nav):
    template_name = "main_nav.html"
    items = [
        NavItem(title="Home", url="/"),
    ]
