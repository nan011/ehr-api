from django.contrib.auth.backends import BaseBackend

from apps.v1.common.tools import get_object_or_none
from .models import Account

class CustomUserAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, role=None):
        account = get_object_or_none(Account, email = email)
        if account is not None:
            if not account.check_password(password) or not account.is_active:
                return None
        return account