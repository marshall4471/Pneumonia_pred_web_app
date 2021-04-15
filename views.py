from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from .serializer import InferenceSerializer
from .models import Inference
from celery.result import AsyncResult

class InferenceViewSet(viewsets.ModelViewSet):

    serializer_class = InferenceSerializer
    queryset = Inference.objects.all()

    @action(methods=['GET'], detail=True)
    def monitor_inference_progress(self, request, slug):
        inference_obj = self.get_object()
        progress = 100
        result = AsyncResult(inference_obj.task_id)
        if isinstance(result.info, dict):
            progress = result.info['progress']
        description = result.state
        return Response({'progress': progress, 'description': description}, status=status.HTTP_200_OK)

