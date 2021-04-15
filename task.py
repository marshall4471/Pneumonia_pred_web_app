from MyApp.celery import app 
import numpy as np
from keras.preprocessing import image
from keras.models import model_from_json
from .models import Inference

@app.task(bind=True)
def run_inference(self, inference_id):

    inference_obj = Inference.objects.get(id=inference_id)
    inference_obj.task_id = self.request.id
    inference_obj.save()

    self.update_state(state='image preprocessing', meta={'progress': 0})
    img = image.load_img(inference_obj.image.file.filename, target_size=(150, 150))
    img_array = image.image_to_array(img)
    img_array.shape = (1, 150, 150, 3)

    self.update_state(state='load the model', meta={'progress': 25})

    with open('./model_architecture.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights('./model_weights.h5')

    self.update_state(state='predict the image', meta={'progress': 50})
    prediction = model.predict(img_array, verbose=1)
    result = 'unknown'
    if prediction < 0.5 :
        result = 'Normal'
    elif prediction > 0.5 :
        result = 'Pneumonia'
    inference_obj.result = result
    inference_obj.save()

    self.update_state(state='Finished', meta={'progress': 100})