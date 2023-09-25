from django.utils import timezone

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_userforeignkey.models.fields import UserForeignKey




class Optimus(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = UserForeignKey(auto_user_add=True, null=True, related_name='optimus_create')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='optimus_create')
    # updated_by = UserForeignKey(auto_user_add=True, related_name='optimus_update', null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='optimus_update', null=True)
    active = models.BooleanField(null=True)
    # practices = models.ManyToManyField('Practice',related_name='optimus_practice')
    ipa = models.ManyToManyField('IPA', related_name="profiles_ipa", blank=True)

    role = models.ManyToManyField('Role', related_name="profiles_role", blank=True)

    ipa_practice = models.ManyToManyField('IpaPractice', related_name='optimus_practiceipa', through='UserIpaPractice', through_fields=('user', 'ipa_practice'))
    default_practice = models.ForeignKey('Practice', on_delete=models.SET_NULL, null=True, related_name='optimus_default_practice')


    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_do_something", "Can Do Something"),

        ]



class IPA(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='ipacreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='ipaupdate')
    active = models.BooleanField()
    practices = models.ManyToManyField('Practice', related_name='roles',through='IpaPractice')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ipa'

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()

        super(IPA, self).save(*args, **kwargs)

class Practice(models.Model):
    # ipa = models.ForeignKey(IPA, on_delete=models.CASCADE)
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

    class Meta:
        db_table = 'practice'

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()

        super(Practice, self).save(*args, **kwargs)


class IpaPractice(models.Model):
    ipa=models.ForeignKey(IPA, on_delete=models.CASCADE)
    practice=models.ForeignKey(Practice, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='ipapracticecreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='ipapracticeupdate')

    def __str__(self):
        # return self.name
        return f"{self.ipa} | {self.practice}"

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        super(IpaPractice, self).save(*args, **kwargs)

        if not self.created_by:
            self.created_by = self.ipa.created_by
        self.updated_by = self.ipa.updated_by

        # super(Role, self).save(*args, **kwargs)
        super(IpaPractice, self).save(*args, **kwargs)


class Role(models.Model):

    role_name = models.CharField(max_length=45)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='rolecreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='role_update')
    privileges = models.ManyToManyField('Privilege', related_name='roles',through='RolePrivilege')
    active = models.BooleanField(null=True)

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'role'

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

    def __str__(self):
        return self.privilege_name

    class Meta:
        db_table = 'privilege'


class RolePrivilege(models.Model):
    role=models.ForeignKey(Role, on_delete=models.CASCADE)
    privilege=models.ForeignKey(Privilege, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='roleprivilagecreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='roleprivilage_update')

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        super(RolePrivilege, self).save(*args, **kwargs)

        if not self.created_by:
            self.created_by = self.role.created_by
        self.updated_by = self.role.updated_by

        # super(Role, self).save(*args, **kwargs)
        super(RolePrivilege, self).save(*args, **kwargs)


class UserIpaPractice(models.Model):
    user = models.ForeignKey(Optimus, on_delete=models.CASCADE, related_name='user_ipa_practices')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_ipa_practices')
    ipa_practice = models.ForeignKey(IpaPractice, on_delete=models.CASCADE, related_name='ipa_practice_users')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='useripapracticecreated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='useripapracticeupdate')

    class Meta:
        unique_together = ('user', 'ipa_practice')


