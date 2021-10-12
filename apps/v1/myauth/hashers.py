from django.contrib.auth.hashers import Argon2PasswordHasher
import os

class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = os.getenv("ARGON2_TIME_COST", 2)
    memory_cost = os.getenv("ARGON2_MEMORY_COST", 512)
    parallelism = os.getenv("ARGON2_PARALLELISM", 2)