# https://colab.research.google.com/drive/1lE3h1sDXNb0nS6Q2V5gVBpMxtVjY3_RE#scrollTo=y_6bGjoPtzau

import logging

import tensorflow as tf
import tensorflow_hub as hub

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

CLASSIFIER_URL ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"
IMAGE_RES = 224

model = tf.keras.Sequential([
    hub.KerasLayer(CLASSIFIER_URL, input_shape=(IMAGE_RES, IMAGE_RES, 3))
])

