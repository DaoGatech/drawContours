from flask import Flask, render_template, request
from flask_restful import Api
from flask_bootstrap import Bootstrap
import base64
import cv2
app = Flask(__name__)
drawContours = Api(app)
Bootstrap(app)


@app.route('/')
def index():
    """Rendering draw homepage"""
    return render_template('index.html')


@app.route('/evaluate', methods=["POST"])
def evaluate():
    image_b64 = request.values['imageBase64']
    content = image_b64.split(';')[1]
    image_encoded = content.split(',')[1]
    body = base64.b64decode(image_encoded.encode('utf-8'))
    filename = 't.jpg'
    with open(filename, 'wb') as f:
        f.write(body)
    analyze()
    return ''


def analyze():
    image = cv2.imread('t.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Extract Contours
    _, contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        # Get approximate polygons
        approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)

        print(len(approx))
        if len(approx) == 3:
            return "Triangle"

        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            if abs(w - h) <= 3:
                return "Square"
            else:
                return "Rectangle"
        elif len(approx) == 10:
            return "Star"


if __name__ == '__main__':
    app.run()

