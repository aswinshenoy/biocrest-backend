import graphene
from chowkidar.graphql.decorators import resolve_user
from chowkidar.graphql.exceptions import APIException
from django.core.files.base import ContentFile
from django.db.models import Q

from certificate.models import EventCertificate, GeneratedCertificate
from event.models import Participant


class GeneratedCertificateFile(graphene.ObjectType):
    file = graphene.String()


class GenerateParticipationCertificate(graphene.Mutation):
    class Arguments:
       eventID = graphene.ID(required=True)

    Output = GeneratedCertificateFile

    @resolve_user
    def mutate(self, info, eventID: graphene.ID) -> GeneratedCertificateFile:
        userID = info.context.userID
        user = info.context.user
        try:
            participant = Participant.objects.get(
                Q(event_id=eventID) &
                Q(Q(user_id=userID) | Q(team__members=userID))
            )
        except Participant.DoesNotExist:
            raise APIException('Participant does not ', code='PARTICIPANT_NOT_FOUND')

        try:
            eventCert = EventCertificate.objects.get(
                event_id=eventID,
                isReleased=True
            )
        except EventCertificate.DoesNotExist:
            raise APIException('Certificate not available', code='NOT_AVAILABLE')


        try:
            generatedCert = GeneratedCertificate.objects.get(
                event_id=eventID, user_id=userID, participant_id=participant.id, type=0
            )
            if generatedCert.generations > 1:
                raise APIException('Maximum generations exceeded', code='CANNOT_GENERATE')
        except GeneratedCertificate.DoesNotExist:
            generatedCert = GeneratedCertificate(
                event_id=eventID,
                user_id=userID,
                participant_id=participant.id,
                type=0,
                generations=1
            )

        name = user.title + ' ' + user.name
        from PIL import Image, ImageDraw, ImageFont
        from requests import get
        from io import BytesIO

        im = Image.open(eventCert.template)
        d = ImageDraw.Draw(im)

        location = (eventCert.namePositionX, eventCert.namePositionY)

        if eventCert.nameFontURL is not None and len(eventCert.nameFontURL) > 5:
            fontURL = eventCert.nameFontURL
        else:
            fontName = eventCert.nameFontName if eventCert.nameFontName else 'Roboto-Regular'
            fontURL = 'https://github.com/googlefonts/roboto/blob/master/src/hinted/' + fontName + '.ttf?raw=true'

        req = get(fontURL)

        font = ImageFont.truetype(BytesIO(req.content),  size=eventCert.nameFontSize)
        d.text(location, name, fill=eventCert.nameFontColor, font=font)

        outputFile = BytesIO()
        im.save(outputFile, format='PDF')
        file = ContentFile(
            outputFile.getvalue(),
            'certificate.pdf'
        )

        generatedCert.file = file
        generatedCert.save()
        return GeneratedCertificateFile(
            file=generatedCert.file.url
        )


class CertificateMutations(graphene.ObjectType):
    generateParticipationCertificate = GenerateParticipationCertificate.Field()


__all__ = [
    'CertificateMutations'
]
