
from picamera2 import Picamera2
from flask import Flask, send_file
import io

app = Flask(__name__)
picam2 = Picamera2()
picam2.start()

@app.route('/capture')
def capture():
    image = picam2.capture_image()
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)