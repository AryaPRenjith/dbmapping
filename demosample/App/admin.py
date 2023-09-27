from django.contrib import admin
from .models import Optimussignal,Role,Privilege,RolePrivilegeChange,IPA,Practice,IpaPracticeChange
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name','created_on','updated_on','created_by','updated_by')
    exclude = ('updated_on', 'created_by', 'updated_by')
    filter_horizontal = ('privileges',)

    def save_model(self, request, obj, form, change):
        # Set the created_by field to the currently logged-in user
        if not obj.pk:  # Check if a new object is being created
            obj.created_by = request.user
        else:
            # If it's an existing object being updated, set the updated_by field
            obj.updated_by = request.user
        obj.save()


class IPAAdmin(admin.ModelAdmin):
    list_display = ('name','created_on','updated_on','created_by','updated_by')
    exclude = ('updated_on', 'created_by', 'updated_by')
    filter_horizontal = ('practices',)

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






admin.site.register([Optimussignal,Privilege,RolePrivilegeChange,IpaPracticeChange])
admin.site.register(Role,RoleAdmin)
admin.site.register(IPA,IPAAdmin)
admin.site.register(Practice,PracticeAdmin)



