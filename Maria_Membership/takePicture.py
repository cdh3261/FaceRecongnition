import cv2
import os
import face_recognition


def takePt(name, phone):
    cnt = 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 800)  # set video width
    cam.set(4, 600)  # set video height

    # 경로 설정
    path = 'C:/Users/multicampus/_dongho/First_PJT/Maria_Membership/haarcascades/'

    # 오픈 소스 사용
    face_detector = cv2.CascadeClassifier(
        path+'haarcascade_frontalface_default.xml')
    eyeCascade = cv2.CascadeClassifier(path+'haarcascade_eye.xml')
    smileCascade = cv2.CascadeClassifier(path+'haarcascade_smile.xml')

    # 회원 가입시 입력한 이름을 받아온다.
    userName = name
    phoneNumber = phone
    # print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    bool_face,bool_eye,bool_mouth = False,False,False
    # 스페이스바 누를 때가지 화면 ON
    while 1:
        ret, img = cam.read()

        # flip video image vertically
        img = cv2.flip(img, 1)

        # 이미지 흑백으로 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # 얼굴 인식
        bool_face = False
        for (x, y, w, h) in faces:
            bool_face = True
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            # 눈 부분 인식
            bool_eye = False
            eyes = eyeCascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.5,
                minNeighbors=10,
                minSize=(5, 5)
            )
            for (ex, ey, ew, eh) in eyes:
                bool_eye = True
                cv2.rectangle(roi_color, (ex, ey),
                              (ex + ew, ey + eh), (0, 255, 0), 2)

            # 웃는 입 인식
            smile = smileCascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.5,
                minNeighbors=15,
                minSize=(25, 25),
            )
            bool_mouth = False
            for (xx, yy, ww, hh) in smile:
                bool_eye = True
                cv2.rectangle(roi_color, (xx, yy),
                              (xx + ww, yy + hh), (0, 255, 0), 2)
            
            
        cv2.imshow('video', img)
        start = cv2.waitKey(1) & 0xff
        print(bool_eye, bool_face, bool_mouth)
        if (bool_eye and bool_face) or (bool_mouth and bool_face):
            cnt += 1
            if cnt == 10:
                start = 32
        # 스페이스 바를 누르면 종료, ESC를 누르면 취소.
        if start == 32:
            img_path = 'C:/Users/multicampus/_dongho/First_PJT/Maria_Membership/newFace/'
            # print('start')
            # 사진이 잘못 저장되었을 경우
            try:
                cv2.imwrite(img_path + phoneNumber +
                            ".jpg", gray[y:y+h, x:x+w])
                # print('face')
                filename = phoneNumber + ".jpg"
                pathname = os.path.join(img_path, filename)
                img = face_recognition.load_image_file(pathname)
                # print('face2')
                face_encoding = face_recognition.face_encodings(img)[0]
                cam.release()
                cv2.destroyAllWindows()
                return 32
                # print('face3')
            except:
                start = 27
                cam.release()
                cv2.destroyAllWindows()
                return 999
            break

        elif start == 27:
            break

    # cv2.destroyAllWindows()
    # 저장 화면 표시, 스페이스 바를 누르면 종료
    # if start == 32:
    #     while 1:
    #         cv2.imshow('Face Save', img)
    #         k = cv2.waitKey(10) & 0xff

    #         # 스페이스 바를 누르면 저장
    #         if k == 32:
    #             # print('save')
    #             # img_path = 'C:/Users/multicampus/_dongho/First_PJT/Maria_Membership/'
    #             # print('save2')
    #             # cv2.imwrite(img_path + "newFace/" + userName + ".jpg", gray[y:y+h,x:x+w])
    #             # print('save3')
    #             cam.release()
    #             cv2.destroyAllWindows()
    #             return 32

    #         # ESC를 누르면 저장하지 않는다.
    #         elif k == 27:
    #             cam.release()
    #             cv2.destroyAllWindows()
    #             return 27
    # elif start == 27:
    #     cam.release()
    #     cv2.destroyAllWindows()
    #     return 27

    # Do a bit of cleanup
    # print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
