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
-----

This challenge is **not asking you to build a full production system**. It is asking you to **design and explain** a release pipeline. Your toy application is just the vehicle to prove the pipeline works.

The important thing is that your demo maps to every requirement in the challenge.

Here is how your project should line up with the challenge:

---

# Challenge Requirement → Your Demo Implementation

## 1. Different stages of the pipeline

You need to show the complete lifecycle:

```text
Developer
    |
    v
Feature Branch
    |
    v
Pull Request
    |
    v
CI Pipeline
    |
    +--> Unit Tests
    |
    +--> Lint
    |
    +--> Security Scan
    |
    +--> Docker Build
    |
    v
Merge to Main
    |
    v
Build Release Artifact
    |
    v
Push Image to ECR
    |
    v
Deploy with ArgoCD
    |
    v
Amazon EKS
```

Your toy Flask risk API demonstrates the artifact moving through this flow.

---

# 2. Technologies supporting each stage

Your assumptions:

| Area                | Technology                                      |
| ------------------- | ----------------------------------------------- |
| Source Control      | GitHub                                          |
| CI                  | GitHub Actions                                  |
| Container Build     | Docker                                          |
| Artifact Storage    | Amazon ECR                                      |
| Kubernetes Platform | Amazon EKS                                      |
| Deployment          | ArgoCD                                          |
| Packaging           | Helm                                            |
| Infrastructure      | Terraform                                       |
| Secrets             | AWS Secrets Manager + External Secrets Operator |
| Monitoring          | Prometheus + Grafana                            |

---

# 3. Environment Promotion

This is where your previous questions about tags come in.

The important concept:

**You do not rebuild images for every environment.**

You create one immutable artifact:

Example:

```text
risk-api:a83f921
```

Then promote that same image:

```text
Development
      |
      v
Staging
      |
      v
Production
```

Your environments have different Helm values:

Example:

```
helm/
 |
 └── risk-api/
      |
      ├── values.yaml
      |
      ├── values-dev.yaml
      |
      ├── values-staging.yaml
      |
      └── values-prod.yaml
```

Only configuration changes.

The image stays:

```
risk-api:a83f921
```

---

# 4. Security Gates

Your pipeline should include:

## Pull Request

Before merge:

```
Pull Request

 |
 +-- pytest
 |
 +-- ruff
 |
 +-- dependency scan
 |
 +-- secret scan
 |
 +-- container scan
 |
 v

Approved
```

Examples:

| Security Control           | Tool                   |
| -------------------------- | ---------------------- |
| Dependency vulnerabilities | Dependabot / Snyk      |
| Container vulnerabilities  | Trivy                  |
| Secrets detection          | GitHub Secret Scanning |
| IAM security               | AWS IAM policies       |

---

# 5. How artifacts are deployed

Your artifact flow:

```
Developer Code

    |
    v

GitHub Actions

    |
    v

Docker Image

    |
    v

Amazon ECR

    |
    v

Helm Chart

    |
    v

ArgoCD

    |
    v

Amazon EKS
```

---

# 6. Explain your choices

Your PDF should answer this:

---

## GitHub Actions

Why?

Security:

* Automated checks before merge
* Prevents insecure code reaching main

Reliability:

* Repeatable pipelines
* Same workflow every time

Developer Experience:

* Fast feedback on PRs

Speed:

* Parallel jobs
* Automated validation

---

## Amazon ECR

Why?

Security:

* IAM controlled access
* Image scanning
* Private registry

Reliability:

* Highly available AWS service

Developer Experience:

* Kubernetes integrates directly

Speed:

* Cached image pulls

---

## ArgoCD

Why?

Security:

* Kubernetes changes are Git controlled
* No manual kubectl deployments

Reliability:

* Automatic drift detection
* Rollback support

Developer Experience:

* Developers change configuration through Git

Speed:

* Automatic synchronization

---

## Amazon EKS

Why?

Security:

* Managed Kubernetes control plane
* IAM integration

