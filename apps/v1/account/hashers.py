from django.contrib.auth.hashers import Argon2PasswordHasher
from django.conf import settings

class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = settings.TIME_COST
    memory_cost = settings.MEMORY_COST
    parallelism = settings.PARALLELISM