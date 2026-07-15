# Risk API

A production-style REST API service that provides risk prediction capabilities.
The application is containerized with Docker and deployed through an automated
CI/CD and GitOps delivery pipeline to Kubernetes.

## Overview

## Architecture Overview

The Risk API repository implements the application delivery lifecycle from
source code commit through container image publication.

The repository is responsible for:

- Flask API application code
- Automated testing
- Code quality validation
- Security scanning
- Docker image creation
- Publishing images to Amazon ECR
- Triggering GitOps deployment workflows


## Architecture

```

Developer
    |
    | Pull Request
    v
GitHub Repository
(risk_api)
    |
    |
    +-----------------------------+
    |                             |
    v                             v
CI Pipeline                  Security Pipeline
GitHub Actions               GitHub Actions
    |                             |
    |                             |
    +-------------+---------------+
                  |
                  v
          Docker Build Validation
                  |
                  v
          Container Security Scan
          (Trivy)
                  |
                  v
          Application Smoke Test
                  |
                  v
             Merge to main
                  |
                  v
          Release Pipeline
                  |
                  v
          Build Docker Image
                  |
                  v
          Amazon ECR
                  |
                  v
     GitHub Repository Dispatch Event
                  |
                  v
        GitOps Repository Update

````

## Deployment Architecture

Deployment is managed outside this repository using GitOps principles.

The deployment flow is:

```
risk_api
   |
   | Docker Image
   v
Amazon ECR
   |
   |
GitOps Repository
   |
   | Helm Values Update
   v
ArgoCD
   |
   v
Amazon EKS
   |
   v
Risk API Kubernetes Deployment
```

The separation between application and deployment repositories provides:

- Independent application and infrastructure lifecycle management
- Auditable deployment changes
- Environment promotion controls
- Declarative Kubernetes state management

## Application Stack

| Component | Technology |
|---|---|
| API Framework | Flask |
| Language | Python 3.11 |
| Container Runtime | Docker |
| Container Registry | Amazon ECR |
| Orchestration | Kubernetes |
| Cloud Platform | AWS EKS |
| Deployment | Helm + ArgoCD |
| CI/CD | GitHub Actions |

---

# Local Development

## Prerequisites

Install:

- Python 3.11+
- Docker
- Make

Clone the repository:

```bash
git clone <repository-url>

cd risk_api
````

---

## Install Dependencies

Create virtual environment:

```bash
python -m venv .venv

source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the API:

```bash
python src/app.py
```

The API will start on:

```
http://localhost:5000
```

---

# API Endpoints

## Health Check

Request:

```bash
curl http://localhost:5000/health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Risk Prediction

Request:

```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '
{
  "features": {
    "income": 80000,
    "credit_score": 720
  }
}'
```

Response:

```json
{
  "risk": "low"
}
```

---

# Testing

Run unit tests:

```bash
pytest
```

Run linting:

```bash
flake8 .
```

---

# Docker

## Build Image

```bash
docker build -t risk-api .
```

## Run Container

```bash
docker run -p 5000:5000 risk-api
```

Test:

```bash
curl http://localhost:5000/health
```

---

# CI Pipeline

Every pull request triggers automated validation:

```
Pull Request
      |
      v
GitHub Actions
      |
      +--> Unit Tests
      |
      +--> Lint Validation
      |
      +--> Dependency Security Scan
      |
      +--> Docker Build Validation
```

A change must pass CI before being merged.

---

# Release Pipeline

Changes merged into `main` trigger:

```
Merge
 |
 v
Build Docker Image
 |
 v
Push Image to Amazon ECR
 |
 v
Update GitOps Repository
 |
 v
ArgoCD Deployment
 |
 v
Amazon EKS
```

---

# Deployment Strategy

The application uses GitOps principles:

* Kubernetes manifests are stored separately from application code
* Container image versions are promoted through environments
* ArgoCD continuously reconciles desired state

Environment promotion flow:

```
Development
      |
      v
QA
      |
      v
Staging
      |
      v
Production
```

---

# Configuration

Application configuration is provided through environment variables.

Example:

```bash
FLASK_ENV=production
PORT=5000
```

Secrets are not stored in Git.

Production secrets should be managed using:

* AWS Secrets Manager
* Kubernetes Secrets
* External Secrets Operator

---

# Security Considerations

Implemented:

* Non-root Docker container execution
* Dependency vulnerability scanning
* Least privilege IAM access
* Private Kubernetes workloads
* Image scanning before deployment

---

# Repository Structure

```
.
├── .github
│   └── workflows
│       ├── ci.yaml
│       └── release.yaml
├── .gitignore
├── DESIGN.md
├── Dockerfile
├── Makefile
├── README.md
├── docs
├── ai-release-pipeline-architecture.png
├── -release-pipeline-design.pdf
├── pyproject.toml
├── src
│   ├── __init__.py
│   ├── app.py
│   └── model.py
└── tests

    ├── e2e
    │   └── test_user_flow.py
    ├── functional
    │   └── test_api_functional.py
    ├── integration
    │   └── test_prediction_api.py
    ├── performance
    │   └── locustfile.py
    ├── regression
    │   └── test_regression.py
    ├── security
    │   └── test_security.py
    ├── smoke
    │   └── test_health.py
    └── unit
        └── test_model.py

```

---