Reliability:

* Multi-AZ architecture

Scalability:

* Horizontal pod autoscaling

---

# 7. Secrets and Config

Do not put secrets in:

```
values.yaml
```

Instead:

```
AWS Secrets Manager

        |
        v

External Secrets Operator

        |
        v

Kubernetes Secret

        |
        v

Application Pod
```

---

# Your current demo progress

You already have:

✅ Flask toy application
✅ Tests
✅ Linting
✅ Docker image
✅ GitHub Actions starting

Next pieces to implement:

1. Add security scanning to GitHub Actions
2. Add Docker image tagging strategy
3. Add ECR push
4. Add Helm deployment
5. Add ArgoCD structure
6. Create architecture diagram
7. Write PDF explanation

That will directly answer the challenge. You do **not** need a complicated ML model; the platform pipeline is the actual deliverable.
----
Good. Now your CI pipeline is doing something meaningful. Let's connect it back to the interview challenge.

Your current pipeline flow is:

```text
Developer
   |
   | git push / Pull Request
   v
GitHub Actions CI
   |
   +--> Tests
   |
   +--> Lint
   |
   +--> Dependency Security Scan
   |
   +--> Secret Scan
   |
   +--> Docker Build
   |
   +--> Push Image to ECR
```

Now let's explain each piece as a **security gate**.

---

# 1. Pull Request is the first gate

A developer does:

```bash
git checkout main
git pull
git checkout -b feature/payment-change

# make code changes

git push origin feature/payment-change
```

They open a PR:

```text
feature/payment-change
          |
          v
        main
```

The PR triggers:

```yaml
on:
  pull_request:
    branches:
      - main
```

The code is **not merged yet**.

The pipeline evaluates it first.

This is the first guardrail:

> "No unverified code reaches main."

---

# 2. Unit tests = functional safety gate

Your step:

```yaml
- name: Run tests
  run: |
    make test
```

Runs:

```text
pytest
```

Example:

Developer changes:

```python
def predict_risk():
    return "LOW"
```

But the test expects:

```python
assert risk_level == "HIGH"
```

Pipeline:

```
Tests ❌
```

Merge blocked.

Purpose:

> Prevent broken application behavior from being promoted.

---

# 3. Lint = code quality gate

Your step:

```yaml
- name: Run lint
  run: |
    make lint
```

Runs:

```text
ruff
```

Example:

Bad code:

```python
import os
import flask
import json
```

Pipeline:

```
Lint ❌
```

Purpose:

> Enforce engineering standards automatically.

---

# 4. Dependency scan = supply chain security gate

Your step:

```yaml
- name: Dependency security scan
  run:
    pip-audit
```

It checks your packages.

Example:

Your app has:

```
Flask==2.0.0
```

but that version has a known vulnerability.

Pipeline:

```
pip-audit ❌
```

Merge blocked.

Purpose:

> Prevent known vulnerable libraries from entering production.

---

# 5. Secret scanning = credential leak prevention

Your step:

```yaml
- name: Secret scanning
  uses: gitleaks/gitleaks-action@v2
```

Example developer accidentally commits:

```python
AWS_SECRET_KEY="AKIAxxxxxxxx"
```

Pipeline:

```
gitleaks ❌
```

Merge blocked.

Purpose:

> Prevent credentials from entering source control.

---

# 6. Docker build = deployment readiness gate

Your step:

```yaml
docker build
```

Checks:

* Dockerfile works
* dependencies install
* application can become a container

Example:

Developer changes:

```dockerfile
FROM python:3.11

COPY missing_file .
```

Build fails:

```
Docker build ❌
```

Purpose:

> Only deploy artifacts that can actually run.

---

# 7. ECR push = artifact creation

After everything passes:

```
Tests       ✅
Lint        ✅
Security    ✅
Docker      ✅
```

Only then:

```
Docker Image
       |
       v
ECR
```

Example:

