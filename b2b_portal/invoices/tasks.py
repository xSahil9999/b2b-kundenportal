from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Invoice


@shared_task
def send_invoice_email(invoice_id: int) -> dict:
    try:
        inv = Invoice.objects.select_related("customer").get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return {"status": "not_found", "invoice_id": invoice_id}

    subject = f"Neue Rechnung {inv.number}"
    recipient = [inv.customer.email] if inv.customer.email else []
    if not recipient:
        return {"status": "no_email", "invoice_id": invoice_id}

    base_url = getattr(settings, "SITE_URL", "")
    pdf_url = inv.pdf.url if getattr(inv, "pdf", None) else ""
    absolute_pdf_url = f"{base_url}{pdf_url}" if base_url and pdf_url and pdf_url.startswith("/") else (pdf_url or "")

    context = {
        "invoice": inv,
        "pdf_url": absolute_pdf_url,
        "site_url": base_url,
    }
    html_content = render_to_string("emails/invoice_notification.html", context)
    text_content = f"Ihre Rechnung {inv.number} ist verfügbar. Betrag: {inv.amount}. Link: {absolute_pdf_url}"

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return {"status": "sent", "invoice_id": invoice_id}
