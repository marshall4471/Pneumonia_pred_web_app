from rest_framework import serializers 
from .models import Inference
from . import run_inference

class InferenceSerializers(serializers.ModelSerializers):
    class Meta:
        model = Inference
        fields = ('name', 'result')

    def create(self, validated_data):
        name = validated_data.get('name')
        image = validated_data.get('image')
        inference_obj = Inference.objects.create(name=name, image=image)
        run_inference.delay(inference_obj.id)
        return inference_obj