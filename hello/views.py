from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat
from .models import CNN
from django.views.decorators.csrf import csrf_exempt
import json


CONTENT_TYPES = ['image', 'video']
MAX_UPLOAD_SIZE = "10485760" # 10 MB
cnn = CNN()

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

@csrf_exempt
def classify(request):
	if request.method == 'POST' and 'image' in request.FILES:
		im = cnn.resize(request.FILES['image'])
		if im != None:
			return HttpResponse(json.dumps({'porn': cnn.predict(im) }), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'error': "resize image failed"}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'error': "No image received"}), content_type="application/json")


