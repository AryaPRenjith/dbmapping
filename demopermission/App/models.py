from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    name=models.CharField(max_length=100)
    role_permissions=models.ManyToManyField("privileges",related_name='roles')

class privileges(models.Model):
    name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100)

class CustomRolePrivilege(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

