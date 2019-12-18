from pathlib import Path
import vectorize
import cv2
import numpy as np
import random
from utils import log

cascadeLoc = 'cascades/data/haarcascade_frontalface_alt2.xml'
face_cascade = cv2.CascadeClassifier(cascadeLoc)


def convert_data_to_vectors(root_path_str="./Data", text_file_str="tr_data.txt", skip_already_done=True):
    """
    Takes all videos and imgs in the data directory and converts them into
    vectors then writes those vectors to files
    Returns a list of vectors and a list of corresponding labels (which are the
    parent directory named after the person where that person's training data
    resides)
    """
    all_vectors = []
    labels = []
    img_types = ('**/*.jpg', '*/*.jpeg')
    vid_types = ('**/*.mp4', '*/*.mov')
    root_path = Path(root_path_str)
    class_paths = [x for x in root_path.iterdir() if x.is_dir()]
    dir_num = 1
    for path in class_paths:
        current_label = str(path.stem)
        log('current label: ' + current_label)
        vid_dir = path / "vids"
        imgs_dir = path / "imgs"
        train_path = path / text_file_str
        log(path)
        # log(vid_dir)
        # log(imgs_dir)
        if skip_already_done and train_path.is_file():
            log('directory already vectorized.')
            log('')
            continue

        imgs = []
        for t in vid_types:
            for vid_path in vid_dir.glob(t):
                log(vid_path)
                cap = cv2.VideoCapture(str(vid_path))
                i = 0
                while(cap.isOpened()):
                    # utils.log(i)
                    i+=1
                    ret, frame = cap.read()
                    if ret:
                        imgs.append(frame)
                    else:
                        break
                cap.release()
                log("Number of extracted frames: " + str(i))
                cv2.destroyAllWindows()
        for t in img_types:
            for img_path in imgs_dir.glob(t):
                # log(img_path)
                img = cv2.imread(str(img_path))
                if not (img is None):
                    imgs.append(img)

        log('Vectorizing:')
        vectors = vectorize.vectorize_images(imgs, True)
        log('Done vectorizing. Number of vectors generated: ' + str(len(vectors)))
        write_vectors_to_txt_file(train_path, vectors)

        for v in vectors:
            labels.append(current_label)
            all_vectors.append(v)

        log('done with directory: ' + str(dir_num))
        log('')
        dir_num += 1

    log('Loading all done\n')
    return all_vectors, labels  # obsolete return


def write_vectors_to_txt_file(file_path, vectors):
    f = open(file_path, 'w+')
    for v in vectors:
        line = ""
        for i in range(len(v)):
            num = str(v[i])
            line += num
            if i < len(v) - 1:
                line += ','
        f.write(line + '\n')
    f.close()


def load_vectors_cross(k_param, root_path_str="./Data"):
    """
    Loads all data from the data directory, prepared to do k-fold cross validation
    with k_param number of partitions
    """
    root_path = Path(root_path_str)
    class_paths = [x for x in root_path.iterdir() if x.is_dir()]
    data = []
    label_set = []
    for path in class_paths:
        label = str(path.stem)
        label_set.append(label)
        train_path = path / "tr_data.txt"
        tr_txt = open(str(train_path), "r+")
        tr_lines = tr_txt.readlines()
        for line in tr_lines:
            data.append((np.fromstring(line, dtype=float, sep=','), label))
        tr_txt.close()

    random.shuffle(data)

    xTr_partition = []  # list of cross-validation training sets
    yTr_partition = []  # list of corresponding cross-validation training label sets
    xV_partition = []  # list of cross-validation validation sets
    yV_partition = []  # list of corresponding cross-validation validation label sets
    k = k_param
    validation_length = int(len(data)/k)
    for i in range(k):
        v_start = int(validation_length * i)
        v_end = v_start + validation_length
        tr, v = data[0:v_start] + data[v_end:], data[v_start:v_end]

        def getX(t):
            return t[0]

        def getY(t):
            return t[1]

        xTr = list(map(getX, tr))
        xV = list(map(getX, v))
        yTr = list(map(getY, tr))
        yV = list(map(getY, v))

        xTr_partition.append(np.array(xTr))
        yTr_partition.append(np.array(yTr))
        xV_partition.append(np.array(xV))
        yV_partition.append(np.array(yV))

    xAll = np.array(list(map(getX, data)))
    yAll = np.array(list(map(getY, data)))

    return xTr_partition, yTr_partition, xV_partition, yV_partition, label_set, xAll, yAll


def load_vectors(path_name, text_file):
    # root_path = Path(path_name)
    root_path = path_name
    class_paths = [x for x in root_path.iterdir() if x.is_dir()]
    data = []
    label_set = []
    for path in class_paths:
        label = str(path.stem)
        label_set.append(label)
        train_path = path / text_file
        tr_txt = open(str(train_path), "r+")
        tr_lines = tr_txt.readlines()
        for line in tr_lines:
            data.append((np.fromstring(line, dtype=float, sep=','), label))
        tr_txt.close()

    combined = list(zip(*data))
    x = combined[0]
    y = combined[1]

    return np.array(x), np.array(y), label_set
    # def getX(t):
    #     return t[0]

    # def getY(t):
    #     return t[1]

    # xTr = list(map(getX, tr))
    # xV = list(map(getX, v))
    # yTr = list(map(getY, tr))
    # yV = list(map(getY, v))

def load_vectors_of_class(path_name, text_file, label_num):
    """
    label_num is +1 for positive and -1 for negative
    """
    # path = Path(path_name)
    path = path_name
    xTr = []
    yTr = []

    label = str(path.stem)
    train_path = path / text_file
    tr_txt = open(str(train_path), "r+")
    tr_lines = tr_txt.readlines()
    for line in tr_lines:
        xTr.append(np.fromstring(line, dtype=float, sep=','))
        yTr.append(label_num)
    tr_txt.close()

    return np.array(xTr), np.array(yTr), label
