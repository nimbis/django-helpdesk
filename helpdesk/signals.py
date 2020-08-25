# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Ticket

@receiver(pre_save, sender=User)
def update_ticket_submitter_email(sender, instance, **kwargs):
    pre_save_user = User.objects.filter(id=instance.id).first()

    # If the user doesn't exist yet, then they won't have any tickets
    if not pre_save_user:
        return

    # Make sure the email address actually changed
    if pre_save_user.email == instance.email:
        return

    tickets = Ticket.objects.filter(submitter_email=pre_save_user.email)
    for ticket in tickets:
        ticket.submitter_email = instance.email
        ticket.save()
