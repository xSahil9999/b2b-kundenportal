from django.contrib import admin

from .models import Invoice
from .tasks import send_invoice_email


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "amount", "invoice_date", "created_at")
    search_fields = ("number", "customer__username", "customer__email")
    list_filter = ("invoice_date",)
    actions = ["send_invoice_notification"]

    @admin.action(description="E-Mail Benachrichtigung senden")
    def send_invoice_notification(self, request, queryset):
        for inv in queryset:
            send_invoice_email.delay(inv.id)
        self.message_user(request, f"E-Mail Versand für {queryset.count()} Rechnung(en) ausgelöst.")
