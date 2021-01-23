from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


EVENT_TYPE_CHOICES = (
    (0, 'Fest'),
    (1, 'Competition'),
    (2, 'Workshop')
)

USER_TYPE_CHOICES = (
    (0, 'Admin'),
    (1, 'Student'),
    (2, 'Academician'),
    (3, 'Industry'),
    (4, 'Judge')
)


__all__ = [
    'USER_TYPE_CHOICES',
    'StaticStorage'
]
