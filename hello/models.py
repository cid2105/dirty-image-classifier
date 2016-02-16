from django.db import models
from lasagne.layers import DenseLayer
from lasagne.layers import InputLayer
from lasagne.layers import DropoutLayer
from lasagne.layers import Conv2DLayer
from lasagne.layers import MaxPool2DLayer
from lasagne.nonlinearities import softmax
from lasagne.updates import adam
from lasagne.layers import get_all_params
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import TrainSplit
from nolearn.lasagne import objective
from PIL import Image, ImageOps
import numpy as np
import logging, logging.config
import sys

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

# Create your models here.

class Singleton(type):
	def __init__(cls, name, bases, dict):
		super(Singleton, cls).__init__(name, bases, dict)
		cls.instance = None 
	def __call__(cls,*args,**kw):
		if cls.instance is None:
			cls.instance = super(Singleton, cls).__call__(*args, **kw)
		return cls.instance

class CNN(object):
	__metaclass__ = Singleton
	channels = 3
	image_size = [64,64]
	layers = [ 
		# layer dealing with the input data
		(InputLayer, {'shape': (None, channels, image_size[0], image_size[1])}),
		# first stage of our convolutional layers 
		(Conv2DLayer, {'num_filters': 32, 'filter_size': 9}),
		(Conv2DLayer, {'num_filters': 32, 'filter_size': 5}),
		(MaxPool2DLayer, {'pool_size': 2}),
		# second stage of our convolutional layers
		(Conv2DLayer, {'num_filters': 32, 'filter_size': 5}),
		(Conv2DLayer, {'num_filters': 32, 'filter_size': 3}),
		(MaxPool2DLayer, {'pool_size': 2}),
		# two dense layers with dropout
		(DenseLayer, {'num_units': 256}),
		(DropoutLayer, {}),
		(DenseLayer, {'num_units': 256}),
		# the output layer
		(DenseLayer, {'num_units': 2, 'nonlinearity': softmax}),
	]
	def __init__(self):
		logger = logging.getLogger(__name__)
		logger.info("Initializing neural net...")
		self.net = NeuralNet(layers=self.layers, update_learning_rate=0.0002 )
		self.net.load_params_from("conv_params")
		logger.info("Finished loading parameters")
	
	def resize(self, infile):
		try:
			im = Image.open(infile)
			resized_im = np.array(ImageOps.fit(im, (self.image_size[0], self.image_size[1]), Image.ANTIALIAS), dtype=np.uint8)
			rgb = np.array([resized_im[:,:,0], resized_im[:,:,1], resized_im[:,:,2]])
			return rgb.reshape(1,self.channels,self.image_size[0],self.image_size[1])

		except IOError:
			return "cannot create thumbnail for '%s'" % infile

	def predict(self, X):
		porn = self.net.predict(X)[0] == 1
		return "true" if porn else "false"
    	