# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Ticket

@receiver(pre_save, sender=User)
def email_address_update(sender, instance, **kwargs):
    qs = User.objects.filter(id=instance.id)
    if not qs:
        return

    pre_save_user = qs.first()
    tickets = Ticket.objects.filter(submitter_email=pre_save_user.email)
    for ticket in tickets:
        ticket.submitter_email = instance.email
        ticket.save()
