from django.contrib.auth.hashers import Argon2PasswordHasher
import os

class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = int(os.getenv("ARGON2_TIME_COST", 2))
    memory_cost = int(os.getenv("ARGON2_MEMORY_COST", 512))
    parallelism = int(os.getenv("ARGON2_PARALLELISM", 2))