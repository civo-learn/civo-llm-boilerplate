from flask import Flask, render_template, request
from ollama import Client
import os
from PIL import Image
import base64
import io

app = Flask(__name__)
upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

ollama_model_text = os.environ.get('TEXT_MODEL')
ollama_model_image = os.environ.get('IMAGE_MODEL')

#  check if the application is running in a container
is_container = (
    os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
    or os.path.exists("/.dockerenv")
    or (
        os.path.isfile("/proc/self/cgroup")
        and (
            any("kubepods" in line for line in open("/proc/self/cgroup"))
            or any("docker" in line for line in open("/proc/self/cgroup"))
        )
    )
)

# use the localhost if not running in a container
if is_container:
    base_url = "http://ollama.ollama.svc.cluster.local:11434"
else:
    base_url = "http://localhost:11434" # Development endpoint port forwarded
    
client = Client(host = base_url)


def process_image(image_path):
    """Convert image to base64."""

    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format = "PNG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64


@app.route('/text')
def input_text():
    
    return render_template('text.html', model = ollama_model_text)

@app.route('/image')
def input_image():
    
    return render_template('image.html', model = ollama_model_image)

@app.route('/text_response', methods=['POST', 'GET'])
def submit_text():
    """Handle text submission and response."""

    ollama_text_prompt = request.form['text']

    ollama_output = client.chat(
        model=ollama_model_text,
        messages=[{'role': 'user', 'content': ollama_text_prompt}],
        stream=False,
    )

    return render_template('text_response.html', model = ollama_model_text, model_output = ollama_output['message']['content'])


@app.route('/image_response', methods=['POST', 'GET'])
def submit_image():
    """Handle image submission and response."""

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    #Get and process image
    ollama_input_image = request.files["ollama_input_image"]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], ollama_input_image.filename)
    ollama_input_image.save(filepath)
    img_base64 = process_image(filepath)

    #Get text prompt from frontend
    ollama_text_prompt = request.form["ollama_text_prompt"]

    #Model output
    ollama_output = client.generate(model = ollama_model_image, 
                images = [img_base64],
                prompt = ollama_text_prompt,
                stream = False)

    return ollama_output['response']


if __name__ == '__main__':
    if is_container:
        app.run(debug=True, host='0.0.0.0', port=80)
    else:
        app.run(debug=True, host='0.0.0.0')    
    