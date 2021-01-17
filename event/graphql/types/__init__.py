import graphene
import json
from django.utils import timezone

from user.graphql.types import UserProfile


class EventFormData(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()


class SelectOption(graphene.ObjectType):
    value = graphene.String()
    label = graphene.String()
    allowedUserTypes = graphene.List(graphene.Int)


class EventFieldData(graphene.ObjectType):
    type = graphene.String()
    label = graphene.String()
    key = graphene.String()
    options = graphene.List(SelectOption)
    maxSelections = graphene.Int()


class Event(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    shortDescription = graphene.String()
    details = graphene.String()
    coverURL = graphene.String()
    isTeamEvent = graphene.Boolean()
    minTeamSize = graphene.Boolean()
    maxTeamSize = graphene.Boolean()
    requireApproval = graphene.Boolean()
    formFields = graphene.List(EventFieldData)
    postApprovalFields = graphene.List(EventFieldData)
    parentEvent = graphene.Field('event.graphql.types.Event')

    def resolve_coverURL(self, info):
        if self and self.cover and hasattr(self.cover, 'url') and self.cover.url:
            return self.cover.url

    def resolve_formData(self, info):
        if self.formFields:
            try:
                return json.loads(self.formFields)
            except ValueError as e:
                pass
        return []


class Participant(graphene.ObjectType):
    uuid = graphene.String()
    id = graphene.String()
    profile = graphene.Field(UserProfile)
    formData = graphene.List(EventFormData)
    timestampRegistered = graphene.String()
    remarks = graphene.String()
    event = graphene.Field(Event)
    isApproved = graphene.Boolean()
    remarks = graphene.String()

    def resolve_profile(self, info):
        return self.user

    def resolve_timestampRegistered(self, info):
        to_tz = timezone.get_default_timezone()
        return self.timestampRegistered.astimezone(to_tz).isoformat()

    def resolve_formData(self, info):
        if self.formData:
            try:
                d = dict(json.loads(self.formData))
                data = []
                for key, value in d.items():
                    data.append({
                        "key": key,
                        "value": value
                    })
                return data
            except Exception:
                pass
        return []

    def resolve_event(self, info):
        return self.event

    def resolve_isApproved(self, info):
        return self.approver_id is not None


__all__ = [
    'EventFormData',
    'Event',
    'Participant'
]
