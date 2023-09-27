from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import HasPermission
from .models import Role
from .serializers import RoleSerializer



class RoleAPIView(APIView):
    required_privilege = ["P4","P2"]
    permission_classes = [HasPermission]

    def get(self, request):
        queryset = Role.objects.all()
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

