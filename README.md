# MINI RAG

## Requirements

- Python 3.8 or later

#### Install python using MiniConda

1) Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/main#quick-command-line-install)

2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag-app python=3.8
```

3) Activate the environment:
```bash 
$ conda activate mini-rag-app
```

### (Optional) Setup your command line interface for better readabiluty

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

## Install the required packages

```bash
$ pip install -r requiremnets.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value

### Run Docker Compose Services

```bash
$ sudo docker compose up -d
```

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN Collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)

