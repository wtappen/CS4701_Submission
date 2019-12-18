import cv2
from pathlib import Path
import urllib.request as request
import numpy as np
from progress.bar import Bar

actors_path = Path(".") / "faceScrub_release" / "facescrub_actors.txt"
actresses_path = Path(".") / "faceScrub_release" / "facescrub_actresses.txt"
test_dir = Path(".") / "faceScrub_big_test" / "imgs"
val_dir = Path(".") / "faceScrub_big_val" / "imgs"
train_dir = Path(".") / "faceScrub_big_train" / "imgs"


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    image = None
    code = -1

    try:
        resp = request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except Exception:
        # print("Skipped: " + url)
        code = 1

    # return the image
    return image, code


def extract_img_info(path):
    # get image urls and their corresponding labels (names)

    links = []
    labels = []
    with open(path, 'r') as f:
        for line in f:
            split_line = line.split("\t")
            link = split_line[3]
            if link.endswith('.jpg'):
                links.append(link)
                name = split_line[0]
                label = name.replace(' ', '_')
                labels.append(label)

    links = links[1:]
    labels = labels[1:]
    return links, labels


def partition_images(path, overall_count):
    title = 'partitioning: ' + str(path)
    C = 20

    num_skipped = 0

    links, labels = extract_img_info(path)
    same_label_count = 0
    labels.reverse()
    links.reverse()
    last_label = labels[0]

    bar = Bar(title, max=len(links))

    for i in range(len(links)):
        bar.next()
        current_label = labels[i]
        if last_label == current_label and same_label_count >= C:
            last_label = current_label
            continue

        overall_count += 1
        if last_label == current_label:
            same_label_count += 1
        else:
            same_label_count = 1
        if same_label_count > C:
            continue

        img, code = url_to_image(links[i])
        
        if code < 0:  
            current_dir = train_dir
            # if same_label_count % 3 == 2:
            #     current_dir = val_dir
            #     continue
            # elif same_label_count % 3 == 0:
            #     current_dir = test_dir
            #     continue

            img_name = current_label + '_' + str(same_label_count) + "_" + str(overall_count) + '.jpg'

            cv2.imwrite(str(current_dir / img_name), img)
        else:
            num_skipped += 1

        last_label = current_label

    bar.finish()
    return overall_count + 1


# count = partition_images(actors_path, 0)
# partition_images(actresses_path, count)

def check_color(dir):
    # seems to not matter in the end

    for img_path in dir.glob(".jpg"):
        i = cv2.imread(img_path)
        size = i.shape
        if len(size) == 3:
            pass
        elif len(size) == 2:
            print(str(img_path))
        else:
            print('hmm')


c = partition_images(actors_path, 0)
partition_images(actresses_path, c)
