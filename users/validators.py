from django.contrib import messages
from django.shortcuts import redirect

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.jpeg', '.png', '.txt', '.doc', '.docx', '.jpg']
    print(ext)
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')