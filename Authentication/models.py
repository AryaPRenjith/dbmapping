from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

IPAs = [("1", "Somos"), ("2", "Excelsior"), ("3", "Corinthian")]
Roles = [("1", "IPA Admin"), ("2", "IPA Level"), ("3", "TIN Level")]
Practices = [
    ("1", "Fishman Centero for Total Eye Care"),
    ("2", "Ridgewood Pediatrics, PC"),
    ("3", "Kings Pulmnary Associates, PC"),
    ("4", "MB Medical Associates, PC"),
]
privileges = [
    ("1", "ELIGIBILITY PRACTICE DASHBOARD VIEW"),
    ("2", "ELIGIBILITY OUTREACH DASHBOARD VIEW"),
    ("3", "HEDIS DASHBOARD VIEW"),
]


# model of IPA table
class IPA(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ipa"  # DB table name


# practice table model
class Practice(models.Model):
    ipa = models.ForeignKey(IPA, on_delete=models.CASCADE)
    tin = models.CharField(max_length=45, default="12345")
    name = models.CharField(max_length=100)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.tin} | {self.name}"

    class Meta:
        db_table = "practice"  # DB table name


#  Role table model
class Role(models.Model):
    role_name = models.CharField(max_length=45)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name="rolecreated")
    updated_by = UserForeignKey(auto_user_add=True, related_name="role_update")
    privileges = models.ManyToManyField("Privilege", related_name="roles")

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = "role"


# privilege table model
class Privilege(models.Model):
    privilege_key = models.CharField(max_length=45)
    privilege_group_name = models.CharField(max_length=45)
    privilege_name = models.CharField(max_length=45)
    privilege_description = models.CharField(max_length=45)
    active = models.BooleanField()

    def __str__(self):
        return self.privilege_name

    class Meta:
        db_table = "privilege"


# Duplicate model of Auth_user
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    ipa = models.ManyToManyField(IPA, related_name="profiles_ipa", blank=True)
    practice = models.ManyToManyField(
        Practice, related_name="profiles_practice", blank=True
    )
    role = models.ManyToManyField(
        Role, related_name="profiles_role", blank=True
    )
    default_practice = models.ForeignKey(
        Practice,
        on_delete=models.SET_NULL,
        related_name="default_profiles",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "optimus_user"
