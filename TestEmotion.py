import cv2
import numpy as np
from keras.models import model_from_json
import time


emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

fps_start_time = 0
fps = 0
total_fps = 0
frame_count = 0

# load json and create model
json_file = open('emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("emotion_model.h5")
print("Loaded model from disk")



# start the webcam feed
cap = cv2.VideoCapture(0)
# pass here your video path
# cap = cv2.VideoCapture("C:\\JustDoIt\\ML\\Sample_videos\\emotion_sample6.mp4")

while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    frame = cv2.resize(frame, (480, 720))

    fps_end_time = time.time()
    time_diff = fps_end_time - fps_start_time
    fps = 1 / (time_diff)
    fps_start_time = fps_end_time
    fps_text = "FPS: {:.2f}".format(fps)
    font = cv2.FONT_HERSHEY_PLAIN

    # total_fps += fps
    # frame_count += 1
    # average_fps = total_fps / frame_count
    # average_fps_text = "Average FPS: {:.2f}".format(average_fps)

    if not ret:
        break
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces available on camera
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w] # isolates the face region
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        # gives array of the prob values of each emotion
        maxindex = int(np.argmax(emotion_prediction))
        # gives max value ka posn from that arrays
        cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.putText(frame, fps_text, (10, 200), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
    # cv2.putText(frame, average_fps_text, (10, 250), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
