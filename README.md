# Vehicle Rental System – DevOps Pipeline

A FastAPI-based Vehicle Rental System with vehicles, customers and bookings, automated CI/CD through Jenkins, Docker containerization, Kubernetes deployment, rollback support, monitoring, logging and Trivy security scanning.

## Features

- Vehicle CRUD APIs
- Customer CRUD APIs
- Booking APIs with vehicle/customer validation
- FastAPI Swagger documentation
- Health and metrics endpoints
- Pytest automated tests
- Docker image versioning
- Jenkins CI/CD
- Trivy HIGH/CRITICAL security scan
- Kubernetes deployment with readiness/liveness probes
- Kubernetes rollout history and rollback on pipeline failure
- Prometheus monitoring
- Grafana dashboard
- Kubernetes/application logging

## Ports

- Prometheus UI: **1000**
- Vehicle Rental API / Swagger: **1001**
- Grafana: **1002**
- Internal container ports: 8000 (app), 9090 (prometheus), 3000 (grafana)

## URLs

```text
http://localhost:1000         (Prometheus UI & Metrics)
http://localhost:1001/        (Vehicle Rental API)
http://localhost:1001/docs    (Swagger UI)
http://localhost:1001/health  (Health Check)
http://localhost:1001/metrics (Application Prometheus Metrics)
http://localhost:1002         (Grafana Observability Dashboard)
```

## API Endpoints

```text
GET/POST/PUT/DELETE /vehicles
GET/POST/PUT/DELETE /customers
GET/POST/PUT/DELETE /bookings
```

## CI/CD Pipeline

```text
Checkout
→ Versioning
→ Install Dependencies
→ Automated Tests
→ Dependency Validation
→ Docker Build
→ Trivy Security Scan
→ Image Verification
→ Kubernetes Preparation
→ Image Load
→ Deployment
→ Health/API Validation
→ Prometheus
→ Grafana
→ Monitoring/Logging Validation
→ Rollback Capability Check
→ Port Forwarding
```

On a failed pipeline after deployment, Jenkins attempts `kubectl rollout undo` for the Vehicle Rental deployment.

## Trivy Security Scanning

Trivy security scanning is fully integrated across the pipeline:

1. **Jenkins Pipeline (`Jenkinsfile`)**:
   - `Trivy Security Scan` stage automatically scans the repository filesystem and built Docker image (`vehicle-rental-service:v1.0.0`) for `HIGH` and `CRITICAL` vulnerabilities.

2. **GitHub Actions Workflow (`.github/workflows/trivy.yml`)**:
   - Automatically runs on `push` to `main`/`master` and pull requests to scan filesystem dependencies and Docker images.

3. **Local Developer Utility Script**:
   - **PowerShell (Windows)**: Run `.\trivy-scan.ps1`

```powershell
.\trivy-scan.ps1
```

## Kubernetes

Namespace:

```text
vehicle-rental-system
```

Application deployment:

```text
vehicle-rental-service
```

Monitoring namespace:

```text
monitoring
```
