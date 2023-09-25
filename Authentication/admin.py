from django.contrib import admin
from .models import Profile, IPA, Practice, Role, Privilege
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_ipa', 'get_practice', 'get_role')
    exclude = ('default_practice',)
    
    def get_ipa(self, obj):
        return "\n".join([x.name for x in obj.ipa.all()])

    def get_practice(self, obj):
        return "\n".join([p.name for p in obj.practice.all()])

    def get_role(self, obj):
        return "\n".join([r.role_name for r in obj.role.all()])


class IPAAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PracticeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)


class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('privilege_name',)


class CustomProfileInline(admin.StackedInline):  # Custom inline to display only practice as dropdown
    model = Profile
    fields = ('default_practice',)  # Specify the fields you want to display

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        if obj:  # If obj is not None, i.e., editing an existing user
            formset.form.base_fields['default_practice'].queryset = obj.profile.practice.all()

        return formset


class CustomUserAdmin(UserAdmin):
    inlines = (CustomProfileInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if 'default_practice' in form.cleaned_data:
            obj.profile.default_practice = form.cleaned_data['default_practice']
            obj.profile.save()


admin.site.register(Profile, ProfileAdmin)
admin.site.register(IPA, IPAAdmin)
admin.site.register(Practice, PracticeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Privilege, PrivilegeAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)