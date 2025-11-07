from django import forms
from django.contrib.auth import get_user_model

from .models import Invoice


User = get_user_model()


class InvoiceUploadForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=User.objects.none())

    class Meta:
        model = Invoice
        fields = ["number", "customer", "pdf", "amount", "invoice_date"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        # Only allow admins/support to choose a customer
        if request and (request.user.is_superuser or getattr(request.user, "role", None) in ("admin", "support")):
            self.fields["customer"].queryset = User.objects.all().order_by("username")
        else:
            self.fields["customer"].queryset = User.objects.none()

    def clean_pdf(self):
        f = self.cleaned_data.get("pdf")
        if not f:
            return f
        name = getattr(f, "name", "").lower()
        content_type = getattr(f, "content_type", "application/octet-stream").lower()
        if not name.endswith(".pdf") or "pdf" not in content_type:
            raise forms.ValidationError("Nur PDF-Dateien sind erlaubt.")
        if f.size and f.size > 20 * 1024 * 1024:
            raise forms.ValidationError("Datei ist zu groß (max. 20MB).")
        return f

