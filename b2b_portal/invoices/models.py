from django.conf import settings
from django.db import models


def invoice_upload_path(instance, filename):
    return f"invoices/{instance.customer_id}/{filename}"


class Invoice(models.Model):
    number = models.CharField("Nummer", max_length=64, unique=True)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Kunde",
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    pdf = models.FileField("PDF", upload_to=invoice_upload_path)
    amount = models.DecimalField("Betrag", max_digits=12, decimal_places=2)
    invoice_date = models.DateField("Rechnungsdatum")
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)

    class Meta:
        ordering = ["-invoice_date", "-created_at"]
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"

    def __str__(self):
        return self.number
