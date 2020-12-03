from django.contrib.auth.hashers import Argon2PasswordHasher
import os

class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = os.getenv("TIME_COST", 2)
    memory_cost = os.getenv("MEMORY_COST", 512)
    parallelism = os.getenv("PARALLELISM", 2)