```
037229268993.dkr.ecr.us-east-1.amazonaws.com/risk-api:a83f921
```

This is now your immutable artifact.

---

# How this maps to the challenge

The challenge asks:

> Design a secure developer-friendly release pipeline with guard rails.

You can explain:

> "The CI pipeline acts as the first control point. Pull requests trigger automated validation including unit tests, static analysis, dependency vulnerability scanning, secret detection, and container build validation. Only validated code can produce a deployable container artifact stored in ECR."

---

# What is still missing for the full challenge

You have completed:

✅ CI system
✅ Security gates
✅ Artifact storage (ECR)

Remaining:

## 1. Environment promotion

Need:

```
dev
 |
 v
staging
 |
 v
production
```

## 2. Helm deployment

Need:

```
ECR Image
     |
     v
Helm values
     |
     v
Kubernetes Deployment
```

## 3. ArgoCD GitOps

Need:

```
Git repo
   |
   v
ArgoCD
   |
   v
EKS
```

## 4. Secrets/config

Need:

```
AWS Secrets Manager
        |
        v
Kubernetes Secrets
        |
        v
Application
```

Your CI part is now the foundation. Next we should build the **CD side: how the ECR image gets promoted from dev → staging → production using Helm + ArgoCD**.
----
\at what point does it get merged to main


Great question. This is the missing piece in the flow.

In a **senior platform engineering setup**, the code is **not automatically merged to `main` just because CI passes** (usually). The normal flow is:

```text
Developer
   |
   v
Feature branch
   |
   v
Pull Request
   |
   v
CI runs (security gates)
   |
   +----------------+
   |                |
 FAIL             PASS
   |                |
 Fix code          |
                  v
          Required approvals
                  |
                  v
              Merge to main
```

---

## Step-by-step example

### 1. Developer creates a branch

Starting from main:

```bash
git checkout main
git pull

git checkout -b feature/payment-validation
```

Developer changes payment code.

---

### 2. Push branch

```bash
git add .
git commit -m "add payment validation"

git push origin feature/payment-validation
```

Now GitHub has:

```text
main
 |
 |
feature/payment-validation
```

---

### 3. Developer opens Pull Request

The PR says:

```
feature/payment-validation
            |
            v
          main
```

GitHub triggers:

```text
GitHub Actions
       |
       +-- pytest
       +-- lint
       +-- security scan
       +-- secret scan
       +-- docker build
```

---

### 4. CI passes

You get:

```
✓ Tests passed
✓ Lint passed
✓ Security scan passed
✓ Docker build passed
```

But the PR is still:

```
OPEN
```

---

### 5. Branch protection rules decide if it can merge

This is another guardrail.

In GitHub:

```
Repository Settings
    |
    v
Branches
    |
    v
main protection rules
```

Configure:

Require:

✅ Pull request before merging
✅ Require approvals
✅ Require status checks to pass
✅ Require conversation resolution

Example:

```
main branch

Cannot merge unless:

[✓] CI Pipeline passed
[✓] 1 engineer approved
```

---

### 6. Merge happens

Now a developer or reviewer clicks:

```
Merge Pull Request
```

Git creates:

```
feature/payment-validation
             |
             v
            main
```

Now your pipeline triggers:

```yaml
on:
  push:
    branches:
      - main
```

This is where you create the production artifact:

```
main
 |
 v
CI
 |
 v
Docker build
 |
 v
ECR
 |
 v
risk-api:a83f921
```

---

## Where does promotion happen?

After merge to main:

```
main
 |
 v
Build image
 |
 v
ECR
 |
 v
Deploy DEV
 |
 v
Testing
 |
 v
Promote STAGING
 |
 v
Approval
 |
 v
Promote PROD
```

The important distinction:

### CI answers:

> "Is this code safe to merge?"

### CD answers:

> "How do we safely move this approved artifact through environments?"

---

For your take-home, I would describe the flow as:

