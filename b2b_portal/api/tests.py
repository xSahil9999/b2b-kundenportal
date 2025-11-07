from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from invoices.models import Invoice


User = get_user_model()


class ApiPaginationFilterTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pw", role="admin")
        self.cust = User.objects.create_user(username="cust", password="pw", role="customer")
        for i in range(30):
            Invoice.objects.create(number=f"R-{i}", customer=self.cust, amount=10 + i, invoice_date="2024-01-01")

    def test_invoices_pagination(self):
        client = APIClient()
        client.login(username="cust", password="pw")
        resp = client.get(reverse("invoice-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("results", resp.data)
        self.assertLessEqual(len(resp.data["results"]), 20)

    def test_filter_invoice_number(self):
        client = APIClient()
        client.login(username="cust", password="pw")
        resp = client.get(reverse("invoice-list"), {"number__icontains": "R-2"})
        self.assertEqual(resp.status_code, 200)
        # Should return invoices with 'R-2' in number
        self.assertTrue(all("R-2" in x["number"] for x in resp.data["results"]))

