from django.core.exceptions import ValidationError
import os

def form_validation_error(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png','.jpg','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.Allowed extensions: '+str(valid_extensions))