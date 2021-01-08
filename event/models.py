import uuid as uuid
from django.db import models

from user.models import User


class Event(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    formFields = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'event'
        verbose_name_plural = "Events"
        verbose_name = "Event"

    def __str__(self):
        return self.title


class Participant(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    formData = models.JSONField(null=True, blank=True)
    timestampRegistered = models.DateTimeField(auto_now=True)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='approver', null=True, blank=True)
    timestampApproved = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=255)

    class Meta:
        unique_together = [
            ('user', 'event')
        ]
        db_table = 'participant'
        verbose_name_plural = "Event Participants"
        verbose_name = "Event Participant"

    def __str__(self):
        return str(self.uuid)


class EventManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    canViewRegistrations = models.BooleanField(default=True)
    canReviewRegistrations = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ('user', 'event')
        ]
        db_table = 'manager'
        verbose_name_plural = "Event Managers"
        verbose_name = "Event Manager"

    def __str__(self):
        return self.user.username + ' ' + self.event.title


__all__ = [
    'Event',
    'Participant',
    'EventManager'
]
