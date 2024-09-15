# Vehicle Damage Detection Tool

## Overview

The Vehicle Damage Detection Tool is a web-based application for detecting and analyzing vehicle damage from images. It uses various image processing techniques to identify and assess damage severity. The tool supports the following processing techniques:

- Contour Detection
- Canny Edge Detection
- Sobel Edge Detection

## Features

- **Upload Image**: Upload an image of the vehicle.
- **Processing Techniques**: Choose from contour detection, Canny edge detection, or Sobel edge detection.
- **Object Masking**: Mask non-damage areas to focus on damaged regions.
- **Damage Scoring**: Calculate damage severity and percentage.
- **Damage Report**: Download a PDF report with damage details.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/vehicle-damage-detection.git
   cd vehicle-damage-detection
   ```

2. **Set Up the Environment**

   Make sure you have Python 3.x installed. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask Application**

   Start the Flask server:

   ```bash
   python app.py
   ```

2. **Access the Web Interface**

   Open your web browser and go to `http://127.0.0.1:5000/` to access the tool.

3. **Upload an Image**

   - Click on "Choose Processing Technique" to select a method.
   - Upload the vehicle image and click "Analyze Damage".
   - View the processed image, damage severity, and download the damage report.

## Configuration

- **UPLOAD_FOLDER**: Directory where uploaded images are stored.
- **REPORT_FOLDER**: Directory where PDF reports are saved.

Adjust these settings in `app.py` if needed.

## Dependencies

- Flask
- OpenCV
- NumPy
- Werkzeug
- FPDF

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenCV for image processing capabilities.
- Flask for web application framework.
- FPDF for PDF report generation.
