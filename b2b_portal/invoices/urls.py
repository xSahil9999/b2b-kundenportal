from django.urls import path

from . import views


app_name = "invoices"

urlpatterns = [
    path("", views.invoice_list, name="list"),
    path("<int:pk>/", views.invoice_detail, name="detail"),
    path("upload/", views.invoice_upload, name="upload"),
]
