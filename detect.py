import cv2 as cv

cascadeLoc = 'cascades/data/haarcascade_frontalface_default.xml'
face_cascade = cv.CascadeClassifier(cascadeLoc)


def detect_faces(color_img, only_largest):
    """
    takes in a color image read in using cv2 and returns a list of cropped
    color images of the detected faces. If only_largest is true, then only
    the largest detected face will be returned.
    """

    gray = cv.cvtColor(color_img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)
    cropped_list = []

    i = -1
    largest_index = -1
    largest_size = -1

    for (x, y, w, h) in faces:
        i += 1
        size = w * h
        if size > largest_size:
            largest_index = i
            largest_size = size

        cropped_color = color_img[y:y+h, x:x+w]
        cropped_list.append(cropped_color)

    if only_largest and largest_size > -1:
        cropped_list = [cropped_list[largest_index]]

    return cropped_list
