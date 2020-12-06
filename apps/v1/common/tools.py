from shutil import move
import os

def get_user_or_none(request):
    if request.user.is_authenticated:
        return request.user
    else:
        return None

def get_object_or_none(model, *args, **kwargs):
    try:
        object = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    return object

def capitalize(text):
    return ' '.join([word[0].upper() + word[1:].lower() for word in text.strip().split()])

def convert_to_camel_case(text):
    return ''.join([word[0].upper() + word[1:].lower() for word in text.strip().split('_')])