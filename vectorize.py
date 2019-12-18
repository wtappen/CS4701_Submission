from embeddings import embed
import preprocess
import detect
from utils import log

DIM = 160  # DO NOT CHANGE, will change the num of embeddings for each face


def vectorize_images(img_list, only_largest):
    """
    takes in a list of cv images and returns a list of embeddings for the
    faces found in those images. If only_lagrest is true, then only the
    embedding for the largest face detected in each image will be returned
    """

    detected_list = []
    for i in img_list:
        detected_list += detect.detect_faces(i, only_largest)
    num_detected = len(detected_list)
    log("Number of detected faces: " + str(num_detected))
    preprocessed_list = []
    for d in detected_list:
        preprocessed_list.append(preprocess.adjust(d, DIM))
    return embed.make_embeddings(preprocessed_list)
