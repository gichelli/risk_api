# Secure Developer-Friendly Release Pipeline Design

## 1. Introduction and Problem Statement
    - Current pipeline pain points
    - Goals
    - Why automation is needed

## 2. Architecture Overview
    - AWS
    - EKS
    - GitHub
    - GitHub Actions
    - ECR
    - Helm
    - ArgoCD
    - Terraform
    - Secrets Manager

---
# 2. Architecture Overview

The proposed release pipeline uses a cloud-native architecture designed around automation, security, and developer productivity.

The platform components are:

- Cloud Provider: AWS
- Container Platform: Amazon EKS Kubernetes
- Source Control: GitHub
- Continuous Integration: GitHub Actions
- Container Registry: Amazon ECR
- Continuous Delivery: ArgoCD using GitOps principles
- Infrastructure as Code: Terraform
- Secrets Management: AWS Secrets Manager with External Secrets Operator

High-level workflow:

Developer
    |
    v
GitHub Pull Request
    |
    v
GitHub Actions CI
    |
    +--> Unit Tests
    |
    +--> Linting
    |
    +--> Security Scanning
    |
    +--> Docker Build
    |
    v
Amazon ECR
    |
    v
ArgoCD
    |
    v
Amazon EKS
    |
    v
Environment Deployment
---

## 3. Demo Application Overview
    - What the application does
    - Why this demo model/API exists

---
# 3. Demo Application Overview

To demonstrate the release pipeline, this repository contains a small Flask-based risk classification API.

The application simulates a machine learning service that receives text input and returns a risk classification.

Example:

Request:

{
  "text": "armed conflict reported"
}

Response:

{
  "risk_level": "HIGH",
  "confidence": 0.90
}

The model logic is intentionally simple because the focus of this project is not model accuracy, but demonstrating:

- Application packaging
- Automated testing
- Containerization
- CI/CD workflows
- Kubernetes deployment
- Production promotion strategies
----


## 4. Local Developer Setup
    - Python venv
    - Dependencies
    - Make commands
    - Running tests
    - Running locally

---
Copy and paste this directly into your `README.md`:

```markdown
# 4. Local Developer Setup

This section describes how developers can set up the application locally and validate changes before opening a pull request.

The local workflow is designed to match the CI pipeline as closely as possible:

```

Developer Change
|
v
Install Dependencies
|
v
Run Tests
|
v
Run Linting
|
v
Build Docker Image
|
v
Submit Pull Request

````

---

## Prerequisites

Install the following tools:

- Python 3.11+
- Docker
- Git
- Make

Verify installations:

```bash
python3 --version
docker --version
make --version
````

---

## Clone Repository

Clone the repository:

```bash
git clone <repository-url>

cd platform_architecture_design
```

---

## Create Python Virtual Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

### macOS / Linux

```bash
source .venv/bin/activate
```

Verify:

```bash
which python
```

Expected:

```text
platform_architecture_design/.venv/bin/python
```

---

## Install Application Dependencies

Install the application and development dependencies:

```bash
make install
```

Dependencies are managed using:

```
app/risk_api/pyproject.toml
```

Installed development tools include:

* Flask application dependencies
* Gunicorn production server
* Pytest testing framework
* Ruff code quality tooling

---

## Run Automated Tests

Execute the test suite:

```bash
make test
```

Expected result:

```text
2 passed
```

The tests validate:

* Health endpoint behavior
* Risk prediction API behavior

---

## Run Code Quality Checks

Run linting:

```bash
make lint
```

Ruff validates:

* Import formatting
* Code quality rules
* Consistent Python standards

Expected result:

```text
All checks passed
```

---

## Run Application Locally

Start the application:

```bash
make run
```

The API will be available at:

```
http://localhost:8080
```

---

## Health Check

Verify the application is running:

```bash
curl http://localhost:8080/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

## Test Prediction API

Send a prediction request:

```bash
curl -X POST http://localhost:8080/predict \
-H "Content-Type: application/json" \
-d '{"text":"armed conflict reported"}'
```

Expected response:

```json
{
  "risk_level": "HIGH",
  "confidence": 0.9
}
```

---

## Build Docker Image

Build the application container:

```bash
make docker-build
```

This creates the container artifact:

```
risk-api:latest
```

The same container artifact will later be promoted through different environments:

```
Development
      |
      v
Staging
      |
      v
Production
```

using the automated release pipeline.

```

This section fits after **Architecture Overview** and before **Containerization / CI/CD Pipeline**.
```

---

## 5. Containerization
    - Dockerfile
    - Building image
    - Running container

## 6. CI/CD Pipeline
    - Pull request flow
    - Testing
    - Linting
    - Security scans
    - Image build

## 7. Artifact Management
    - ECR
    - Image tagging
    - Promotion strategy

## 8. Kubernetes Deployment
    - Helm charts
    - EKS
    - Configuration

## 9. GitOps Deployment
    - ArgoCD
    - Environment promotion

## 10. Security Controls
    - Dependency scanning
    - Container scanning
    - Secrets management

## 11. Operational Considerations
    - Monitoring
    - Logging
    - Rollbacks
    - Disaster recovery