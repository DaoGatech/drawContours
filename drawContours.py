from flask import Flask, render_template, request
from flask_restful import Api
from flask_bootstrap import Bootstrap
import base64
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
    return ''

if __name__ == '__main__':
    app.run()

