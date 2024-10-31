from flask import Flask
from openai import OpenAI
from os import path
app = Flask(__name__)

#  check if the application is running in a container
is_container = (
    path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
    or path.exists("/.dockerenv")
    or (
        path.isfile("/proc/self/cgroup")
        and (
            any("kubepods" in line for line in open("/proc/self/cgroup"))
            or any("docker" in line for line in open("/proc/self/cgroup"))
        )
    )
)

@app.route('/')
def return_results():
    
    # use the localhost if not running in a container
    if is_container:
        ollama_api_endpoint = "http://ollama.ollama.svc.cluster.local:11434"
    else:
        ollama_api_endpoint = "http://localhost:11434" # Development endpoint port forwarded
    
    client = OpenAI(
        base_url = ollama_api_endpoint + '/v1',
        api_key='forced_key', # required, but unused
    )
    
    # generate a response
    response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a motivational quote."},
        ]
    )
    
    # return the response
    return response.choices[0].message.content

if __name__ == '__main__':
    if is_container:
        app.run(debug=True, host='0.0.0.0', port=80)
    else:
        app.run(debug=True, host='0.0.0.0')
    
    