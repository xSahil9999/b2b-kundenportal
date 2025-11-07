from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Ticket, TicketComment


@login_required
def ticket_list(request):
    qs = Ticket.objects.all()
    if not request.user.is_superuser and getattr(request.user, "role", None) != "admin":
        qs = qs.filter(customer=request.user)
    return render(request, "tickets/list.html", {"tickets": qs})


@login_required
@require_http_methods(["GET", "POST"])
def ticket_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title and description:
            t = Ticket.objects.create(title=title, description=description, customer=request.user)
            return redirect("tickets:detail", pk=t.pk)
    return render(request, "tickets/create.html")


@login_required
@require_http_methods(["GET", "POST"])
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not request.user.is_superuser and getattr(request.user, "role", None) != "admin":
        if ticket.customer_id != request.user.id and getattr(request.user, "role", None) != "support":
            from django.http import HttpResponseForbidden

            return HttpResponseForbidden("Keine Berechtigung")
    if request.method == "POST":
        msg = request.POST.get("message")
        if msg:
            TicketComment.objects.create(ticket=ticket, author=request.user, message=msg)
    return render(request, "tickets/detail.html", {"ticket": ticket})