```
Developer Branch
       |
       v
Pull Request
       |
       v
CI Security Gates
       |
       v
Approval + Branch Protection
       |
       v
Merge to Main
       |
       v
Build Immutable Artifact
       |
       v
ECR
       |
       v
ArgoCD Promotion
       |
       v
EKS Environments
```

Your current demo is now at the point:

**PR → CI gates → merge → build/push artifact.**

The next thing we should implement is the **"after merge to main" part**, because that is where environment promotion begins.
----

You are right to call that out. I jumped ahead.

You **have not completed**:

```text
Developer
   |
   v
Pull Request
   |
   v
CI Security Gates
   |
   v
Merge to main
   |
   v
Docker Image
   |
   v
ECR
```

You have only completed part of it.

Let's put your demo exactly where it is.

---

## What you have actually completed

### 1. Developer creates code ✅

You have:

```text
platform_architecture_design
```

with:

```text
app/risk_api
```

You created:

* Flask API
* model
* tests
* Dockerfile
* Makefile

---

### 2. CI pipeline exists ✅

Your GitHub Actions does:

```text
Pull Request
      |
      v
GitHub Actions
      |
      +--> pytest
      |
      +--> ruff lint
      |
      +--> pip-audit
      |
      +--> gitleaks
      |
      +--> docker build
```

This part is done.

---

### 3. ECR push works manually ✅

You manually proved:

```text
Docker image
      |
      v
ECR
```

---

## What is NOT done yet

### A. CI does not yet push the image automatically

Your workflow has:

```yaml
docker push
```

but we have not confirmed a successful GitHub Actions run that:

1. builds the image
2. tags it
3. pushes it to ECR

The AWS OIDC part just started working.

We need to verify:

GitHub Actions:

```text
Configure AWS credentials ✅
Login ECR ✅
Build image ✅
Push image ✅
```

---

### B. Pull Request protection is not configured

Right now, GitHub will not necessarily block merging.

You need:

GitHub:

```
Repository
  |
  Settings
  |
  Branches
  |
  main
  |
  Branch protection rules
```

Enable:

```
☑ Require pull request before merging

☑ Require status checks to pass

☑ Require branches to be up to date

☑ Do not allow bypassing
```

Then select:

```
CI Pipeline
```

as required.

---

### C. The merge flow has not been tested

The actual test should be:

1. Create branch:

```bash
git checkout -b test-change
```

2. Change something small.

Example:

```python
return "LOW"
```

3. Push:

```bash
git push origin test-change
```

4. Open PR.

You should see:

```text
CI Pipeline running
```

5. Wait for:

```
Tests        ✅
Lint         ✅
Security     ✅
Docker       ✅
ECR Push     ✅
```

6. Merge button becomes available.

---

## So the next step is NOT environment promotion.

The next step is:

# Finish CI → Merge → ECR

Your immediate task:

1. Create a test branch.
2. Open a PR.
3. Confirm GitHub Actions runs.
4. Confirm the image appears in ECR.

Only after that we move to:

```
ECR
 |
 v
Environment promotion
 |
 v
Dev → Staging → Production
```

You were correct — I skipped a major milestone. We need to finish the release pipeline foundation before building CD.


--- order terraform first

platform_infrastructure
        |
        v
AWS foundation exists
(ECR + EKS + IAM + networking)
        |
        v
risk_api
        |
        v
Build + scan + push image to ECR
        |
        v
risk_api_gitops
        |
        v
Helm + ArgoCD deployment
        |
        v
Environment promotion
(dev → qa → staging → production)


Yes. Given your three repositories and the fact that your **CI + release pipeline in `risk_api` is already mostly working**, I would start with **Terraform/platform infrastructure first**.

The reason: your application pipeline can build and push images, but there is nowhere to deploy yet. The dependency order is:

```text
platform_infrastructure
        |
        v
AWS foundation exists
(ECR + EKS + IAM + networking)
        |
        v
risk_api
        |
        v
Build + scan + push image to ECR
        |
        v
risk_api_gitops
        |
        v
Helm + ArgoCD deployment
        |
        v
Environment promotion
(dev → qa → staging → production)
```

