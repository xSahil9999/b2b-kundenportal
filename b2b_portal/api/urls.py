from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import InvoiceViewSet, TicketViewSet, UserViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("token/", obtain_auth_token, name="api-token"),
    path("", include(router.urls)),
]

