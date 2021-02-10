AWS_STORAGE_BUCKET_NAME = 'animal-aid-local'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_LOCATION = 'static'
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'AnimalAid.settings.aws.storage_backends.MediaStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'