Here is the exact checklist I would follow.

---

# Phase 1 — Platform Infrastructure (`platform_infrastructure`)

Repository:

```text
platform_infrastructure
```

Goal:

Create the AWS platform using Terraform.

## Step 1. Terraform foundation

Verify:

```text
terraform/
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
```

Need:

* AWS provider
* region variable
* Terraform state configuration

Commands:

```bash
terraform init
terraform validate
terraform plan
```

---

## Step 2. Create networking

Add/verify:

```text
terraform/vpc.tf
```

Create:

* VPC
* public subnets
* private subnets
* route tables
* security groups

For a demo:

* avoid NAT Gateway if possible to reduce cost

Test:

```bash
terraform plan
```

---

## Step 3. Create ECR

File:

```text
terraform/ecr.tf
```

Create:

```text
risk-api ECR repository
```

Expected output:

```text
037229268993.dkr.ecr.us-east-1.amazonaws.com/risk-api
```

Add:

```text
terraform outputs
```

Example:

```hcl
output "ecr_repository_url" {
  value = aws_ecr_repository.risk_api.repository_url
}
```

Test:

```bash
terraform apply
```

Verify:

```bash
aws ecr describe-repositories
```

---

## Step 4. Create EKS

File:

```text
terraform/eks.tf
```

Create:

* EKS cluster
* managed node group
* IAM roles

Goal:

```text
EKS Cluster
 |
 +-- worker nodes
```

Apply:

```bash
terraform apply
```

Verify:

```bash
aws eks update-kubeconfig \
--region us-east-1 \
--name <cluster-name>
```

Then:

```bash
kubectl get nodes
```

Expected:

```text
Ready
```

---

## Step 5. Configure GitHub Actions IAM

Your `risk_api/release.yaml` already uses:

```yaml
id-token: write
```

So Terraform should create:

* IAM role
* OIDC trust relationship
* ECR permissions

Test:

Push code.

Verify GitHub Actions can:

```text
login AWS
push image ECR
```

---

# Phase 2 — GitOps Repository (`risk_api_gitops`)

Repository:

```text
risk_api_gitops
```

Goal:

Deploy the application into Kubernetes.

---

## Step 6. Fix Helm chart

Verify:

```text
helm/demo
```

Files:

```text
Chart.yaml

templates/
├── deployment.yaml
├── service.yaml
├── ingress.yaml
├── hpa.yaml
└── _helpers.tpl
```

Deployment must use:

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

---

## Step 7. Create Helm values structure

Create:

```text
helm/demo/values.yaml
```

Shared:

```yaml
image:
  repository: 037229268993.dkr.ecr.us-east-1.amazonaws.com/risk-api
  tag: ""

replicaCount: 1
```

Create:

```text
environments/
├── dev/
│   └── values.yaml
├── qa/
│   └── values.yaml
├── staging/
│   └── values.yaml
└── production/
    └── values.yaml
```

---

## Step 8. Install ArgoCD

On EKS:

```bash
kubectl create namespace argocd
```

Install ArgoCD.

Verify:

```bash
kubectl get pods -n argocd
```

---

## Step 9. Create ArgoCD application

File:

```text
risk_api_gitops/argocd/application.yaml
```

Connect:

```text
GitHub
   |
   v
risk_api_gitops
   |
   v
EKS
```

Test:

```bash
kubectl get applications -n argocd
```

---

# Phase 3 — Connect Release Pipeline (`risk_api`)

Repository:

```text
risk_api
```

You already have:

✅ tests
✅ lint
✅ dependency scan
✅ Docker build
✅ ECR push

Need to add:

---

## Step 10. Update GitOps after image push

After:

```bash
docker push
```

Add:

```text
Checkout risk_api_gitops
        |
Update values.yaml tag
        |
Commit
        |
Push
```

Example:

