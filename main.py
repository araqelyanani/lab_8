import cv2
import time

# 1 пункт
bgr_img = cv2.imread('variant-3.jpeg')

hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
cv2.imwrite('hsv_image.jpeg', hsv_img)

cv2.imshow("Original Image", bgr_img)
cv2.imshow('HSV image', hsv_img)

# 2, 3 пункты + допзадание
def video_processing():
    cap = cv2.VideoCapture('video.mp4')
    down_points = (640, 480)
    i = 0
    img = cv2.imread('img_1.png')
    img_height, img_width, _ = img.shape
    color_red = (0, 0, 255)
    a, b = 200, 200
    left_ang = ((down_points[0]-a)//2, (down_points[1]-b)//2) 
    right_ang = ((down_points[0]-a)//2 + a, (down_points[1]-b)//2 + b) 
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
        cv2.rectangle(frame, left_ang, right_ang, color_red, thickness=2, lineType=8, shift=0)  # квадрат 200х200
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if i % 5 == 0:
                a = x + (w // 2)
                b = y + (h // 2)
                # print(a, b)

            if x >= 220 and y >= 140 and x+w <= 440 and y+h <= 340: # проверка на попадание
                print(True)
            else:
                print(False)

            frame[y:y+img_height , x:x+img_width] = img # "добавляем муху"

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()

if __name__ == '__main__':
    video_processing()


cv2.waitKey(0)
cv2.destroyAllWindows()
