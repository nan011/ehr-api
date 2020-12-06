# Create your models here.
import binascii
import os

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from apps.v1.common.models import BaseModel

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # for field_name in list(extra_fields.keys()):
        #     setattr(user, field_name, extra_fields.pop(field_name))
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Admin
        extra_fields['role'] = 1

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = None
    username = None
    first_name = None
    last_name = None
    name = models.CharField(_('name'), max_length = 255)
    email = models.EmailField(_('email address'), unique = True, primary_key = True)

    class Role(models.IntegerChoices):
        UNKNOWN = 0, _('Unknown')
        ADMIN = 1, _('Admin')
        OPERATOR = 2, _('Operator')
        PATIENT = 3, _('Patient')
    role = models.IntegerField(choices = Role.choices, default = Role.UNKNOWN)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        User,
        related_name='auth_token',
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
