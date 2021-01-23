import uuid as uuid
from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField

from framework.utils import USER_TYPE_CHOICES, EVENT_TYPE_CHOICES
from user.fields import MediaField
from user.media import EventStorage, SubmissionStorage
from user.models import User, Team


class Event(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=EVENT_TYPE_CHOICES, default=0, blank=True)

    cover = MediaField(
        storage=EventStorage(),
        max_size=1024 * 1024 * 8,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
        ],
        null=True, blank=True
    )
    poster = MediaField(
        storage=EventStorage(),
        max_size=1024 * 1024 * 8,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
        ],
        null=True, blank=True
    )
    shortDescription = models.CharField(max_length=100, default='', blank=True)
    details = models.TextField(default='', blank=True)

    isTeamEvent = models.BooleanField(default=False)
    minTeamSize = models.PositiveSmallIntegerField(null=True, blank=True)
    maxTeamSize = models.PositiveSmallIntegerField(null=True, blank=True)

    acceptRegistrations = models.BooleanField(default=True)
    registrationCloseTimestamp = models.DateTimeField(null=True, blank=True)
    allowedUserTypes = MultiSelectField(choices=USER_TYPE_CHOICES, max_choices=10, max_length=255, null=True, blank=True)

    formFields = models.JSONField(null=True, blank=True)
    requireApproval = models.BooleanField(default=False)
    postApprovalFields = models.JSONField(null=True, blank=True)

    def _generate_slug(self):
        self.slug = slugify(self.name, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.pk or self.slug == '' or self.slug is None:
            self._generate_slug()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [
            ['slug', 'parent']
        ]
        db_table = 'event'
        verbose_name_plural = "Events"
        verbose_name = "Event"

    def __str__(self):
        return self.name


class Participant(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)

    formData = models.JSONField(null=True, blank=True)
    postApprovalData = models.JSONField(null=True, blank=True)
    timestampRegistered = models.DateTimeField(auto_now=True)

    approver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='approver', null=True, blank=True)
    timestampApproved = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        unique_together = [
            ('user', 'event')
        ]
        db_table = 'participant'
        verbose_name_plural = "Event Participants"
        verbose_name = "Event Participant"

    def __str__(self):
        return str(self.id)


class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = (
        (1, 'Image'),
        (2, 'PDF'),
        (3, 'PPT'),
        (4, 'Youtube URL'),
    )
    file = MediaField(
        storage=SubmissionStorage(),
        max_size=1024 * 1024 * 12,
        null=True, blank=True
    )
    url = models.URLField(null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=SUBMISSION_TYPE_CHOICES, default=1)
    timestamp = models.DateTimeField(auto_now=True)
    isPublic = models.BooleanField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, default='', blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'submission'
        verbose_name_plural = "Event Submissions"
        verbose_name = "Event Submission"

    def __str__(self):
        return str(self.id)


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
        return self.user.username + ' ' + self.event.name


__all__ = [
    'Event',
    'Participant',
    'Submission',
    'EventManager'
]
