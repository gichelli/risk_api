Let's walk through a **real enterprise CI/CD + GitOps flow** from the moment you are a developer pushing code.

Assumptions:

* GitHub = source control
* GitHub Actions = CI/CD
* Amazon ECR = container registry
* ArgoCD = GitOps deployment
* EKS = Kubernetes clusters
* Environments:

  * Development
  * Staging
  * Production

A common branch model:

```text
main
 |
 |-- production
 |
staging
 |
develop
 |
feature branches
```

(Some companies use trunk-based development instead; the idea is the same.)

---

# Step 1 — Developer creates a branch

You start from the latest development branch:

```bash
git checkout develop
git pull

git checkout -b feature/payment-change
```

You modify:

```text
app/payment.py
```

Example:

```python
def process_payment():
    return "new logic"
```

---

# Step 2 — Developer pushes code

You commit:

```bash
git add .
git commit -m "change payment processing"

git push origin feature/payment-change
```

Now GitHub receives your branch.

---

# Step 3 — Pull Request is created

You open:

```
feature/payment-change
          |
          v
       develop
```

The PR automatically triggers CI.

---

# Step 4 — CI Pipeline starts

GitHub Actions runs.

Example:

```
.github/workflows/ci.yaml
```

The pipeline does:

---

## 4.1 Checkout code

```text
GitHub Actions
       |
       v
Downloads your branch
```

---

## 4.2 Code quality checks

Examples:

### Lint

```bash
ruff check .
```

Checks:

* style problems
* unused code
* bad practices

---

### Unit tests

```bash
pytest
```

Example:

```
100 tests passed
```

---

## 4.3 Security scanning

Multiple checks run.

### Dependency scanning

Checks:

```
requirements.txt
pyproject.toml
```

Example:

Finds:

```
Flask version has vulnerability
```

Pipeline fails.

---

### Static application security testing (SAST)

Scans your code.

Example:

Finds:

```python
password = "admin123"
```

Pipeline fails.

---

### Container scanning

After Docker build:

```
platform:a83f921
```

Scanner checks the image.

Example:

```
Critical CVE found
```

Pipeline fails.

---

# Step 5 — Build Docker image

If everything passes:

GitHub Actions builds:

```bash
docker build .
```

Creates:

```
platform:a83f921
```

where:

```
a83f921 = Git commit SHA
```

---

# Step 6 — Push image to ECR

GitHub Actions:

```
docker push
```

Uploads:

```
ECR

platform:a83f921
```

Now the artifact exists.

---

# Step 7 — Deploy automatically to Development

The pipeline updates your GitOps configuration.

Example:

Before:

```yaml
# environments/dev/values.yaml

image:
  tag: old123
```

After:

```yaml
image:
  tag: a83f921
```

Commit:

```
Deploy platform a83f921 to dev
```

---

# Step 8 — ArgoCD deploys Development

ArgoCD sees:

```
Git changed
```

It runs Helm:

```
Helm template
+
values-dev.yaml
```

Creates Kubernetes manifest:

```yaml
image:
  ECR/platform:a83f921
```

Deploys:

```
EKS Development Cluster
```

---

# Step 9 — Automated testing in Development

Now tests run against the deployed application.

Examples:

## Smoke tests

```
GET /health
```

Expected:

```
200 OK
```

---

## Integration tests

Example:

```
Create payment
Verify database update
```

---

## End-to-end tests

Example:

```
User login
Checkout
Payment
Receipt
```

---

If tests fail:

```
STOP
```

The image does not move.

---

# Step 10 — Promotion to Staging

If development tests pass:

The pipeline promotes the SAME image.

Important:

It does NOT rebuild.

You already have:

```
ECR/platform:a83f921
```

The staging configuration changes:

Before:

```yaml
image:
  tag: old555
```

After:

```yaml
image:
  tag: a83f921
```

---

ArgoCD deploys:

```
EKS Staging Cluster
```

---

# Step 11 — Staging validation

Run:

* QA tests
* regression tests
* performance tests
* security validation

Example:

```
Load test:
500 users
```

---

# Step 12 — Production approval

Now production promotion happens.

Usually:

A release approval is required.

Example:

```
Production deployment approved
```

This is often:

* Change management approval
* Product owner approval
* Automated policy approval

---

# Step 13 — Promote to Production

Again, no rebuild.

Same image:

```
ECR/platform:a83f921
```

Production configuration changes:

```yaml
image:
  tag: a83f921
```

ArgoCD deploys:

```
EKS Production Cluster
```

---

# Step 14 — Merge to main

The code promotion and deployment promotion are connected.

After staging approval:

A release PR is created:

```
develop
   |
   v
main
```

Example:

```
Merge release/payment-change
```

After merge:

```
main contains production code
```

---

# Final picture

```
Developer Laptop

      |
      |
      v

feature/payment-change

      |
      | Pull Request
      v

CI Pipeline
 |
 |-- Unit Tests
 |-- Lint
 |-- Security Scan
 |-- SAST
 |-- Dependency Scan
 |-- Build Docker
 |-- Container Scan
 |
 v

Amazon ECR

platform:a83f921

      |
      |
      v

Development EKS
      |
      |
 Automated Tests
      |
      v

Staging EKS
      |
      |
 Approval
      |
      v

Production EKS


      |
      v

main branch updated
```

The core principle:

**Code moves through Git. Artifacts move through environments.**

You do not rebuild for staging or production. You promote the exact Docker image that already passed testing. That is what makes the release process reliable and auditable.
