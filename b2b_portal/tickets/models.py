from django.conf import settings
from django.db import models


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Offen"
        IN_PROGRESS = "in_progress", "In Bearbeitung"
        CLOSED = "closed", "Geschlossen"

    title = models.CharField("Titel", max_length=200)
    description = models.TextField("Beschreibung")
    status = models.CharField("Status", max_length=20, choices=Status.choices, default=Status.OPEN)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Kunde", related_name="tickets", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Zugewiesen an",
        related_name="assigned_tickets",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Aktualisiert am", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"#{self.pk} {self.title}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name="Ticket", related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Autor", on_delete=models.CASCADE)
    message = models.TextField("Nachricht")
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Ticket-Kommentar"
        verbose_name_plural = "Ticket-Kommentare"

    def __str__(self):
        return f"Kommentar von {self.author}"
