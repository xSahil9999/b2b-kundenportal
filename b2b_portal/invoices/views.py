from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Invoice
from .forms import InvoiceUploadForm
from accounts.roles import role_required


@login_required
def invoice_list(request):
    qs = Invoice.objects.all()
    if not request.user.is_superuser and getattr(request.user, "role", None) != "admin":
        qs = qs.filter(customer=request.user)
    return render(request, "invoices/list.html", {"invoices": qs})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if not request.user.is_superuser and getattr(request.user, "role", None) != "admin":
        if invoice.customer_id != request.user.id:
            from django.http import HttpResponseForbidden

            return HttpResponseForbidden("Keine Berechtigung")
    return render(request, "invoices/detail.html", {"invoice": invoice})


@role_required(["admin", "support"])
@require_http_methods(["GET", "POST"])
def invoice_upload(request):
    if request.method == "POST":
        form = InvoiceUploadForm(data=request.POST, files=request.FILES, request=request)
        if form.is_valid():
            inv = form.save()
            # Trigger email via Celery
            try:
                from .tasks import send_invoice_email

                send_invoice_email.delay(inv.id)
            except Exception:
                pass
            return redirect("invoices:detail", pk=inv.pk)
    else:
        form = InvoiceUploadForm(request=request)
    return render(request, "invoices/upload.html", {"form": form})
