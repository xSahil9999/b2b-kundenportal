from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Ticket


User = get_user_model()


class TicketVisibilityTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pw", role="admin")
        self.cust1 = User.objects.create_user(username="c1", password="pw", role="customer")
        self.cust2 = User.objects.create_user(username="c2", password="pw", role="customer")
        Ticket.objects.create(title="T1", description="d", customer=self.cust1)
        Ticket.objects.create(title="T2", description="d", customer=self.cust2)

    def test_customer_sees_only_own_tickets(self):
        self.client.login(username="c1", password="pw")
        resp = self.client.get(reverse("tickets:list"))
        self.assertContains(resp, "T1")
        self.assertNotContains(resp, "T2")

    def test_admin_sees_all_tickets(self):
        self.client.login(username="admin", password="pw")
        resp = self.client.get(reverse("tickets:list"))
        self.assertContains(resp, "T1")
        self.assertContains(resp, "T2")

