# Create your models here.
import binascii
import os
import uuid

from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.dispatch import receiver

from apps.v1.common.models import BaseModel

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_raw(self, email, password, **extra_fields):
        """
        Create and save a Account with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        extra_fields.setdefault('is_active', False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        return user

    def create(self, **extra_fields):
        user = self.create_raw(**extra_fields)
        user.save()
        return user

class Account(AbstractBaseUser):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
    )
    created_at = models.DateTimeField(
        verbose_name = "Created at",
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = "Updated at",
        auto_now = True,
    )
    is_active = models.BooleanField(default = False)

    name = models.CharField(_('name'), max_length = 255)
    email = models.EmailField(_('email address'))
    class Role(models.IntegerChoices):
        UNKNOWN = 0, _('Unknown')
        ADMIN = 1, _('Admin')
        OPERATOR = 2, _('Operator')
        PATIENT = 3, _('Patient')
    role = models.IntegerField(choices = Role.choices, default=Role.UNKNOWN)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    class Meta:
        unique_together = (('email', 'role'),)

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Admin(BaseModel):
    id = None
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)

@receiver(models.signals.pre_save, sender=Admin)
def set_role(sender, instance, *args, **kwargs):
    instance.account.role = Account.Role.ADMIN
    instance.account.save()
    return instance


@receiver(models.signals.post_delete, sender=Admin)
def remove_account(sender, instance, *args, **kwargs):
    if instance != None:
        instance.account.delete()

class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    created_at = models.DateTimeField(
        verbose_name = "Created at",
        auto_now_add = True,
    )
    user = models.OneToOneField(
        Account,
        related_name='token',
        on_delete=models.CASCADE,
        verbose_name=_("Account"),
    )

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
