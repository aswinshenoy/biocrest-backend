from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'event', 'team', 'approver']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(EventManager)
class EventManagerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'event']

