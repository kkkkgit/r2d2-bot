from flask import Flask, Response
import cv2
import jetson_inference
import jetson_utils
import numpy as np

net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

app = Flask(__name__)

def generate():
    cam = cv2.VideoCapture('/dev/video0')
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cam.read()
        if not success:
            break

        height, width = frame.shape[:2]
        img_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
        cuda_img = jetson_utils.cudaFromNumpy(img_rgba)

        detections = net.Detect(cuda_img, width, height)

        for d in detections:
            left, top, right, bottom = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
            class_name = net.GetClassDesc(d.ClassID)
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255, 0), 2)
            cv2.putText(frame, class_name, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)