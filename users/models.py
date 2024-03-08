from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Leave the standard fields
    # username = models.CharField(_("username"), max_length=150, unique=True, ...)
    # first_name = models.CharField(_("first name"), max_length=150, blank=True)
    # last_name = models.CharField(_("last name"), max_length=150, blank=True)
    # email = models.EmailField(_("email address"), blank=True)
    # date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    REQUIRED_FIELDS = []
