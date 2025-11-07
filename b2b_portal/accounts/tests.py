from django.test import TestCase
from django.contrib.auth import get_user_model

from .roles import is_role


User = get_user_model()


class RoleTests(TestCase):
    def test_is_role_helper(self):
        admin = User.objects.create_user(username="admin", password="x", role="admin")
        cust = User.objects.create_user(username="cust", password="x", role="customer")
        self.assertTrue(is_role(admin, "admin"))
        self.assertFalse(is_role(cust, "admin"))

