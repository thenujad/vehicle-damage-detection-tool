import cv2
import os
import numpy as np
import time  # To calculate processing time
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        technique = request.form.get('technique')
        message = ""
        details = {}

        if technique == 'canny':
            details = process_image_with_canny(filepath)
            message = "Canny Edge Detection applied successfully."
        elif technique == 'sobel':
            details = sobel_edge_detection(filepath)
            message = "Sobel Edge Detection applied successfully."
        else:
            details = process_image(filepath)
            message = "Contour Detection applied successfully."

        return render_template('index.html', filename=filename, message=message, details=details)

    return redirect(request.url)

# Processing techniques
def process_image(filepath):
    image = cv2.imread(filepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    cv2.imwrite(filepath, image)

    height, width = image.shape[:2]
    num_contours = len(contours)
    
    return {
        'height': height,
        'width': width,
        'num_contours': num_contours
    }

def process_image_with_canny(filepath):
    image = cv2.imread(filepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    start_time = time.time()
    edges = cv2.Canny(gray, 100, 200)
    end_time = time.time()

    cv2.imwrite(filepath, edges)
    height, width = edges.shape[:2]
    num_edges = np.sum(edges > 0)
    
    return {
        'height': height,
        'width': width,
        'num_edges': num_edges,
        'processing_time': round(end_time - start_time, 2)
    }

def sobel_edge_detection(filepath):
    image = cv2.imread(filepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    start_time = time.time()
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    sobel_edges = np.sqrt(sobelx ** 2 + sobely ** 2)
    end_time = time.time()

    cv2.imwrite(filepath, np.uint8(sobel_edges))
    height, width = gray.shape
    num_sobel_edges = np.sum(sobel_edges > 0)
    
    return {
        'height': height,
        'width': width,
        'num_sobel_edges': num_sobel_edges,
        'processing_time': round(end_time - start_time, 2)
    }

if __name__ == '__main__':
    app.run(debug=True)
