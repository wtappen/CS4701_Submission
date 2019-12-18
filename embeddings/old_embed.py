from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import scipy
import tensorflow as tf
import numpy as np
import os
import sys
import math
import cv2
from sklearn.svm import SVC
from downloaded_facenet import facenet

with tf.Graph().as_default():

    with tf.Session() as sess:

        # Load the model
        print('Loading feature extraction model')
        # p = os.path.join('C:', 'Users', 'wtapp', 'OneDrive', 'College', '5th_Semester', 'AI_Prac', 'embedding_weights', '20170512-110547.pb')
        facenet.load_model('20170512-110547.pb', )
        print('done loading')

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        # embedding_size = embeddings.get_shape()[1]


        start_images = [
            "test_face.jpg",
            "test_img_2.jpg",
            "african_woman_cropped.jpeg",
            "elderly_man.jpg",
        ]

        num_images = len(start_images)

        img_list = []

        for img_name in start_images:

            # img = imageio.imread(img_name, as_gray=False, pilmode="RGB")
            img = cv2.imread(img_name)
            # im = Image.fromarray(img)
            # new_image = np.array(im.resize((200, 200), Image.BILINEAR))
            img_resized = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LINEAR)
            prewhitened = facenet.prewhiten(img_resized)
            img_list.append(prewhitened)

        images = np.stack(img_list)

        # Run forward pass to calculate embeddings
        feed_dict = {
                images_placeholder: images,
                phase_train_placeholder: False
            }
        emb = sess.run(embeddings, feed_dict=feed_dict)
        # print(emb[0])
        # print(emb[1])

        dist = np.sqrt(np.sum(np.square(np.subtract(emb[0, :], emb[1, :]))))
        print(np.linalg.norm(emb[3]))
        # print('  %1.4f  ' % dist, end='')
        # print()
        # print(scipy.spatial.distance.cosine(emb[0, :], emb[1, :]))
        # print()
        # dist = np.sqrt(np.sum(np.square(np.subtract(emb[0,:], emb[2,:]))))
        # print('  %1.4f  ' % dist, end='')
        # print(scipy.spatial.distance.cosine(emb[0,:], emb[2,:]))
        # print()
        # dist = np.sqrt(np.sum(np.square(np.subtract(emb[0,:], emb[3,:]))))
        # print('  %1.4f  ' % dist, end='')
        # print(scipy.spatial.distance.cosine(emb[0,:], emb[3,:]))
        # print()
        # print(type(emb[0]))
