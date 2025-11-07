from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from invoices.models import Invoice
from tickets.models import Ticket


@login_required
def home(request):
    stats = {}
    if request.user.is_superuser or getattr(request.user, "role", None) == "admin":
        stats = {
            "invoice_count": Invoice.objects.count(),
            "open_tickets": Ticket.objects.filter(status=Ticket.Status.OPEN).count(),
            "in_progress_tickets": Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).count(),
        }
        tmpl = "dashboard/admin_dashboard.html"
    else:
        stats = {
            "my_invoices": Invoice.objects.filter(customer=request.user).count(),
            "my_open_tickets": Ticket.objects.filter(customer=request.user, status=Ticket.Status.OPEN).count(),
        }
        tmpl = "dashboard/customer_dashboard.html"
    return render(request, tmpl, {"stats": stats})

