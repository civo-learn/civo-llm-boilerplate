# Project Name: Civo LLM Boilerplate

## Introduction

This project provides a boilerplate for deploying a K8s GPU Cluster on Civo Cloud using Terraform. It automates the setup of various applications and tools, including:

- [Ollama LLM Inference Server](https://github.com/ollama/ollama)
- [Ollama Web UI](https://github.com/open-webui/open-webui)
- [Nvidia Device Plugin](https://github.com/NVIDIA/k8s-device-plugin)
- An example Python LLM application

## Project Goal

The goal of this project is to enable customers to easily use Open Source Large Language Models (LLMs), providing 1:1 compatibility with OpenAI's ChatGPT.

- Access to the latest Open Source LLMs made available from Ollama
- Provide a user interface to allow non-technical users access to models
- Provide a path to produce insights with LLMs whilst maintaining sovereignty over the data
- Enable LLMs in regulatory usecases where ChatGPT can't be used.


## Prerequisites

Before beginning, ensure you have the following:

- A [Civo Cloud account](https://dashboard.civo.com/signup).
- A [Civo Cloud API Key](https://dashboard.civo.com/security).
- [Terraform](https://developer.hashicorp.com/terraform/install) installed on your local machine.
- [Docker Desktop](https://docs.docker.com/desktop/) installed and running (for building the example app).

## Project Setup

### Option 1: Environment variable (recommended)

```powershell
$env:CIVO_TOKEN = "YOUR_API_KEY"
```

### Option 2: Terraform variables file

Create `infra/tf/terraform.tfvars` with:

```hcl
civo_token = "YOUR_API_KEY"
```

## Project Configuration

Project configurations are managed within the `infra/tf/variables.tf` file. This file contains definitions and default values for the Terraform variables used in the project.

| Variable             | Description                                       | Type   | Default Value      |
|----------------------|---------------------------------------------------|--------|--------------------|
| `cluster_name`       | The name of the cluster.                          | string | "llm_boilerplate"  |
| `cluster_node_size`  | The GPU node instance to use for the cluster.     | string | "an.g1.l40s.kube.x1" |
| `cluster_node_count` | The number of nodes to provision in the cluster.  | number | 1                  |
| `civo_token`         | The Civo API token, set in terraform.tfvars.      | string | N/A                |
| `region`             | The Civo Region to deploy the cluster in.         | string | "NYC1"             |

## Deployment Configuration

Deployment of components is controlled through boolean variables within the `infra/tf/variables.tf` file. Set these variables to `true` to enable the deployment of the corresponding component.

| Variable                      | Description                                             | Type  | Default Value |
|-------------------------------|---------------------------------------------------------|-------|---------------|
| `deploy_ollama`               | Deploy the Ollama inference server.                     | bool  | true         |
| `deploy_ollama_ui`            | Deploy the Ollama Web UI.                               | bool  | true         |
| `deploy_app`                  | Deploy the example application.                         | bool  | false         |
| `deploy_nv_device_plugin_ds`  | Deploy the Nvidia GPU Device Plugin for enabling GPU support. | bool  | true         |
| `default_models`              | List of models to pre-pull in Ollama.                   | list  | ["llama3.3", "gemma3:4b", "qwen3:8b"] |
| `ollama_ui_image_version`     | Image tag for Open WebUI.                               | string | "v0.10.2"     |

## Deploy the Cluster

1. **Navigate to the Terraform directory:**

    ```
    cd infra/tf
    ```

2. **Initialize Terraform:**

    ```
    terraform init
    ```

    This installs the required providers and prepares the environment.

3. **Plan Deployment:**

    ```
    terraform plan
    ```

    This shows what resources will be created.

4. **Apply Deployment:**

    ```
    terraform apply
    ```

    Type `yes` when prompted. This takes 10-15 minutes.

5. **Get the Open WebUI IP:**

    ```
    terraform output ollama_ui_service_ip
    ```

    Open `http://<IP>` in your browser to access the chat interface.

## Building and Deploying the Example Application

The example app is a Flask service that connects to Ollama and returns a generated quote. It runs on port 8080 and exposes a health endpoint at `/health`.

### Enable the app

Set `deploy_app = true` in `infra/tf/variables.tf` or add it to `infra/tf/terraform.tfvars`:

```hcl
deploy_app = true
```

### Build and push the Docker image

1. **Build the image:**

    ```
    cd app
    docker build -t your-dockerhub-username/example .
    ```

2. **Push to Docker Hub:**

    Login if needed:
    ```
    docker login
    ```

    Then push:
    ```
    docker push your-dockerhub-username/example
    ```

### Update the Helm chart

Edit `infra/helm/app/values.yaml`:

```yaml
image:
  repository: your-dockerhub-username/example
  tag: "latest"

env:
  ollamaBaseUrl: "http://ollama.ollama.svc.cluster.local:11434"
  model: "llama3.3:latest"

service:
  type: LoadBalancer
  port: 80
  targetPort: 8080
```

### Deploy with Terraform

```
cd infra/tf
terraform apply
```

### Check the app

Get the LoadBalancer IP:

```
terraform output ollama_app_load_balancer_ip
```

Test it:

```
curl http://<IP>/
curl http://<IP>/health
```

The first returns a motivational quote from the LLM. The second returns `{"status":"ok"}`.

### Environment variables

The app accepts these environment variables (set in `infra/helm/app/values.yaml`):

| Variable          | Default                                        | Description            |
|-------------------|------------------------------------------------|------------------------|
| `OLLAMA_BASE_URL` | `http://ollama.ollama.svc.cluster.local:11434` | Ollama API endpoint    |
| `MODEL`           | `llama3.3:latest`                              | Model name to query    |

## Destroy Everything

```
cd infra/tf
terraform destroy
```

## Project Structure

```
├── app/                        # Example Flask application
│   ├── main.py                 # App entrypoint with / and /health endpoints
│   ├── Dockerfile              # Python 3.12-slim, non-root user
│   ├── requirements.txt        # Pinned dependencies
│   └── .dockerignore
├── infra/
│   ├── helm/
│   │   ├── app/                # Helm chart for the example app
│   │   ├── ollama-ui/          # Helm chart for Open WebUI
│   └── tf/                     # Terraform configuration
│       ├── providers.tf        # Terraform providers
│       ├── variables.tf        # All configurable variables
│       ├── civo-cluster.tf     # K8s cluster resource
│       ├── civo-network.tf     # Network resource
│       ├── civo-firewall.tf    # Firewall rules
│       ├── helm-ollama.tf      # Ollama Helm release
│       ├── helm-ollama-ui.tf   # Open WebUI Helm release
│       ├── helm-app.tf         # Example app Helm release
│       ├── manifest-nv-dvc-plugin-ds.tf  # Nvidia device plugin
│       └── outputs.tf          # Output values
├── notebooks/                  # Jupyter notebooks
│   ├── openai.ipynb
│   ├── langchain.ipynb
│   ├── llamaindex.ipynb
│   └── autogen.ipynb
└── .github/workflows/          # CI/CD workflows
```
