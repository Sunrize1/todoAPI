from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['patch'])
    def mark_as_done(self, request, pk=None):
        task = self.get_object()
        task.is_done = True
        task.save()
        return Response({'status': 'marked as done'})

    @action(detail=True, methods=['patch'])
    def mark_as_undone(self, request, pk=None):
        task = self.get_object()
        task.is_done = False
        task.save()
        return Response({'status': 'marked as undone'})

    @action(detail=False, methods=['post'])
    def replace_tasks(self, request):
        Task.objects.all().delete()
    
        tasks = request.data.get('tasks', [])
        for task_data in tasks:
            serializer = TaskSerializer(data=task_data)
            if serializer.is_valid():
                serializer.save()
    
        return Response({'status': 'tasks replaced'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def clear_tasks(self, request):
        Task.objects.filter(is_done=True).delete()
        return Response({'status': 'completed tasks cleared'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'])
    def all_done_tasks(self, request):
        tasks = Task.objects.filter(is_done=False)
        for task in tasks:
            task.is_done = True
            task.save()
        return Response({'status': 'all tasks marked as done'}, status=status.HTTP_200_OK)