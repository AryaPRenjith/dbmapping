from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LogSample
from .serializers import LogSampleSerializer
from django.shortcuts import get_object_or_404
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils._os import safe_join
from django.utils.timezone import now

def log_api_action(user, action_flag, obj, message=''):
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.pk
    object_repr = str(obj)

    change_message = f'{action_flag} {object_repr}.'

    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=content_type.pk,
        object_id=object_id,
        object_repr=object_repr,
        action_flag=action_flag,
        change_message=change_message,
    )

class LogSampleAPIView(APIView):
    def get(self, request):
        queryset = LogSample.objects.all()
        serializer = LogSampleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogSampleSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            log_api_action(request.user, ADDITION, instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogSampleDetailAPIView(APIView):
    def get(self, request, pk):
        instance = get_object_or_404(LogSample, pk=pk)
        serializer = LogSampleSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = get_object_or_404(LogSample, pk=pk)
        serializer = LogSampleSerializer(instance, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            log_api_action(request.user, CHANGE, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = get_object_or_404(LogSample, pk=pk)
        instance.delete()
        log_api_action(request.user, DELETION, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)