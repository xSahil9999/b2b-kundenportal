from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Invoice


User = get_user_model()


PDF_BYTES = b"%PDF-1.4 test pdf file\n%%EOF"


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class InvoiceUploadTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pw", role="admin", email="admin@example.com")
        self.cust = User.objects.create_user(username="cust", password="pw", role="customer", email="cust@example.com")

    def test_admin_can_upload_invoice(self):
        self.client.login(username="admin", password="pw")
        url = reverse("invoices:upload")
        pdf = SimpleUploadedFile("test.pdf", PDF_BYTES, content_type="application/pdf")
        data = {
            "number": "R-1001",
            "customer": self.cust.id,
            "amount": "123.45",
            "invoice_date": "2024-01-01",
            "pdf": pdf,
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Invoice.objects.filter(number="R-1001", customer=self.cust).exists())

    def test_customer_cannot_access_upload(self):
        self.client.login(username="cust", password="pw")
        url = reverse("invoices:upload")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

