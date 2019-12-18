from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import sys
import cv2
from embeddings.downloaded_facenet import facenet
import os
from utils import log

model_dir = os.path.join('.', 'embeddings', '20180402-114759.pb')

def make_embeddings(img_list):
    """
    takes in a list of cv images of already-detected and cropped faces
    and returns a list of vectors that are the embeddings of each of these
    images
    """

    with tf.Graph().as_default():

        with tf.Session() as sess:

            # Load the model
            log('Loading feature extraction model')
            # facenet.load_model('20170512-110547.pb', )
            facenet.load_model(model_dir)
            log('done loading')

            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            images = np.stack(img_list)

            # Run forward pass to calculate embeddings
            feed_dict = {
                    images_placeholder: images,
                    phase_train_placeholder: False
                }
            emb = sess.run(embeddings, feed_dict=feed_dict)

            return emb
