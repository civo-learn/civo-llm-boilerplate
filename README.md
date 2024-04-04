
# Project Name: Civo LLM Boilerplate

## Introduction

This project provides a boilerplate for deploying a K8s GPU Cluster on Civo Cloud using Terraform. It automates the setup of various applications and tools, including:

- [Ollama LLM Inference Server](https://github.com/ollama/ollama)
- [Ollama Web UI](https://github.com/open-webui/open-webui)
- [Nvidia Device Plugin](https://github.com/NVIDIA/k8s-device-plugin)
- An example Python LLM application

## Project Goal

The goal of this project is to enable customers to easily use Open Source Large Language Models (LLMs), providing 1:1 compatibility with OpenAI's ChatGPT.

- Access to the latest Open Source LLMs made avaliable from Ollama
- Provide a user interface to allow non-technical users access to models
- Provide a path to produce insights with LLMs whilst maintaining soverignty over the data
- enable LLMs in regulatory usecases where ChatGPT can't be used.


## Prerequisites

Before beginning, ensure you have the following:

- A [Civo Cloud account](https://dashboard.civo.com/signup).
- A [Civo Cloud API Key](https://dashboard.civo.com/security).
- [Terraform](https://developer.hashicorp.com/terraform/install) installed on your local machine.

## Project Setup

1. Obtain your Civo API key from the Civo Cloud dashboard.
2. Create a file named `terraform.tfvars` in the project's root directory.
3. Insert your Civo API key into this file as follows:

    ```hcl
    civo_token = "YOUR_API_KEY"
    ```

## Project Configuration

Project configurations are managed within the `tf/variables.tf` file. This file contains definitions and default values for the Terraform variables used in the project.

| Variable             | Description                                       | Type   | Default Value      |
|----------------------|---------------------------------------------------|--------|--------------------|
| `cluster_name`       | The name of the cluster.                          | string | "llm_cluster3"     |
| `cluster_node_size`  | The GPU node instance to use for the cluster.     | string | "g4g.40.kube.small" |
| `cluster_node_count` | The number of nodes to provision in the cluster.  | number | 1                  |
| `civo_token`         | The Civo API token, set in terraform.tfvars.      | string | N/A                |
| `region`             | The Civo Region to deploy the cluster in.         | string | "LON1"             |

## Deployment Configuration

Deployment of components is controlled through boolean variables within the `tf/variables.tf` file. Set these variables to `true` to enable the deployment of the corresponding component.

| Variable                      | Description                                             | Type  | Default Value |
|-------------------------------|---------------------------------------------------------|-------|---------------|
| `deploy_ollama`               | Deploy the Ollama inference server.                     | bool  | true         |
| `deploy_ollama_ui`            | Deploy the Ollama Web UI.                               | bool  | true         |
| `deploy_app`                  | Deploy the example application.                         | bool  | false         |
| `deploy_nv_device_plugin_ds`  | Deploy the Nvidia GPU Device Plugin for enabling GPU support. | bool  | true         |

## Deploy LLM Boiler Plate

To deploy, simply run the following commands:

1. **Initialize Terraform:**

    ```
    terraform init
    ```

    This command initializes Terraform, installs the required providers, and prepares the environment for deployment.

2. **Plan Deployment:**

    ```
    terraform plan
    ```

    This command displays the deployment plan, showing what resources will be created or modified.

3. **Apply Deployment:**

    ```
    terraform apply
    ```

    This command applies the deployment plan. Terraform will prompt for confirmation before proceeding with the creation of resources.


## Building and deploying the Example Application
1. **Build the custom application container**
    Enter the application folder:
    ```
    cd app
    ```
    Build the docker image:
    ```
    docker build -t {repo}/{image} .
    ```
    Push the docker image to a registry:
    ```
    docker push -t {repo}/{image}
    ```
    Navigate to the helm chart:
    ```
    cd ../infra/helm/app
    ```
    Modify the Helm Values to point to your docker registry, e.g
    ```yaml
    replicaCount: 1
    image:
        repository: {repo}/{image}
        pullPolicy: Always
        tag: "latest"

    service:
        type: ClusterIP
        port: 80
    ```
2. **Initialize Terraform:**

    Navigate to the terraform directory
    ```
    cd ../tf
    ```

    ```
    terraform init
    ```

    This command initializes Terraform, installs the required providers, and prepares the environment for deployment.

3. **Plan Deployment:**

    ```
    terraform plan
    ```

    This command displays the deployment plan, showing what resources will be created or modified.

4. **Apply Deployment:**

    ```
    terraform apply
    ```

    This command applies the deployment plan. Terraform will prompt for confirmation before proceeding with the creation of resources.