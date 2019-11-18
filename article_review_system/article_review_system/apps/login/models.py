from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """定义用户模型类"""
    def __str__(self):
        return self.username