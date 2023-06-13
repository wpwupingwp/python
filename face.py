def test_gray(img_file):
    import cv2
    img = cv2.imread(img_file)
     

    pass



def test_camera():
    import numpy as np
    import cv2
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, -1)  # Flip camera vertically
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        k = cv2.waitKey()
        if k == 27:  # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()


def test_camera2():
    import numpy as np
    import cv2
    from pathlib import Path
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)  # set Width
    cap.set(4, 640)  # set Heightwhile(True):
    while True:
        ret, frame = cap.read()
        if frame is None:
            continue
        # frame = cv2.flip(frame, 0) # Flip camera vertically
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        # cv2.imshow('blue', frame[:,:,0])
        edge = cv2.Canny(gray, 16, 200)
        blur = cv2.GaussianBlur(frame, (15, 15), 0)
        revert = 255 - frame
        cv2.imshow('edge', edge)
        cv2.imshow('blur', blur)
        cv2.imshow('revert', revert)

        k = cv2.waitKey()
        if k == 27:  # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
    return


# test_camera()
def face_detect():
    import numpy as np
    import cv2
    from pathlib import Path
    classifier_file1 = Path(
        cv2.__file__).parent / 'data' / 'haarcascade_frontalface_default.xml'
    classifier_file2 = Path(
        cv2.__file__).parent / 'data' / 'haarcascade_eye.xml'
    faceCascade = cv2.CascadeClassifier(str(classifier_file1))
    eye_cascade = cv2.CascadeClassifier(str(classifier_file2))
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Heightwhile True:
    while True:
        ret, img = cap.read()
        # img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.5,
                minNeighbors=10,
                minSize=(5, 5),
            )
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex + ew, ey + eh),
                              (0, 255, 50), 2)
        cv2.imshow('video', img)
        k = cv2.waitKey()
        if k == 27:  # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
    return


def face_detection_dnn():
    # import packages
    import numpy as np
    import cv2

    from sys import argv

    # image_file = argv[1]
    # https://github.com/spmallick/learnopencv/blob/master/FaceDetectionComparison/models/deploy.prototxt
    model_text = 'deploy.prototxt'
    model_file = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'

    net = cv2.dnn.readNetFromCaffe(model_text, model_file)

    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        # loop over the detections to extract specific confidence
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < 0.5:
                continue
            # compute the boxes (x, y)-coordinates
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (x1, y1, x2, y2) = box.astype('int')
            if y1 - 10 > 10:
                y = y1 - 10
            else:
                y = y1 + 10
            text = '{:.2f}'.format(confidence * 100)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y), cv2.LINE_AA, 0.45, (0, 0, 255), 2)
        cv2.imshow('video', frame)
        k = cv2.waitKey()
        if k == 27:  # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
    return


def get_face(frame):
    import cv2
    import numpy as np
    model_text = 'deploy.prototxt'
    model_file = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'

    net = cv2.dnn.readNetFromCaffe(model_text, model_file)
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    faces = list()
    # loop over the detections to extract specific confidence
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < 0.5:
            continue
        # compute the boxes (x, y)-coordinates
        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
        (x1, y1, x2, y2) = box.astype('int')
        if y1 - 10 > 10:
            y = y1 - 10
        else:
            y = y1 + 10
        face = (x1, y1, x2, y2)
        faces.append(face)
    return faces


def get_face_imgs(number=5):
    from pathlib import Path
    from time import sleep
    from faker import Faker
    import requests

    f = Faker(locale='zh')

    folder = Path('./train')
    if not folder.exists():
        folder.mkdir()
    url = 'https://thispersondoesnotexist.com/'
    number = 5
    for _ in range(number):
        r = requests.get(url)
        filename = f.name() + '.webp'
        out = open(filename, 'wb')
        out.write(r.content)
        print('Got', filename)
        sleep(2)
    return folder


def face_recognition():
    # import packages
    import numpy as np
    import cv2

    from pathlib import Path

    train_folder = get_face_imgs()
    face_sample = list()
    names = list()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    n = 0
    id_name = dict()
    for img_file in train_folder.glob('*.webp'):
        name = img_file.stem
        id_name[n] = name
        n = n + 1
        fake_name = str(n)
        img = cv2.imread(str(img_file), cv2.CV_LOAD_IMAGE_GRAYSCALE)
        faces = get_face(img)
        for face_box in faces:
            x1, y1, x2, y2 = face_box
            face = img[x1:x2, y1:y2]
            face_sample.append(face)
            names.append(fake_name)
    recognizer.train(faces, np.array(names))
    recognizer.write(train_folder / 'trainer.yml')
    recognizer.read(train_folder / 'trainer.yml')

    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = get_face(frame)
        for face in faces:
            x1, y1, x2, y2 = face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            detect_id, confidence = recognizer.predict(gray[x1:x2, y1:y2])
            if 0 <= confidence <= 100:
                detect_name = id_name[detect_id]
            else:
                detect_name = 'unknown'
            conf_text = ' {}%'.format(round(100-confidence))
            cv2.putText(frame, detect_name+conf_text, (x1+5, y1+5), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
        cv2.imshow('video', frame)
        k = cv2.waitKey()
        if k == 27:  # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
