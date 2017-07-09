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
        approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)

        print(len(approx))
        if len(approx) == 3:
            shape_name = "Triangle"
            cv2.drawContours(image, [cnt], 0, (0, 255, 0), -1)
            print("TRIANGLE")
            # Find contour center to place text at the center
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.putText(image, shape_name, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Check to see if 4-side polygon is square or rectangle
            # cv2.boundingRect returns the top left and then width and
            if abs(w - h) <= 3:
                shape_name = "Square"

                # Find contour center to place text at the center
                cv2.drawContours(image, [cnt], 0, (0, 125, 255), -1)
                cv2.putText(image, shape_name, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            else:
                shape_name = "Rectangle"

                # Find contour center to place text at the center
                cv2.drawContours(image, [cnt], 0, (0, 0, 255), -1)
                M = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.putText(image, shape_name, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

        elif len(approx) == 10:
            shape_name = "Star"
            cv2.drawContours(image, [cnt], 0, (255, 255, 0), -1)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.putText(image, shape_name, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)



        elif len(approx) >= 15:
            shape_name = "Circle"
            cv2.drawContours(image, [cnt], 0, (0, 255, 255), -1)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.putText(image, shape_name, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

        cv2.waitKey(0)

if __name__ == '__main__':
    app.run()

