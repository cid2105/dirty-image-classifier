from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat
from .models import CNN
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import json
import urllib, cStringIO
import logging, logging.config

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)
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
	logger.info(request)
	if request.method == 'POST':
		if 'image' in request.FILES:
			im = cnn.resize(request.FILES['image'])
			return HttpResponse(process_image(im), content_type="application/json")
		if 'URL' in request.POST:
			file = cStringIO.StringIO(urllib.urlopen(request.POST['URL']).read())
			im = cnn.resize(file)
			if im is not None:
				return HttpResponse(process_image(im), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'error': "Bad URL"}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'error': "No image received"}), content_type="application/json")


