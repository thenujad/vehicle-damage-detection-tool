# Object Boundary Detection Tool

## Overview

This project is designed to detect and highlight object boundaries in images using advanced image segmentation techniques. It leverages the power of OpenCV's contour detection and the Watershed algorithm to provide precise segmentation, which is essential for applications like medical imaging and industrial inspection.

## Features

- **Contour Detection**: Detects and highlights the boundaries of objects using OpenCV.
- **Watershed Algorithm**: Provides enhanced segmentation for overlapping or unclear boundaries (optional).
- **Web Interface**: Users can upload images via a Flask-based web application.
- **Glassmorphism UI**: Modern and stylish interface with a glassmorphism effect for a clean and aesthetic look.

## Technologies Used

- **Backend**: Python, OpenCV
- **Frontend**: HTML, CSS (with Glassmorphism effect), Flask
- **Workflow**: Users upload images, which are then processed to highlight object boundaries. The results are displayed on the web interface.

## Folder Structure

```
/project
│── /static
│   └── /uploads
│   └── /css
│       └── style.css
│── /templates
│   └── index.html
│── app.py
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install flask opencv-python numpy
```

### 4. Run the Flask Application

```bash
python app.py
```

### 5. Access the Application

Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

1. **Upload Image**: Use the file upload button to select an image from your local machine.
2. **Process Image**: After uploading, the image will be processed to detect and highlight object boundaries.
3. **View Results**: The processed image will be displayed on the same page.

## Example Use Cases

- **Medical Imaging**: Detecting and highlighting tumor boundaries in MRI scans.
- **Industrial Inspection**: Identifying and checking the boundaries of products on a manufacturing line.
- **Leaf Boundary Detection**: Highlighting the contour of leaves from images for further analysis.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenCV for image processing and computer vision.
- Flask for the web framework.
- CSS Glassmorphism for a modern UI effect.

