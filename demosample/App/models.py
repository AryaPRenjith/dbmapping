from django.utils import timezone

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from .middleware import *
from django.contrib.auth import get_user






class Role(models.Model):

    role_name = models.CharField(max_length=45)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='rolecreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='role_update')
    privileges = models.ManyToManyField('Privilege', related_name='userroles')
    active = models.BooleanField(null=True)

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()

        super(Role, self).save(*args, **kwargs)


class Privilege(models.Model):

    privilege_key = models.CharField(max_length=45)
    privilege_group_name = models.CharField(max_length=45)
    privilege_name = models.CharField(max_length=45)
    privilege_description = models.CharField(max_length=45)
    active = models.BooleanField(null=True)


class RolePrivilegeChange(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)

    added = models.BooleanField(default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='privilege-change+',
                                    on_delete=models.SET_NULL, null=True)

    modified_at = models.DateTimeField(auto_now=True)



class IPA(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='ipacreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='ipaupdate')
    active = models.BooleanField()
    practices = models.ManyToManyField('Practice', related_name='roles')

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()

        super(IPA, self).save(*args, **kwargs)

class Practice(models.Model):

    tin = models.CharField(max_length=45, default='1234')
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='practicecreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='practiceupdate')

    active = models.BooleanField()

    def __str__(self):
        # return self.name
        return f"{self.tin} | {self.name}"


    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()

        super(Practice, self).save(*args, **kwargs)


class IpaPracticeChange(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ipa = models.ForeignKey(IPA, on_delete=models.CASCADE)

    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    added = models.BooleanField(default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='practice-change+',
                                    on_delete=models.SET_NULL, null=True)

    modified_at = models.DateTimeField(auto_now=True)





class Optimussignal(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='optimussignalcreate')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='optimussignalupdate')

    # role = models.ForeignKey(Role, on_delete=models.CASCADE,related_name='optimusrole')



def get_current_user():
    return get_user(thread_locals.request)