```yaml
image:
  tag: ${{ github.sha }}
```

---

# Phase 4 — Promotion Workflow

Add:

```text
.github/workflows/promote.yaml
```

Flow:

```text
DEV
 |
 approval
 |
QA
 |
 approval
 |
STAGING
 |
 approval
 |
PRODUCTION
```

Promotion changes only:

```yaml
image:
  tag:
```

Example:

Before:

```yaml
tag: abc123
```

After:

```yaml
tag: def456
```

---

# Final End-to-End Test

You should be able to demonstrate:

```text
1. Developer opens PR
        |
2. CI runs
        |
3. Security gates pass
        |
4. Merge to main
        |
5. Release builds Docker image
        |
6. Push image to ECR
        |
7. Update GitOps repo
        |
8. ArgoCD deploys DEV
        |
9. Promote DEV → QA
        |
10. Promote QA → PROD
```

---

So yes, the order is:

1. **Terraform (`platform_infrastructure`)**
2. **Verify EKS exists**
3. **Fix GitOps (`risk_api_gitops`)**
4. **Connect ArgoCD**
5. **Connect release pipeline to GitOps**
6. **Add promotion workflow**

That order will also give you the best Terraform interview practice because you will actually go through `init → plan → apply → destroy`.




------



I actually think this is the better direction for your challenge.

If I were interviewing a Senior Platform Engineer, I would be **more impressed** by someone who used the official AWS Terraform modules correctly than by someone who hand-wrote hundreds of lines of Terraform resources.

## This is the architecture I recommend

```text
platform_infrastructure/
└── terraform/
    ├── providers.tf
    ├── versions.tf
    ├── variables.tf
    ├── terraform.tfvars
    ├── vpc.tf
    ├── ecr.tf
    ├── eks.tf
    ├── iam.tf
    └── outputs.tf
```

Instead of creating:

* aws_vpc
* aws_subnet
* aws_internet_gateway
* aws_route_table
* aws_eks_cluster
* aws_eks_node_group
* IAM attachments
* security groups

manually...

we use:

* **terraform-aws-modules/vpc/aws**
* **terraform-aws-modules/eks/aws**

These are the de facto standard modules used by many AWS teams.

---

# I would restart Phase 1

Since your files are basically empty, it's actually easier to rebuild them cleanly.

We'll build this in order:

## Step 1

```
versions.tf
```

Terraform version

AWS provider

---

## Step 2

```
providers.tf
```

AWS provider configuration

---

## Step 3

```
variables.tf
```

Variables

---

## Step 4

```
terraform.tfvars
```

Configuration

Example:

```hcl
aws_region  = "us-east-1"
cluster_name = "risk-api-cluster"
environment = "demo"
```

---

## Step 5

```
vpc.tf
```

Official AWS VPC module

---

## Step 6

```
ecr.tf
```

ECR repository

---

## Step 7

```
iam.tf
```

GitHub OIDC

IAM

---

## Step 8

```
eks.tf
```

Official AWS EKS module

---

## Step 9

```
outputs.tf
```

Outputs

---

Then:

```bash
terraform fmt
terraform init
terraform validate
terraform plan
terraform apply
```

---

# Why this is better

When the interviewer asks:

> Why did you use modules?

You can answer:

> "I used the official `terraform-aws-modules` because they encapsulate AWS best practices, reduce maintenance, and are widely adopted in production. They let me focus on the platform architecture rather than reimplementing well-tested infrastructure components."

That is a much stronger answer than:

> "I copied 500 lines of VPC resources from a blog."

---

# I would also make one improvement

Instead of creating everything in one shot, I would build and test in this order:

### Milestone 1

```
VPC
```

Test

---

### Milestone 2

```
ECR
```

Test

---

### Milestone 3

```
EKS
```

Test

---

### Milestone 4

```
IAM
```

Test

---

### Milestone 5

```
GitHub OIDC
```

Test

---

### Milestone 6

```
ArgoCD
```

