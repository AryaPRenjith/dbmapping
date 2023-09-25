from django.contrib import admin
from .models import Optimus, IPA, Practice, Role, Privilege,RolePrivilege,IpaPractice,UserIpaPractice

from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Group


class UserIpaPracticeInline(admin.TabularInline):
    model = UserIpaPractice
    fk_name = 'user'
    exclude = ('updated_on', 'created_by', 'updated_by')

class OptimusAdmin(UserAdmin):
    model = Optimus
    list_display = ('username', 'email', 'gender', 'dob', 'created_at', 'updated_at')
    exclude = ['created_by', 'updated_by']
    inlines = (UserIpaPracticeInline,)


    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2", "first_name", "last_name","email","gender","dob","role","ipa","groups"],
            },
        ),
    ]
    fieldsets = [
        (None, {"fields": ["username","password"]}),  # stuff to edit in an existing datapoint
        ("Personal info", {"fields": ["first_name", "last_name","role","ipa","groups","default_practice"]},),


    ]


class IpaPracticeInline(admin.TabularInline):
    model = IpaPractice
    # exclude = ('updated_on',)
    exclude = ('updated_on', 'created_by', 'updated_by')


class IPAAdmin(admin.ModelAdmin):
    list_display = ('name','created_on','updated_on','created_by','updated_by')
    exclude = ('updated_on', 'created_by', 'updated_by')
    inlines = (IpaPracticeInline,)

    def save_model(self, request, obj, form, change):
        # Set the created_by field to the currently logged-in user
        if not obj.pk:  # Check if a new object is being created
            obj.created_by = request.user
        else:
            # If it's an existing object being updated, set the updated_by field
            obj.updated_by = request.user
        obj.save()


class PracticeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('updated_on', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        # Set the created_by field to the currently logged-in user
        if not obj.pk:  # Check if a new object is being created
            obj.created_by = request.user
        else:
            # If it's an existing object being updated, set the updated_by field
            obj.updated_by = request.user
        obj.save()

class IpaPracticeAdmin(admin.ModelAdmin):
    list_display = ('ipa', 'practice', 'created_by', 'updated_by', 'created_on', 'updated_on')

class RolePrivilegeInline(admin.TabularInline):
    model = RolePrivilege
    # exclude = ('updated_on',)
    exclude = ('updated_on', 'created_by', 'updated_by')





class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name','created_on','updated_on','created_by','updated_by')
    exclude = ('updated_on', 'created_by', 'updated_by')
    inlines = (RolePrivilegeInline,)


    def save_model(self, request, obj, form, change):
        # Set the created_by field to the currently logged-in user
        if not obj.pk:  # Check if a new object is being created
            obj.created_by = request.user
        else:
            # If it's an existing object being updated, set the updated_by field
            obj.updated_by = request.user
        obj.save()




class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('privilege_name',)
    # exclude = ('updated_on', 'created_by', 'updated_by')

class RolePrivilegeAdmin(admin.ModelAdmin):
    list_display = ('role', 'privilege', 'created_by', 'updated_by', 'created_on', 'updated_on')


class UserIpaPracticeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role','created_by', 'updated_by', 'created_on', 'updated_on')



admin.site.register(Optimus, OptimusAdmin)
admin.site.register(IPA, IPAAdmin)
admin.site.register(Practice, PracticeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
admin.site.register(RolePrivilege,RolePrivilegeAdmin)
admin.site.register(IpaPractice,IpaPracticeAdmin)
admin.site.register(UserIpaPractice,UserIpaPracticeAdmin)




