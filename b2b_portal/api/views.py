from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from invoices.models import Invoice
from tickets.models import Ticket, TicketComment
from .permissions import IsAdminOrOwner
from .serializers import (
    InvoiceSerializer,
    TicketCommentSerializer,
    TicketSerializer,
    UserSerializer,
)


User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAdminUser()]


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminOrOwner]
    filterset_fields = {
        "number": ["exact", "icontains"],
        "invoice_date": ["exact", "gte", "lte"],
        "customer": ["exact"],
        "amount": ["gte", "lte"],
    }
    search_fields = ["number"]
    ordering_fields = ["invoice_date", "created_at", "amount", "number"]

    def get_queryset(self):
        qs = Invoice.objects.all()
        user = self.request.user
        if user.is_superuser or getattr(user, "role", None) in ("admin", "support"):
            return qs
        return qs.filter(customer=user)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrOwner]
    filterset_fields = {
        "status": ["exact"],
        "customer": ["exact"],
        "created_at": ["gte", "lte"],
    }
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "status"]

    def get_queryset(self):
        qs = Ticket.objects.all()
        user = self.request.user
        if user.is_superuser or getattr(user, "role", None) in ("admin", "support"):
            return qs
        return qs.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=["post"]) 
    def comment(self, request, pk=None):
        ticket = self.get_object()
        msg = request.data.get("message")
        if not msg:
            return Response({"detail": "message ist erforderlich"}, status=400)
        TicketComment.objects.create(ticket=ticket, author=request.user, message=msg)
        return Response(TicketSerializer(ticket, context={"request": request}).data)
