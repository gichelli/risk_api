Let's break this down **one by one** from a Senior Platform Engineer perspective. These are the core Kubernetes capabilities that make the hosting platform reliable, scalable, and production-ready.

---

# 1. Deployments — Application Lifecycle Management

## What is a Kubernetes Deployment?

A **Deployment** is a Kubernetes object that manages the lifecycle of application workloads.

Instead of manually creating and managing containers, you define:

* What container image to run
* How many copies (replicas) should exist
* How updates should happen
* How failures should be recovered

Kubernetes Deployment ensures the desired state is maintained.

Example:

You want your API service to always have **3 running instances**.

You define:

```yaml
apiVersion: apps/v1
kind: Deployment

spec:
  replicas: 3

  template:
    spec:
      containers:
      - name: api
        image: my-api:v1.4.2
```

Kubernetes continuously monitors:

```
Desired State:
3 API pods

        vs

Current State:
2 API pods
```

If one pod crashes:

```
Before:

API Pod 1  ✅
API Pod 2  ❌
API Pod 3  ✅


Kubernetes creates:

API Pod 1  ✅
API Pod 2  ✅  (new)
API Pod 3  ✅
```

---

## Why use Deployments?

### Reliability

* Automatically replaces failed pods
* Maintains application availability

### Deployment Safety

Supports:

### Rolling Updates

Example:

Current version:

```
API v1

Pod 1
Pod 2
Pod 3
```

Deploy v2:

```
API v2

Replace Pod 1
Replace Pod 2
Replace Pod 3
```

No downtime.

---

### Rollback

If v2 has problems:

```
v2 ❌

Rollback

v1 ✅
```

Kubernetes keeps previous deployment history.

---

## In the release pipeline

The flow is:

```
CI Pipeline
    |
    v
Docker Image
    |
    v
ECR
    |
    v
Update Deployment image
    |
    v
Kubernetes rolls out new version
```

---

# 2. Services — Internal Communication

## What is a Kubernetes Service?

A **Service** provides stable network access to a group of pods.

Pods are temporary.

Example:

```
API Pod
10.0.1.5

API Pod
10.0.1.6

API Pod
10.0.1.7
```

Pods can disappear and get new IP addresses.

A Service gives them a stable endpoint:

```
api-service

      |
      |
----------------
|      |       |
Pod1   Pod2   Pod3
```

---

## Example

Frontend application needs to call backend API.

Without Service:

```
Frontend

calls:

10.0.1.5
```

Problem:

That IP may disappear.

With Service:

```
Frontend

calls:

api-service.default.svc.cluster.local


          |
          |
     Kubernetes
          |
   ----------------
   Pod1 Pod2 Pod3
```

The Service automatically routes traffic.

---

## Why use Services?

### Reliability

If a pod dies:

```
Pod 1 ❌

Service automatically sends traffic to:

Pod 2
Pod 3
```

---

### Load Balancing

The Service distributes requests:

```
Request 1 --> Pod 1

Request 2 --> Pod 2

Request 3 --> Pod 3
```

---

# 3. Ingress — External Traffic Routing

## What is Ingress?

Ingress manages traffic coming **from outside the Kubernetes cluster**.

Example:

A customer opens:

```
https://api.company.com
```

Ingress decides where that request goes.

Architecture:

```
Internet

    |
    v

Ingress Controller

    |
    |
--------------------
|                  |
Frontend Service    API Service
```

---

## Example routing rules:

```
company.com/

        |
        v
Frontend


company.com/api

        |
        v
Backend API
```

---

## Why use Ingress?

### Security

Provides:

* TLS termination
* HTTPS certificates
* Authentication integration

### Reliability

Can route traffic across multiple pods.

---

### Developer Experience

Developers do not need to manage:

* Load balancers
* DNS routing
* SSL configuration

---

# 4. Horizontal Pod Autoscaler (HPA) — Scaling

## What is HPA?

Horizontal Pod Autoscaler automatically changes the number of pods based on demand.

Example:

Normal traffic:

```
API Deployment

2 Pods
```

High traffic:

```
API Deployment

10 Pods
```

Low traffic:

```
API Deployment

2 Pods
```

---

## Example rule:

```
If CPU > 70%

Increase replicas
```

Example:

```
Current:

API Pods:
3


Traffic increases:

CPU = 85%


HPA scales:

API Pods:
8
```

---

## Why use HPA?

### Performance

Handles traffic spikes.

Example:

* Product launch
* High user activity
* Batch workloads

### Cost Efficiency

Does not run unnecessary resources.

---

# 5. Readiness and Liveness Probes — Application Health

These are Kubernetes health checks.

---

# Readiness Probe

## Question it answers:

> "Is this application ready to receive traffic?"

Example:

Application starts:

```
Container starts

     |
     |
Loading configuration

     |
     |
Connecting database

     |
     |
Ready
```

Before ready:

```
Traffic ❌
```

After ready:

```
Traffic ✅
```

---

Example:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8080
```

---

# Liveness Probe

## Question it answers:

> "Is this application still alive?"

Example:

Application hangs:

```
API process frozen

Container still running

but not responding
```

Kubernetes detects:

```
Liveness failed
```

Then:

```
Restart container
```

---

Example:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
```

---

# How all five work together

Complete production flow:

```
                Internet
                    |
                    v
               Ingress
                    |
                    v
              Kubernetes Service
                    |
        -------------------------
        |           |           |
       Pod         Pod         Pod
        |
        |
 Readiness Probe
        |
        |
 Application Healthy


        |
        v

Horizontal Pod Autoscaler

(add/remove pods based on load)


        |
        v

Deployment Controller

(manages versions and updates)
```

---

# How you explain this in the interview

A concise Senior-level answer:

> "The platform uses Kubernetes Deployments to manage application lifecycle and perform safe rolling updates. Services provide stable internal communication between workloads while abstracting away dynamic pod IPs. Ingress manages external traffic routing into the cluster. Horizontal Pod Autoscaler allows workloads to scale automatically based on demand. Readiness and liveness probes ensure only healthy applications receive traffic and automatically recover unhealthy containers."

That answer directly connects Kubernetes capabilities to **reliability, scalability, and developer experience**, which is what Extrac.ai is looking for.
