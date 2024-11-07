from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the homepage that shows the upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        
        # Save the file to the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Optionally, process the image (e.g., open and save in a different format)
        img = Image.open(file_path)
        img = img.convert('RGB')  # Example: convert to RGB (if it's not)
        img.save(os.path.join(UPLOAD_FOLDER, f"processed_{filename}"))

        return f"File uploaded and processed successfully! Saved as {filename}", 200
    else:
        return "File type not allowed", 400

if __name__ == '__main__':
    app.run(debug=True)
