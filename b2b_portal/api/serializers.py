from django.contrib.auth import get_user_model
from rest_framework import serializers

from invoices.models import Invoice
from tickets.models import Ticket, TicketComment


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]


class InvoiceSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ["id", "number", "customer", "amount", "invoice_date", "pdf", "created_at"]
        read_only_fields = ["id", "customer", "created_at"]


class TicketCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = TicketComment
        fields = ["id", "author", "message", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "status",
            "customer",
            "assigned_to",
            "created_at",
            "updated_at",
            "comments",
        ]
        read_only_fields = ["id", "customer", "assigned_to", "created_at", "updated_at", "comments"]

