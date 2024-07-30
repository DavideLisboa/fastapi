# Microserviço de Lista de Tarefas com FastAPI

Este projeto é um microserviço baseado em FastAPI para gerenciar uma lista de tarefas (to-do list). Ele suporta operações CRUD, persistência de dados usando PostgreSQL, cache com Redis, conteinerização com Docker e orquestração com Kubernetes.

## Funcionalidades

- Criar, Ler, Atualizar, Excluir tarefas
- Persistência de dados com PostgreSQL
- Cache com Redis
- Conteinerização com Docker
- Orquestração com Kubernetes
- Deploy em um provedor de nuvem (Heroku, AWS, GCP)

## Estrutura do Projeto
fastapi/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── models.py
│ ├── crud.py
│ ├── schemas.py
│ ├── database.py
│ ├── cache.py
├── tests/
│ ├── init.py
│ ├── test_tasks.py
├── Dockerfile
├── docker-compose.yml
├── k8s/
│ ├── deployment.yaml
│ ├── service.yaml
│ ├── configmap.yaml
│ ├── secret.yaml
├── README.md
└── requirements.txt


## Configuração

### Requisitos

- Docker
- Docker Compose
- Kubernetes (kubectl e minikube ou um provedor de nuvem)
- Python 3.10

### Executando Localmente

1. Clone o repositório:
    ```bash
    git clone https://github.com/seunomeusuario/fastapi_todo.git
    cd fastapi_todo
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Inicie os serviços usando Docker Compose:
    ```bash
    docker-compose up --build
    ```

5. A API estará disponível em `http://localhost:8000`

### Executando os Testes

1. Execute os testes usando pytest:
    ```bash
    pytest
    ```

### Deploy com Kubernetes

1. Certifique-se de que seu cluster Kubernetes está em execução (minikube ou um provedor de nuvem).

2. Aplique os manifestos do Kubernetes:
    ```bash
    kubectl apply -f k8s/
    ```

3. O serviço estará disponível via o IP do LoadBalancer fornecido pelo seu cluster Kubernetes.

### Deploy em Provedor de Nuvem

1. Construa e envie sua imagem Docker para o Docker Hub (ou outro registro):
    ```bash
    docker build -t seunomeusuario_docker/fastapi_todo:latest .
    docker push seunomeusuario_docker/fastapi_todo:latest
    ```

2. Atualize a imagem no `k8s/deployment.yaml` para corresponder ao seu nome de usuário do Docker Hub.

3. Faça o deploy dos manifestos do Kubernetes conforme descrito na seção Deploy com Kubernetes.

4. Siga as instruções do seu provedor de nuvem para expor o serviço.
