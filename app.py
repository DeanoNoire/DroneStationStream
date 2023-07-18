from flask import Flask, Response, render_template
import cv2
import time
import io

app = Flask(__name__)

def gen_frames():
    while True:
        # Capture frame-by-frame
        cap = cv2.VideoCapture(0)
        success, frame = cap.read()
        if not success:
            break
        else:
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            ret, buffer = cv2.imencode('.jpg', rotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def index():
    # Render index.html template
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

