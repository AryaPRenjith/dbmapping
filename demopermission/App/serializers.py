from rest_framework import serializers
from .models import Role, privileges

class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = privileges
        fields = ('name', 'code_name')

class RoleSerializer(serializers.ModelSerializer):
    role_permissions = PrivilegeSerializer(many=True)

    class Meta:
        model = Role
        fields = ('name', 'role_permissions')