Test

---

I think this will give you a much more professional repository and a much better story during your interview. We can build it file by file, testing each milestone before moving on.
----


```
Developer
    |
    v
risk_api repo
    |
    | Pull Request
    v
GitHub Actions CI
    |
    +-- Unit tests
    +-- Lint
    +-- Dependency scan
    +-- Secret scan
    +-- Docker build
    +-- Container scan
    |
    v
Merge to main
    |
    v
Release Pipeline
(risk_api/.github/workflows/release.yaml)
    |
    | GitHub OIDC
    v
AWS IAM Role
(created by Terraform)
    |
    v
Amazon ECR
    |
    | image:
    | risk-api:<commit-sha>
    v
Update GitOps repo
    |
    v
risk_api_gitops
    |
    +-- dev values.yaml
    +-- qa values.yaml
    +-- staging values.yaml
    +-- production values.yaml
    |
    v
ArgoCD
    |
    v
EKS Cluster
(created by Terraform)
    |
    v
Application running
```
Once `terraform apply` succeeds, your **platform foundation is ready**. Then you move to connecting your three repositories into a complete end-to-end delivery pipeline.

Your three repos:

```text
1. risk_api
   → Application code
   → CI
   → Docker build
   → Push image to ECR

2. risk_api_gitops
   → Kubernetes manifests
   → Helm charts
   → Environment promotion
   → ArgoCD watches this repo

3. platform_infrastructure
   → Terraform
   → AWS infrastructure
   → EKS
   → ECR
   → IAM
```

The complete flow becomes:

```text
Developer
    |
    v
risk_api repo
    |
    | Pull Request
    v
GitHub Actions CI
    |
    +-- Unit tests
    +-- Lint
    +-- Dependency scan
    +-- Secret scan
    +-- Docker build
    +-- Container scan
    |
    v
Merge to main
    |
    v
Release Pipeline
(risk_api/.github/workflows/release.yaml)
    |
    | GitHub OIDC
    v
AWS IAM Role
(created by Terraform)
    |
    v
Amazon ECR
    |
    | image:
    | risk-api:<commit-sha>
    v
Update GitOps repo
    |
    v
risk_api_gitops
    |
    +-- dev values.yaml
    +-- qa values.yaml
    +-- staging values.yaml
    +-- production values.yaml
    |
    v
ArgoCD
    |
    v
EKS Cluster
(created by Terraform)
    |
    v
Application running
```

---

# After Terraform succeeds, do this order

## Phase 1 — Verify infrastructure

Repository:

```text
platform_infrastructure
```

Run:

```bash
aws eks update-kubeconfig \
--region us-east-1 \
--name risk-api
```

Test:

```bash
kubectl get nodes
```

You should see your worker node(s).

Test:

```bash
kubectl get namespaces
```

---

# Phase 2 — Connect ECR to risk_api release pipeline

Repository:

```text
risk_api
```

Your Terraform output gives:

```bash
terraform output ecr_repository_url
```

Example:

```text
037229268993.dkr.ecr.us-east-1.amazonaws.com/risk-api
```

Add GitHub variable:

```
ECR_REGISTRY

037229268993.dkr.ecr.us-east-1.amazonaws.com
```

Your release workflow:

```yaml
env:
  ECR_REGISTRY: ${{ vars.ECR_REGISTRY }}
  IMAGE_NAME: risk-api
```

will push:

```
037229268993.dkr.ecr.us-east-1.amazonaws.com/risk-api:<commit-sha>
```

---

# Phase 3 — Update GitOps repository

Repository:

```text
risk_api_gitops
```

Your Helm values currently:

```yaml
image:
  repository: ...
  tag: ...
```

Should become:

```yaml
image:
  repository: 037229268993.dkr.ecr.us-east-1.amazonaws.com/risk-api
  tag: "commit-sha"
```

But do NOT manually edit this every deployment.

Your release pipeline should update it.

Example:

After Docker push:

