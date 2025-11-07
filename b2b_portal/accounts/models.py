from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Kunde"
        SUPPORT = "support", "Support"

    role = models.CharField(
        "Rolle",
        max_length=20,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
        help_text="Rolle des Benutzers für Berechtigungen",
    )

    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_customer(self):
        return self.role == self.Roles.CUSTOMER

    def is_support(self):
        return self.role == self.Roles.SUPPORT

    class Meta:
        verbose_name = "Benutzer"
        verbose_name_plural = "Benutzer"
