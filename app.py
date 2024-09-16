import cv2
import os
import numpy as np
import time
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['REPORT_FOLDER'] = 'static/reports'
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
        damage_info = {}

        if technique == 'canny':
            details = process_image_with_canny(filepath)
            message = "Canny Edge Detection applied successfully."
        elif technique == 'sobel':
            details = sobel_edge_detection(filepath)
            message = "Sobel Edge Detection applied successfully."
        else:
            details = process_image(filepath)
            message = "Contour Detection applied successfully."

        if details:
            # Assuming that the image is in BGR format
            image = cv2.imread(filepath)
            masked_image = mask_non_damage_areas(image)
            contours, _ = cv2.findContours(cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            severity, damage_percentage = calculate_damage_severity(contours, image.shape)
            damage_info = {
                'severity': severity,
                'damage_percentage': damage_percentage,
                'report_filename': generate_report(filepath, {
                    'severity': severity,
                    'damage_percentage': damage_percentage
                })
            }
        
        return render_template('index.html', filename=filename, message=message, details=details, damage_info=damage_info)

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

def mask_non_damage_areas(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_body = np.array([0, 0, 50])
    upper_body = np.array([180, 255, 255])
    mask = cv2.inRange(hsv_image, lower_body, upper_body)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    return masked_image

def calculate_damage_severity(contours, image_shape):
    damage_area = sum([cv2.contourArea(c) for c in contours])
    image_area = image_shape[0] * image_shape[1]
    damage_percentage = (damage_area / image_area) * 100
    if damage_percentage < 5:
        severity = 'Minor'
    elif damage_percentage < 15:
        severity = 'Moderate'
    else:
        severity = 'Severe'
    return severity, damage_percentage

def generate_report(image_path, damage_info):
    report_filename = "damage_report.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Vehicle Damage Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Severity: {damage_info['severity']}", ln=True)
    pdf.cell(200, 10, txt=f"Damage Percentage: {damage_info['damage_percentage']}%", ln=True)

    pdf.output(os.path.join(app.config['REPORT_FOLDER'], report_filename))
    return report_filename

if __name__ == '__main__':
    app.run(debug=True)
