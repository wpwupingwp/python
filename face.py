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