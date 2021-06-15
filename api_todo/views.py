from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>',
        'Delete': '/task-delete/<str:pk>',
    }
    return Response(api_urls)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def task_create(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    
    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def task_update(request, pk):

    if request.method == "GET":
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task)

        return Response(serializer.data)

    if request.method == "POST":
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(instance=task, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    serializer = TaskSerializer(task)

    if request.method == "DELETE":
        task.delete()

    return Response(serializer.data)
