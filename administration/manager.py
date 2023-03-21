from django.db import models
from django.db.models import Model, Manager
from main.models import models
from django.db.models.functions import Now


class ticketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ticket_expire_date__gt=Now())
