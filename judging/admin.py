from django.contrib import admin
from judging.models import ParticipantJudgement


@admin.register(ParticipantJudgement)
class ParticipantJudgementAdmin(admin.ModelAdmin):
    list_display = ('participant', 'judge', 'points')
    list_filter = ('participant__event', )