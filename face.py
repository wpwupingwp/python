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


# test_camera()

def face_detect():
    import numpy as np
    import cv2
    faceCascade = cv2.CascadeClassifier(
        'Cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)  # set Height
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, -1)
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
        cv2.imshow('video', img)
        cv2.imshow('roi_gray', roi_gray)
        cv2.imshow('roi_color', roi_color)
        k = cv2.waitKey(30)
        if k == 27:  # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
    return

# face_detect()

def _():
    from time import sleep

    import requests
    from faker import Faker
    import cv2
    import numpy as np

    f = Faker(locale='zh')


    def get_face(number=5):
        folder = Path('train')
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


    names = list()
    encodings = list()
    train = Path('train')
    train_images = train.glob('*.webp')
    for i in train_images:
        name = i.stem
        names.append(name)
        encodings.append(encoding)

    test = Path('test') / 'trump-sessions-resign.webp'