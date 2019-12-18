
from embeddings.downloaded_facenet import facenet
import cv2

def adjust(img, dim):
    """
    returns the cv img resized to be size dim x dim and whitened with the facenet.prewhiten
    function
    """

    img_resized = cv2.resize(img, (dim, dim), interpolation=cv2.INTER_LINEAR)
    prewhitened = facenet.prewhiten(img_resized)
    return prewhitened