from django.contrib import admin
from .models import Role,privileges,CustomRolePrivilege
from django.contrib.auth.admin import UserAdmin

class CustomRolePrivilegeAdmin(UserAdmin):
    model = CustomRolePrivilege
    # list_display = ('username', 'email', 'gender', 'dob')
    exclude = ['created_by', 'updated_by']


    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2", "first_name", "last_name","email","role"],
            },
        ),
    ]
    fieldsets = [
        (None, {"fields": ["username","password"]}),  # stuff to edit in an existing datapoint
        ("Personal info", {"fields": ["first_name", "last_name","role"]},),


    ]


# Register your models here.
admin.site.register(Role)
admin.site.register(privileges)
admin.site.register(CustomRolePrivilege,CustomRolePrivilegeAdmin)