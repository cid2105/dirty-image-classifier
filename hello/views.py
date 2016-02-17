from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat
from .models import CNN
from django.views.decorators.csrf import csrf_exempt
import json
import urllib, cStringIO


CONTENT_TYPES = ['image', 'video']
MAX_UPLOAD_SIZE = "10485760" # 10 MB
cnn = CNN()

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def process_image(im):
	if im != None:
		return json.dumps({'porn': cnn.predict(im) })
	else:
		return json.dumps({'error': "resize image failed"})

@csrf_exempt
def classify(request):
	if request.method == 'POST':
		if 'image' in request.FILES:
			im = cnn.resize(request.FILES['image'])
			return HttpResponse(process_image(im), content_type="application/json")
		if 'url' in request.POST:
			file = cStringIO.StringIO(urllib.urlopen(URL).read())
			im = Image.open(file)
			return HttpResponse(process_image(im), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'error': "No image received"}), content_type="application/json")