```yaml
IMAGE_TAG=${{ github.sha }}
```

Then:

```bash
cd risk_api_gitops

yq e \
-i '.image.tag="'$IMAGE_TAG'"' \
environments/dev/values.yaml

git add .
git commit -m "Deploy risk-api $IMAGE_TAG"
git push
```

Now GitOps repo becomes the deployment source.

---

# Phase 4 — Install ArgoCD

This belongs to:

```text
risk_api_gitops
```

Your file:

```
argocd/application.yaml
```

should point to:

```yaml
spec:
  source:
    repoURL: https://github.com/gichelli/risk_api_gitops
    path: helm/demo
```

ArgoCD watches that repo.

When:

```
values.yaml
```

changes:

```
new image tag
```

ArgoCD deploys automatically.

---

# Phase 5 — Environment promotion

Your GitOps repo already has:

```
environçments/
├── dev
│   └── values.yaml
├── qa
│   └── values.yaml
├── staging
│   └── values.yaml
└── production
    └── values.yaml
```

The flow:

```
risk_api
   |
   | build image
   |
   v
ECR
   |
   |
   v
dev values.yaml
   |
   | approval
   v
qa values.yaml
   |
   | approval
   v
staging values.yaml
   |
   | approval
   v
production values.yaml
```

---

# What you should work on after Terraform

Your order:

## 1. Finish Terraform

✅ VPC
✅ ECR
✅ EKS
✅ IAM OIDC

↓

## 2. Validate Kubernetes access

```bash
kubectl get nodes
```

↓

## 3. Finish Helm chart

Repo:

```
risk_api_gitops
```

Test:

```bash
helm lint helm/demo
```

↓

## 4. Install ArgoCD

↓

## 5. Connect ArgoCD application.yaml

↓

## 6. Modify release.yaml to update GitOps repo

↓

## 7. Test full flow:

```
git push
      |
      v
CI
      |
      v
Docker image
      |
      v
ECR
      |
      v
GitOps commit
      |
      v
ArgoCD
      |
      v
EKS pod running
```

That is the complete end-to-end platform engineer challenge. Your Terraform is the foundation; after that the focus moves to **GitOps automation and deployment flow**.


----
```
Developer
    |
    v
Feature branch
    |
    v
Pull Request
    |
    v
CI checks
    |
    v
Merge
    |
    v
Build Docker image
    |
    v
ECR
    |
    |
    |  <-- PROMOTION STARTS HERE
    |
    v
GitOps repo

dev values.yaml
    |
    v
ArgoCD
    |
    v
DEV


approval

qa values.yaml
    |
    v
ArgoCD
    |
    v
QA


approval

staging values.yaml
    |
    v
STAGING


approval

production values.yaml
    |
    v
PRODUCTION
```

----

```
Developer changes code
        |
        v
Pull Request
        |
        v
CI tests
        |
        +--> Unit tests
        +--> Lint
        +--> Security scans
        +--> Build validation
        |
        v
Merge to main
        |
        v
Build Docker image
        |
        v
Push image to ECR
        |
        v
Deploy DEV (ArgoCD)
        |
        v
DEV environment tests
        |
        +--> Smoke tests
        +--> Integration tests
        |
        v
Promote QA
        |
        v
QA testing
        |
        +--> Regression tests
        +--> Functional tests
        |
        v
Promote Staging
        |
        v
Production
```

---

promote-dev.yaml
        |
        v
Update environments/dev/values.yaml
        |
        v
ArgoCD detects Git change
        |
        v
ArgoCD deploys DEV
        |
        v
Deployment complete
        |
        v
RUN DEV TESTS  <--------- this is the missing step
        |
        +--> Smoke tests
        |
        +--> Integration tests
        |
        v
Tests PASS?
        |
        +------ NO ---> STOP
        |
        +------ YES
                |
                v
          promote-qa.yaml
                |
                v
          Update environments/qa/values.yaml
                |
                v
          ArgoCD deploys QA