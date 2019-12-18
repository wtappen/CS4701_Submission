import vectorize
import base64
from imageio import imread
import io
import cv2


def classify_img(img, label):
    vectors = vectorize.vectorize_images([img], False)
    if not vectors.any():  # if empty
        return False
    else:
        return True  # TODO


def convert_image(img_str):
    # takes in a base64 string encoding of and image and returns a cv2 image

    img = base64.b64decode(img_str)
    img = imread(io.BytesIO(img))
    cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return cv2_img
